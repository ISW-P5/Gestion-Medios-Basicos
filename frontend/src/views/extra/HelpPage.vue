<template>
    <CCard>
        <CCardHeader>
            <CIcon name="cil-spreadsheet" />
            Ayuda
        </CCardHeader>
        <CCardBody>
         <p>Esta sistema se desarrollo con el fin de crear una aplicación que que le dé solución al problema
            de informatizar el proceso de control y organización de los medios básicos del Vicedecanato de
            Administración de la Facultad 2.</p>
        </CCardBody>
    </CCard>
</template>

<script>
import loading from "../../mixins/loading";

export default {
    name: "HelpPage",
    title: 'Admin | Ayuda',
    panel_title: 'Ayuda',
    mixins: [loading],
}
</script>

<style scoped>

</style>