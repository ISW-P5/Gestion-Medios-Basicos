import Vue from 'vue';
import Vuex from 'vuex';
import {getSidebar} from "../helpers/menu";

Vue.use(Vuex);

const state = {
    sidebar: [],
    sidebarShow: 'responsive',
    sidebarMinimize: false,
    version: '1.0.0.0',
    panelTitle: 'Panel Administrativo',
    user: {
        username: 'Unknown'
    }
};

const mutations = {
    toggleSidebarDesktop(state) {
        const sidebarOpened = [true, 'responsive'].includes(state.sidebarShow);
        state.sidebarShow = sidebarOpened ? false : 'responsive';
    },
    toggleSidebarMobile(state) {
        const sidebarClosed = [false, 'responsive'].includes(state.sidebarShow);
        state.sidebarShow = sidebarClosed ? true : 'responsive';
    },
    set(state, [variable, value]) {
        state[variable] = value;
    },
    updateSidebar(state, sidebar) {
        state.sidebar = sidebar;
    },
    setUserData(state, data, update_sidebar = true) {
        state.user = data;
        if (update_sidebar) {
            state.sidebar = getSidebar(state.user.permissions);
        }
    },
};

const getters = {};

const actions = {};

export default new Vuex.Store({
    state,
    mutations,
    actions,
    modules: {},
    getters
});
