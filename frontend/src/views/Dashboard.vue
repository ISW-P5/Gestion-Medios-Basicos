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
import loading from "../mixins/loading";

export default {
    name: "Dashboard",
    title: 'Admin | Dashboard',
    mixins: [loading]
};
</script>