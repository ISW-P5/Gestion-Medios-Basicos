export default {
    created() {
        // Remove loading
        if (this.$services.logging) {
            this.$store.commit('removeLoading');
        }
    }
};