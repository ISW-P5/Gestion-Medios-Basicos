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
            // Forms Data
            wasValidated: false,
            horizontal: { label:'col-md-2', input:'col-md-10' },
            fields,
        }
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
        ...mapGetters(['privilege_required'])
    },
    created() {
        const title = 'Admin | ' + this.get_title() + ' Medio Basico';
        const panel_title = this.get_title() + ' Medio Basico';
        if (title) {
            document.title = title;
            this.$store.state.panelTitle = panel_title || 'Panel Administrativo';
        }
    }
};