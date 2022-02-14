<template>
    <CCard>
        <CCardHeader>
            <CIcon name="cil-spreadsheet" />
            Ayuda
        </CCardHeader>
        <CCardBody>
          Contenido de Ayuda
        </CCardBody>
    </CCard>
</template>

<script>
import loading from "../../mixins/loading";

export default {
    name: "HelpPage",
    title: 'Admin | Changelog',
    panel_title: 'Ayuda',
    mixins: [loading],
}
</script>

<style scoped>

</style>