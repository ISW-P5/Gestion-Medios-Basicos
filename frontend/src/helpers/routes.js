import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../views/Dashboard';
import ErrorPage from "../views/errors/ErrorPage";
import TheContainer from "../containers/TheContainer";
import HelpPage from "../views/extra/HelpPage";

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Medios Basicos',
        component: TheContainer,
        children: [
            {
                path: '',
                name: 'dashboard',
                meta: {label: 'Panel Principal'},
                component: Dashboard
            },
            {
                path: 'help/',
                name: 'help',
                meta: {label: 'Ayuda'},
                component: HelpPage
            },
        ]
    },
    {
        name: 'home',
        meta: {label: 'Home'},
        path: "/redirecting",
        redirect: (_) => {
            window.location.replace('https://' + window.location.host);
            return '/redirecting';
        },
    },
    {
        path: "/error",
        component: TheContainer,
        redirect: '/error/',
        children: [
            {
                path: '/',
                name: 'error.fatal',
                meta: {label: 'Error Fatal'},
                component: ErrorPage,
                props: {
                    error_type: 'ERROR'
                }
            },
            {
                path: '/connection/',
                name: 'error.connection',
                meta: {label: 'Error de Conexión'},
                component: ErrorPage,
                props: {
                    error_type: '000'
                }
            },
            {
                path: '/forbidden/',
                name: 'error.forbidden',
                meta: {label: 'Permiso Insuficiente'},
                component: ErrorPage,
                props: true
            },
        ]
    },
    {
        path: "*",
        component: TheContainer,
        children: [
            {
                path: '*',
                name: 'error.404',
                meta: {label: 'Error 404'},
                component: ErrorPage,
                props: {
                    error_type: '404'
                }
            },
        ]
    }
];

const router = new VueRouter({
    mode: 'hash',  // history
    linkActiveClass: 'active',
    scrollBehavior: () => ({y: 0}),
    base: '/admin/',
    routes
});

export default router;
