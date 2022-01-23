<template>
    <CCard>
        <CCardHeader>
            <strong>Bienvenida</strong>
        </CCardHeader>
        <CCardBody>
          Bienvenido al Panel Administrativo del Sistema de Gestion de Medios Basicos de la Facultad 2.
        </CCardBody>
    </CCard>
</template>

<script>

export default {
    name: "Dashboard",
    title: 'Admin | Dashboard',
    components: {},
    data() {
        return {
            system_information: [],
            drives: [],
        }
    },
    methods: {

    },
};
</script>

<style scoped>

</style>