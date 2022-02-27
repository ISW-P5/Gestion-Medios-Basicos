<template>
    <CContainer class="d-flex align-items-center mt-5">
        <CRow class="w-100 justify-content-center">
            <CCol md="6">
                <div class="clearfix" v-if="error_type !== '000'">
                    <h1 class="float-left display-3 mr-4">{{ error_type }}</h1>
                    <h4 class="pt-3" v-html="error_title">{{ error_title }}</h4>
                    <p class="text-muted" v-html="error_message">{{ error_message }}</p>
                </div>
                <div class="clearfix" v-else>
                    <div class="float-left display-3 mr-4">
                        <CIcon width="6rem" name="cil-link-broken" />
                    </div>
                    <h4 class="pt-3">¡Error de Conexión!</h4>
                    <p class="text-muted">Ha ocurrido un error de conexión con el Servidor. Inténte acceder más tarde. <CLink :to="{name: back}">Reintentar</CLink></p>
                </div>
            </CCol>
        </CRow>
    </CContainer>
</template>

<script>
import loading from "../../mixins/loading";

export default {
    name: 'ErrorPage',
    title: 'Admin | Error',
    mixins: [loading],
    props: {
        error_type: {
            type: String,
            default: () => '404',
        },
        error_title: {
            type: String,
            default() {
                switch (this.error_type) {
                    case "404":
                        return '¡Página no encontrada!';
                    case "500":
                        return 'Houston, tenemos un problema!';
                    case "401":
                        return '¡Sin autorización!';
                    case "403":
                        return '¡Permisos Insuficientes!';
                    case "ERROR":
                        return '¡Error FATAL!';
                    default:
                        return 'Error desconocido';
                }
            }
        },
        error_message: {
            type: String,
            default() {
                switch (this.error_type) {
                    case "404":
                        return 'No se ha localizado la URL solicitada en este servidor. ' +
                            'Si usted ha introducido la URL manualmente, por favor revise su ortografía e inténtelo de nuevo.';
                    case "500":
                        return 'Hemos tenido un error interno en el servidor. Por favor, revise los registros.';
                    case "401":
                        return 'Usted no posee los permisos necesarios para acceder a esta url. Por favor, intente autenticarse!';
                    case "403":
                        return 'Usted no posee los permisos suficientes para utilizar esta característica o tus permisos' +
                            ' no han sido actualizados. Por favor, recargue la página para actualizar sus privilegios o ' +
                            'vuelva a <a href="/super/">Inicio</a>!';
                    case "ERROR":
                        return 'Ha ocurrido un error fatal en el Servidor. No se ha podido cargar los datos de tu sesión.' +
                            ' Inténte acceder más tarde. <a href="/super/">Volver a inicio</a>';
                    default:
                        return 'Ha ocurrido un error desconocido en el Servidor.';
                }
            }
        },
    },
    data() {
        return {
            back: 'dashboard'  // Default url (Dashboard)
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            // Save from url before enter to this route
            if (from.name && !from.name.startsWith('error')) {
                vm.back = from.name;
            }
        })
    },
    created() {
        if (this.$route.name === 'error.fatal') {
            this.$services.getCurrentUser(this);
        }
    }
};
</script>
