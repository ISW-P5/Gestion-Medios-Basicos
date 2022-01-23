<template>
    <CFooter :fixed="false">
        <div>
            <span>Medios Basicos v{{ version }}</span>
            <span class="ml-1">&copy; {{new Date().getFullYear()}}</span>
        </div>
        <div class="mfs-auto">
            <span class="mr-1">Creado por</span>
            <a href="https://github.com/ISW-P5" target="_blank">F2401</a>
        </div>
    </CFooter>
</template>

<script>
import {mapState} from "vuex";

export default {
    name: 'TheFooter',
    computed: {
        ...mapState(['version'])
    }
};
</script>

<style scoped>
    .c-footer {
        background: #d8dbe0;
    }
</style>