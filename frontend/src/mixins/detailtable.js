import {mapGetters} from "vuex";
import privileges from "../helpers/utils";

const fields = [
    { key: 'p'},
    { key: 'v'},
];

export default {
    data() {
        return {
            privileges,
            // Deleting
            confirm_delete: false,
            // Forms Data
            wasValidated: false,
            horizontal: { label:'col-md-2', input:'col-md-10' },
            fields,
        }
    },
    computed: {
        ...mapGetters(['privilege_required'])
    },
    methods: {
        add(f) {
            f.preventDefault();
            if (this.is_valid()) {
                this.add_queryset();
            } else {
                this.wasValidated = true;
            }
        },
        edit(f) {
            f.preventDefault();
            if (this.is_valid()) {
                this.edit_queryset();
            } else {
                this.wasValidated = true;
            }
        },
        get_title() {
            let value = this.$route.name.replace(this.route + '.', '');
            switch (value) {
                case 'add':
                    return 'Añadir';
                case 'detail':
                    return 'Ver';
                case 'edit':
                    return 'Editar';
            }
            return '';
        },
        set_delete() {
            this.confirm_delete = true;
        },
        finish_delete() {
            this.confirm_delete = false;
        },
    },
    created() {
        const title = 'Admin | ' + this.get_title() + ' ' + this.$options.panel_title;
        const panel_title = this.get_title() + ' ' + this.$options.panel_title;
        if (title) {
            document.title = title;
            this.$store.state.panelTitle = panel_title || 'Panel Administrativo';
        }

        if (this.$route.name !== (this.route + '.add')) {
            this.get_queryset();
        }
        if (this.$route.name === (this.route + '.add') || this.$route.name === (this.route + '.edit')) {
            this.metadata_queryset();
        }
    }
};