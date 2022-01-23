function getTitle(vm) {
    const {title} = vm.$options;
    if (title) {
        return typeof title === 'function'
            ? title.call(vm)
            : title;
    }
}

function getPanelTitle(vm) {
    const {panel_title} = vm.$options;
    if (panel_title) {
        return typeof panel_title === 'function'
            ? panel_title.call(vm)
            : panel_title;
    }
}

export default {
    created() {
        const title = getTitle(this);
        const panel_title = getPanelTitle(this);
        if (title) {
            document.title = title;
            this.$store.state.panelTitle = panel_title || 'Panel Administrativo';
        }
    }
};