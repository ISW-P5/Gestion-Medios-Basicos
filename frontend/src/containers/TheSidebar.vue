<template>
    <CSidebar
            fixed
            :minimize="sidebarMinimize"
            :show="sidebarShow"
            @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
    >
        <CSidebarBrand class="d-md-down-none" to="/">
            <img src="../../public/apple-touch-icon-57.webp" alt="Logo" class="brand-image" style="opacity: .8">
            <div class="c-sidebar-brand-full">
                <span class="pl-2 font-xl">Medios Basicos</span>
            </div>
        </CSidebarBrand>

        <CRenderFunction flat :content-to-render="sidebar"/>
    </CSidebar>
</template>

<script>
import {mapState} from "vuex";

export default {
    name: 'TheSidebar',
    computed: {
        ...mapState(['sidebarMinimize', 'sidebarShow', 'sidebar'])
    }
};
</script>

<style scoped>
    .brand-image {
        width: 32px;
    }
</style>