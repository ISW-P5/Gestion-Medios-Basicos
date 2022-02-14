import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '../views/Dashboard';
import ErrorPage from "../views/errors/ErrorPage";
import TheContainer from "../containers/TheContainer";
import HelpPage from "../views/extra/HelpPage";
import BasicMediumPage from "../views/basic_medium/BasicMediumPage";
import AddBasicMediumPage from "../views/basic_medium/AddBasicMediumPage";

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Medios Basicos',
        component: TheContainer,
        redirect: '/',
        children: [
            {
                path: '',
                name: 'dashboard',
                meta: {label: 'Panel Principal'},
                component: Dashboard
            },
            {
                path: 'mediums/',
                name: 'basic_medium',
                meta: {label: 'Medios Basicos'},
                component: BasicMediumPage,
                children: [
                    {
                        path: 'add/',
                        name: 'basic_medium.add',
                        meta: {label: 'Añadir Medio Basico'},
                        component: AddBasicMediumPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'basic_medium.detail',
                        meta: {label: 'Ver Medio Basico'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'basic_medium.edit',
                        meta: {label: 'Editar Medio Basico'},
                        component: HelpPage
                    },
                ]
            },
            {
                path: 'movements/',
                name: 'movement_ticket',
                meta: {label: 'Vales de Movimiento'},
                component: HelpPage,
                children: [
                    {
                        path: 'add/',
                        name: 'movement_ticket.add',
                        meta: {label: 'Añadir Vale de Movimiento'},
                        component: HelpPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'movement_ticket.detail',
                        meta: {label: 'Ver Vale de Movimiento'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'movement_ticket.edit',
                        meta: {label: 'Editar Vale de Movimiento'},
                        component: HelpPage
                    },
                ]
            },
            {
                path: 'requests/',
                name: 'request_ticket',
                meta: {label: 'Vales de Solicitud'},
                component: HelpPage,
                children: [
                    {
                        path: 'add/',
                        name: 'request_ticket.add',
                        meta: {label: 'Añadir Vale de Solicitud'},
                        component: HelpPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'request_ticket.detail',
                        meta: {label: 'Ver Vale de Solicitud'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'request_ticket.edit',
                        meta: {label: 'Editar Vale de Solicitud'},
                        component: HelpPage
                    },
                ]
            },
            {
                path: 'certificate/',
                name: 'responsibility_certificate',
                meta: {label: 'Actas de Responsabilidad'},
                component: HelpPage,
                children: [
                    {
                        path: 'add/',
                        name: 'responsibility_certificate.add',
                        meta: {label: 'Añadir Acta de Responsabilidad'},
                        component: HelpPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'responsibility_certificate.detail',
                        meta: {label: 'Ver Acta de Responsabilidad'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'responsibility_certificate.edit',
                        meta: {label: 'Editar Acta de Responsabilidad'},
                        component: HelpPage
                    },
                ]
            },
            {
                path: 'users/',
                name: 'user',
                meta: {label: 'Usuarios'},
                component: HelpPage,
                children: [
                    {
                        path: 'add/',
                        name: 'user.add',
                        meta: {label: 'Añadir Usuario'},
                        component: HelpPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'user.detail',
                        meta: {label: 'Ver Usuario'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'user.edit',
                        meta: {label: 'Editar Usuario'},
                        component: HelpPage
                    },
                ]
            },
            {
                path: 'groups/',
                name: 'group',
                meta: {label: 'Grupos'},
                component: HelpPage,
                children: [
                    {
                        path: 'add/',
                        name: 'group.add',
                        meta: {label: 'Añadir Grupo'},
                        component: HelpPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'group.detail',
                        meta: {label: 'Ver Grupo'},
                        component: HelpPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'group.edit',
                        meta: {label: 'Editar Grupo'},
                        component: HelpPage
                    },
                ]
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
