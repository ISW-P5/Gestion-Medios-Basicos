import Vue from 'vue';
import VueRouter from 'vue-router';
import TheContainer from "../containers/TheContainer";
import Dashboard from '../views/Dashboard';
import ErrorPage from "../views/errors/ErrorPage";
import HelpPage from "../views/extra/HelpPage";
import BasicMediumPage from "../views/basic_medium/BasicMediumPage";
import DetailBasicMediumPage from "../views/basic_medium/DetailBasicMediumPage";
import ResponsibilityCertificatePage from "../views/responsibility_certificate/ResponsibilityCertificatePage";
import DetailResponsibilityCertificatePage from "../views/responsibility_certificate/DetailResponsibilityCertificatePage";
import UserPage from "../views/users/UserPage";
import DetailUserPage from "../views/users/DetailUserPage";
import RequestTicketPage from "../views/request_ticket/RequestTicketPage";
import DetailRequestTicketPage from "../views/request_ticket/DetailRequestTicketPage";
import MovementTicketPage from "../views/movement_ticket/MovementTicketPage";
import DetailMovementTicketPage from "../views/movement_ticket/DetailMovementTicketPage";

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
                        meta: {label: 'Añadir'},
                        component: DetailBasicMediumPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'basic_medium.detail',
                        meta: {label: 'Ver'},
                        component: DetailBasicMediumPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'basic_medium.edit',
                        meta: {label: 'Editar'},
                        component: DetailBasicMediumPage
                    },
                ]
            },
            {
                path: 'movements/',
                name: 'movement_ticket',
                meta: {label: 'Vales de Movimiento'},
                component: MovementTicketPage,
                children: [
                    {
                        path: 'add/',
                        name: 'movement_ticket.add',
                        meta: {label: 'Añadir'},
                        component: DetailMovementTicketPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'movement_ticket.detail',
                        meta: {label: 'Ver'},
                        component: DetailMovementTicketPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'movement_ticket.edit',
                        meta: {label: 'Editar'},
                        component: DetailMovementTicketPage
                    },
                ]
            },
            {
                path: 'requests/',
                name: 'request_ticket',
                meta: {label: 'Vales de Solicitud'},
                component: RequestTicketPage,
                children: [
                    {
                        path: 'add/',
                        name: 'request_ticket.add',
                        meta: {label: 'Añadir'},
                        component: DetailRequestTicketPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'request_ticket.detail',
                        meta: {label: 'Ver'},
                        component: DetailRequestTicketPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'request_ticket.edit',
                        meta: {label: 'Editar'},
                        component: DetailRequestTicketPage
                    },
                ]
            },
            {
                path: 'certificate/',
                name: 'responsibility_certificate',
                meta: {label: 'Actas de Responsabilidad'},
                component: ResponsibilityCertificatePage,
                children: [
                    {
                        path: 'add/',
                        name: 'responsibility_certificate.add',
                        meta: {label: 'Añadir'},
                        component: DetailResponsibilityCertificatePage
                    },
                    {
                        path: ':id/detail/',
                        name: 'responsibility_certificate.detail',
                        meta: {label: 'Ver'},
                        component: DetailResponsibilityCertificatePage
                    },
                    {
                        path: ':id/edit/',
                        name: 'responsibility_certificate.edit',
                        meta: {label: 'Editar'},
                        component: DetailResponsibilityCertificatePage
                    },
                ]
            },
            {
                path: 'users/',
                name: 'user',
                meta: {label: 'Usuarios'},
                component: UserPage,
                children: [
                    {
                        path: 'add/',
                        name: 'user.add',
                        meta: {label: 'Añadir'},
                        component: DetailUserPage
                    },
                    {
                        path: ':id/detail/',
                        name: 'user.detail',
                        meta: {label: 'Ver'},
                        component: DetailUserPage
                    },
                    {
                        path: ':id/edit/',
                        name: 'user.edit',
                        meta: {label: 'Editar'},
                        component: DetailUserPage
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
