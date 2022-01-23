<template>
    <CHeader fixed with-subheader light>
        <CToggler
                in-header
                class="ml-3 d-lg-none"
                @click="$store.commit('toggleSidebarMobile')"
        />
        <CToggler
                in-header
                class="ml-3 d-md-down-none"
                @click="$store.commit('set', ['sidebarMinimize', !sidebarMinimize])"
        />
        <CHeaderBrand class="mx-auto d-lg-none" to="/">
            <img src="../../public/apple-touch-icon-57.webp" height="48" alt="Logo" class="brand-image"
                 style="opacity: .8">
            <div class="c-sidebar-brand-full">
                <span class="pl-2 font-xl">Medios Basicos</span>
            </div>
        </CHeaderBrand>
        <CHeaderNav class="d-md-down-none mr-auto">
            <CHeaderNavItem class="px-3">
                {{ panelTitle }}
            </CHeaderNavItem>
        </CHeaderNav>
        <CHeaderNav class="mr-4">
            <TheHeaderDropdownAccnt/>
        </CHeaderNav>
        <CSubheader class="px-3">
            <CBreadcrumbRouter class="border-0 mb-0"/>
        </CSubheader>
    </CHeader>
</template>

<script>
import {mapState} from "vuex";
import TheHeaderDropdownAccnt from './TheHeaderDropdownAccnt';

export default {
    name: 'TheHeader',
    components: {
        TheHeaderDropdownAccnt
    },
    computed: {
        ...mapState(['panelTitle', 'sidebarMinimize'])
    }
};
</script>
