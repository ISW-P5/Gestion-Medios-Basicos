import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

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

    getList_Responsible(vm, all=false) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/responsible/', {
                params: {all:all}
            }),
            function (sender, response) {
                vm.responsible = response.data.responsible;
                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    getList_MediumsCertificate(vm, excluded = -1) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/mediums_certificate/', {
                params: {
                    excluded_id: excluded
                }
            }),
            function (sender, response) {
                vm.basic_medium = response.data.basic_medium;
                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    getList_Mediums(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/mediums/'),
            function (sender, response) {
                vm.basic_medium = response.data.basic_medium;
                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    getList_Roles(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/roles/'),
            function (sender, response) {
                vm.groups = response.data.groups;
                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },

    // List, Detail, Remove, Add and Edit Basic Medium
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
    detail_BasicMedium(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/basic_medium/' + String(id) + '/'),
            function (sender, response) {
                vm.id = response.data.id;
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

    // List, Detail, Remove, Add and Edit Responsibility Certificate
    getList_ResponsibilityCertificate(vm) {
        this._create_request(vm, axios.get('/api/responsibility_certificate/', {
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
    detail_ResponsibilityCertificate(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/responsibility_certificate/' + String(id) + '/'),
            function (sender, response) {
                vm.id = response.data.id;
                vm.identity_card = response.data.identity_card;
                vm.basic_medium_id = response.data.medium.id;
                vm.basic_medium_name = response.data.medium.name;
                vm.responsible_id = response.data.owner.id;
                let value = response.data.owner.first_name + ' ' + response.data.owner.last_name;
                vm.responsible_name = (value.length === 0 || !value.trim()) ? response.data.owner.username : value;
                vm.datetime = response.data.datetime;

                sender.getList_MediumsCertificate(vm, response.data.medium.id);

                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    remove_ResponsibilityCertificate(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.delete('/api/responsibility_certificate/' + String(id) + '/'),
            function (sender, response) {
                // Remove from list
                vm.data.items = vm.data.items.filter((value, _, __) => value.id !== id);
                vm.finish_delete();

                // Remove loading
                vm.$store.commit('removeLoading');
            }, false);
    },
    add_ResponsibilityCertificate(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.post('/api/responsibility_certificate/', {
                identity_card: vm.identity_card,
                basic_medium: vm.basic_medium_id,
                responsible: vm.responsible_id,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'responsibility_certificate'}).then(r => {});
            });
    },
    edit_ResponsibilityCertificate(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.put('/api/responsibility_certificate/' + String(id) + '/', {
                identity_card: vm.identity_card,
                basic_medium: vm.basic_medium_id,
                responsible: vm.responsible_id,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'responsibility_certificate.detail', params: {id:id}}).then(r => {});
            });
    },

    // List, Detail, Remove, Add and Edit User
    getList_User(vm) {
        this._create_request(vm, axios.get('/api/users/', {
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
    detail_User(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.get('/api/users/' + String(id) + '/'),
            function (sender, response) {
                vm.id = response.data.id;
                vm.username = response.data.username;
                vm.email = response.data.email;
                vm.first_name = response.data.first_name;
                vm.last_name = response.data.last_name;
                vm.group_id = response.data.role_id;
                vm.group_name = response.data.role;
                vm.is_staff = response.data.is_staff;

                // Remove loading
                vm.$store.commit('removeLoading');
            });
    },
    remove_User(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.delete('/api/users/' + String(id) + '/'),
            function (sender, response) {
                // Remove from list
                vm.data.items = vm.data.items.filter((value, _, __) => value.id !== id);
                vm.finish_delete();

                // Remove loading
                vm.$store.commit('removeLoading');
            }, false);
    },
    add_User(vm) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.post('/api/users/', {
                identity_card: vm.identity_card,
                basic_medium: vm.basic_medium_id,
                responsible: vm.responsible_id,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'responsibility_certificate'}).then(r => {});
            });
    },
    edit_User(vm, id) {
        vm.$store.commit('setLoading');
        this._create_request(vm, axios.put('/api/users/' + String(id) + '/', {
                identity_card: vm.identity_card,
                basic_medium: vm.basic_medium_id,
                responsible: vm.responsible_id,
            }),
            function (sender, response) {
                // Remove loading
                vm.$store.commit('removeLoading');

                // Redirect to List Warnings
                vm.$router.push({name: 'responsibility_certificate.detail', params: {id:id}}).then(r => {});
            });
    },

    // List, Detail, Remove, Add and Edit Movement Ticket

    // List, Detail, Remove, Add and Edit Request Ticket
};

export default Service;