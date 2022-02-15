import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

// TODO: Create and Migrate all API Methods to Async/Await
const Service = {
    // Attempts
    attempts: 0,
    csrf_attempts: 0,
    time_wait: 3000,
    logging: false,

    // Utils
    _responseIsObject: (r) => typeof r.data === 'object',
    _responseIsString: (r) => typeof r.data === 'string',
    redirectToLogin() {
        window.location.replace('http://' + window.location.host + '/login/');
    },

    _connectionError(vm) {
        // Detect CSRF Errors
        if (this.csrf_attempts > 2) {   // Max 3 attempts
            if (vm.$route.name !== 'error.forbidden') {
                vm.$router.push({name:'error.forbidden', params: {
                    error_type: '403',
                    error_message: 'Error verificando el CSRF Token. Por favor, reenvie el Formulario o ' +
                        'vuelva a <a href="/super/">Inicio</a>!'
                }});
            }
            return true;
        }
        // Detect Connection Errors
        if (this.attempts > 4) {        // Max 5 attempts
            if (vm.$route.name !== 'error.connection') {
                vm.$router.push({name:'error.connection'});
            }
            return true;
        }
        this.attempts++;
        return false;
    },
    _resetAttempts() {
        this.attempts = 0;
    },
    _resetCSRFAttempts() {
        this.csrf_attempts = 0;
    },
    _requireLogin(response) {
        // Reset attempts because if check login === can access to Web
        this._resetAttempts();
        this._resetCSRFAttempts();

        // Verify Required Login
        if (this._responseIsString(response)) {
            return response.data.includes("Autenticar");
        } else if (this._responseIsObject(response)) {
            return response.data.detail && response.data.detail.includes("credenciales");
        }
        return false;
    },
    _requirePrivilege(vm, privilege, power = 0) {
        const bypass = vm.$store.state.user(privilege, power);
        if (!bypass) {
            if (vm.$route.name !== 'error.forbidden') {
                vm.$router.push({name:'error.forbidden', params: {error_type: '403'}});
            }
        }
        return bypass;
    },
    _waitForCheckError(vm, e) {
        if (!this._connectionError(vm)) {
            if (e.response) {
                if (process.env.NODE_ENV !== 'production') {
                    console.log("RESPONSE", e.response);
                }
                switch (e.response.status) {
                    case 403:
                        if (e.response.data.error === 'CSRF token missing or incorrect.') {
                            return new Promise((resolve) => {
                                if (this.logging) {
                                    this.csrf_attempts++; // Incremental csrf attempt
                                    axios.get('/api/csrf/')
                                    .then(_ => resolve(true))
                                    .catch(_ => {
                                        if (vm.$route.name !== 'error.forbidden') {
                                            vm.$router.push({name:'error.forbidden', params: {
                                                error_type: '403',
                                                error_message: 'Error verificando el CSRF Token. Por favor, reenvie el ' +
                                                    'Formulario o vuelva a <a href="/super/">Inicio</a>!'
                                            }});
                                        }
                                        resolve(false);
                                    });
                                }
                            });
                        } else {
                            if (vm.$route.name !== 'error.forbidden') {
                                vm.$router.push({name:'error.forbidden', params: {error_type: '403'}});
                            }
                            return new Promise((resolve) => resolve(false));
                        }
                    case 404:
                        if (vm.$route.name !== 'error.404') {
                            vm.$router.push({name:'error.404'});
                        }
                        return new Promise((resolve) => resolve(false));
                    case 500:
                        if (vm.$route.name !== 'error.fatal') {
                            vm.$router.push({name:'error.fatal'});
                        }
                        return new Promise((resolve) => resolve(false));
                }
            }
            return new Promise((resolve) => resolve(true));
        }
        return new Promise((resolve) => resolve(false));
    },
    _create_request(vm, request, action, validation = true) {
            request.then(response => {
                if (!this._requireLogin(response)) {
                    // Check error
                    if (validation && !this._responseIsObject(response)) {
                        if (vm.$route.name !== 'error.fatal') {
                            vm.$router.push({name:'error.fatal'});
                        }
                    } else if (validation && response.data.detail) {
                        if (vm.$route.name !== 'error.fatal') {
                            vm.$router.push({name:'error.fatal'});
                        }
                    } else {
                        // Save in Global state user data
                        if (vm.$route.name === 'error.fatal') {
                            // Back to View before ErrorPage
                            vm.$router.back();
                        }

                        action(this, response);
                    }
                } else {
                    this.redirectToLogin();  // Redirect to Login Page
                }
            })
            .catch(e => {
                this._waitForCheckError(vm, e).then(r => {
                    if (r) {
                        if (vm.$route.name !== 'error.fatal') {
                            vm.$router.push({name:'error.fatal'});
                        }
                    }
                });
            });
    },

    // All Services
    getCurrentUser(vm) {
        this._create_request(vm, axios.get('/api/user/'), function (sender, response) {
            sender.logging = true;
            sender.getUserData(vm, response.data.id);
        }, !this.logging);
    },
    getUserData(vm, id) {
        this._create_request(vm, axios.get('/api/users/' + String(id) + '/'),
            function (sender, response) {
                response.data.id = id;
                vm.$store.commit('setUserData', response.data);
            });
    },

    getList_BasicMedium(vm) {
        // TODO: Removed default loading because using TableSkeletonLoading
        // vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/basic_medium/', {
                params: {
                    page: vm.page,
                    per_page: vm.per_page,
                    filter: vm.appliedFilter,
                    ordering: vm.ordering,
                }
            }), function (sender, response) {
                vm.data = response.data;
                vm.loading = false;

                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    get_BasicMedium(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/basic_medium/ ' + String(id) + '/'),
            function (sender, response) {
                vm.name = response.data.name;
                vm.inventory_number = response.data.inventory_number;
                vm.location = response.data.location;
                vm.responsible_id = response.data.owner.id;
                let value = response.data.owner.first_name + ' ' + response.data.owner.last_name;
                vm.responsible_name = (value.length === 0 || !value.trim()) ? response.data.owner.username : value;
                vm.is_enable = response.data.is_enable;

                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    remove_BasicMedium(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.delete('/api/basic_medium/' + String(id) + '/'),
            function (sender, response) {
                // Remove from list
                vm.data.items = vm.data.items.filter((value, _, __) => value.id !== id);
                vm.finish_delete();

                // Remove loading
                vm.$store.commit('removeLoading');
            }, false);
    },
    metadata_BasicMedium(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/basic_medium/metadata/'),
            function (sender, response) {
                vm.responsible = response.data.responsible;
                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    add_BasicMedium(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.post('/api/basic_medium/', {
                inventory_number: vm.inventory_number,
                name: vm.name,
                responsible: vm.responsible_id,
                location: vm.location,
                is_enable: vm.is_enable,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'basic_medium'}).then(r => {});
            });
    },
    edit_BasicMedium(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.put('/api/basic_medium/' + String(id) + '/', {
                inventory_number: vm.inventory_number,
                name: vm.name,
                responsible: vm.responsible_id,
                location: vm.location,
                is_enable: vm.is_enable,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'basic_medium.detail', params: {id:id}}).then(r => {});
            });
    },
};

export default Service;