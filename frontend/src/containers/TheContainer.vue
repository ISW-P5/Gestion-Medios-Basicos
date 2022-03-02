<template>
    <div class="c-app">
        <TheSidebar/>
        <CWrapper>
            <TheHeader/>
            <div class="c-body">
                <main class="c-main">
                    <CContainer fluid>
                        <transition name="fade" mode="out-in">
                            <div>
                                <CToaster :autohide="5000">
                                    <template v-for="toast in $store.state.activeToasts">
                                        <CToast :key="'toast' + toast" :show="true" :color="$store.state.typeToasts"
                                            v-html="$store.state.textToasts">
                                            {{ $store.state.textToasts }}
                                        </CToast>
                                    </template>
                                </CToaster>

                                <router-view :key="$route.path"></router-view>
                                <CElementCover v-if="$store.state.loading" :opacity="0.8">
                                    <h1 class="d-inline">Cargando... </h1><CSpinner size="5xl" color="success"/>
                                </CElementCover>
                            </div>
                        </transition>
                    </CContainer>
                </main>
            </div>
            <TheFooter/>
        </CWrapper>
    </div>
</template>

<script>
import TheSidebar from './TheSidebar';
import TheHeader from './TheHeader';
import TheFooter from './TheFooter';

export default {
    name: 'TheContainer',
    components: {
        TheSidebar,
        TheHeader,
        TheFooter
    }
};
</script>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.3s;
    }

    .fade-enter,
    .fade-leave-to {
        opacity: 0;
    }
</style>
