import 'core-js/stable';
import Vue from 'vue';
import App from './App';
import CoreuiVue from '@coreui/vue';
import {iconsSet as icons} from './assets/icons/icons.js';
import moment from 'moment';
import titleMixin from './mixins/title';
import router from './helpers/routes';
import store from './helpers/store';
import service from "./helpers/service";

Vue.config.performance = true;
Vue.use(CoreuiVue);
Vue.mixin(titleMixin);
Vue.filter('formatDate', (value) =>
    (!value) ? '' : moment(value).locale("es").format('DD MMMM YYYY, h:mm:ss a'));
Vue.prototype.$services = service;  // Loaded Services

new Vue({
    el: '#app',
    router,
    store,
    icons,
    template: '<App/>',
    components: {
        App
    }
});
