import axios from 'axios';

axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";

// TODO: Create and Migrate all API Methods to Async/Await
const service = {
    // Attempts
    attempts: 0,
    csrf_attempts: 0,
    // Timer for try again
    timer: 0,
    time_wait: 5000,
    stopped: false,
    // Logging
    logging: false,
    logging_promise: 0,
    // Control & Internals
    resetRequest() {
        this.destroyRequest();
        this.stopped = false;
    },
    destroyRequest() {
        if (this.timer && !this.stopped) {
            this.stopped = true;
            clearTimeout(this.timer);
            this.timer = 0;
        }
    },
    redirectToLogin() {
        window.location.replace('http://' + window.location.host + '/login/');
    },
    _connectionError(vm) {
        if (this.csrf_attempts > 2) {   // Max 3 attempts
            this.resetRequest();
            if (vm.$route.name !== 'error.forbidden') {
                vm.$router.push({name:'error.forbidden', params: {
                    error_type: '403',
                    error_message: 'Error verificando el CSRF Token. Por favor, reenvie el Formulario o ' +
                        'vuelva a <a href="/super/">Inicio</a>!'
                }});
            }
            return true;
        }
        if (this.attempts > 4) {        // Max 5 attempts
            this.resetRequest();
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
        return typeof response.data === 'string' && response.data.includes("auth_username") && response.data.includes("auth_password");
    },
    _requirePrivilege(vm, privilege = 0, power = 1) {
        const bypass = vm.$store.getters.privilege_required(privilege, power);
        if (!bypass) {
            if (vm.$route.name !== 'error.forbidden') {
                vm.$router.push({name:'error.forbidden', params: {error_type: '403'}});
            }
        }
        return bypass;
    },
    _waitForLogging(vm) {
        if (this.logging) {
            return (new Promise((resolve) => resolve(true)));
        } else if (!this.logging_promise) {
            this.logging_promise = (new Promise((resolve) => this.getCurrentUserPromise(vm, resolve)));
        }
        return this.logging_promise;
    },
    _waitForCheckError(vm, e) {
        if (!this._connectionError(vm)) {
            if (e.response) {
                switch (e.response.status) {
                    case 403:
                        if (e.response.data.error === 'CSRF token missing or incorrect.') {
                            return new Promise((resolve) => {
                                if (this.logging) {
                                    this.csrf_attempts++; // Incremental csrf attempt
                                    axios.get('/super/api/csrf')
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
                            this.resetRequest();
                            if (vm.$route.name !== 'error.forbidden') {
                                vm.$router.push({name:'error.forbidden', params: {error_type: '403'}});
                            }
                            return new Promise((resolve) => resolve(false));
                        }
                    case 404:
                        this.resetRequest();
                        if (vm.$route.name !== 'error.404') {
                            vm.$router.push({name:'error.404'});
                        }
                        return new Promise((resolve) => resolve(false));
                    case 500:
                        this.resetRequest();
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
    _responseIsObject: (r) => typeof r.data === 'object',
    _responseIsString: (r) => typeof r.data === 'string',
    // Utils
    getPage: (paginator, page) => (paginator[paginator.length - 1] < page) ? paginator[paginator.length - 1] : page,
    // All Services
    getCurrentUserPromise(vm, resolve) {
        this.resetRequest();
        if (!this.logging) {
            axios.get('/super/api/current_session')
            .then(response => {
                if (!this._requireLogin(response)) {
                    // Check not Stopped
                    if (!this.stopped) {
                        // Check error
                        if (!this._responseIsObject(response)) {
                            if (vm.$route.name !== 'error.fatal') {
                                vm.$router.push({name:'error.fatal'});
                            }
                            this.logging_promise = 0;
                            resolve(false);
                        } else if (response.data.error) {
                            if (vm.$route.name !== 'error.fatal') {
                                vm.$router.push({name:'error.fatal'});
                            }
                            this.logging_promise = 0;
                            resolve(false);
                        } else {
                            // Save in Global state user data
                            if (vm.$route.name === 'error.fatal') {
                                // Back to View before ErrorPage
                                vm.$router.back();
                            }
                            this.logging = true;
                            vm.$store.commit('setUserData', response.data);

                            this.logging_promise = 0;
                            resolve(true);
                        }
                    } else {
                        this.logging_promise = 0;
                        resolve(false);
                    }
                } else {
                    this.redirectToLogin();  // Redirect to Login Page
                    this.logging_promise = 0;
                    resolve(false);
                }
            })
            .catch(a => {
                if (vm.$route.name !== 'error.fatal') {
                    vm.$router.push({name:'error.fatal'});
                }
                this.logging_promise = 0;
                resolve(false);
            });
        } else {
            this.logging_promise = 0;
            resolve(true);
        }
    },
    getCurrentUser(vm) {
        this.resetRequest();
        if (!this.logging) {
            axios.get('/super/api/current_session')
            .then(response => {
                if (!this._requireLogin(response)) {
                    // Check not Stopped
                    if (!this.stopped) {
                        // Check error
                        if (!this._responseIsObject(response)) {
                            if (vm.$route.name !== 'error.fatal') {
                                vm.$router.push({name:'error.fatal'});
                            }
                            this.timer = setTimeout(() => this.getCurrentUser(vm), this.time_wait);
                        } else if (response.data.error) {
                            if (vm.$route.name !== 'error.fatal') {
                                vm.$router.push({name:'error.fatal'});
                            }
                            this.timer = setTimeout(() => this.getCurrentUser(vm), this.time_wait);
                        } else {
                            // Save in Global state user data
                            if (vm.$route.name === 'error.fatal') {
                                // Back to View before ErrorPage
                                vm.$router.back();
                            }
                            this.logging = true;
                            vm.$store.commit('setUserData', response.data);
                        }
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
                        this.timer = setTimeout(() => this.getCurrentUser(vm), this.time_wait);
                    }
                });
            });
        }
    },
};

export default service;