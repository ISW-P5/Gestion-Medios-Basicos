import {mapGetters} from "vuex";
import TableLoading from "../components/loading/TableLoading";
import validator from "../helpers/validator";
import privileges from "../helpers/utils";

export default {
    data() {
        return {
            privileges,
            loading: true,
            // Deleting
            confirm_delete: false,
            delete_data: 0,
            // Data & Paginator & Ordering
            data: 0,
            page: 1,
            per_page: 50,
            ordering: {
                asc: true,
                column: 'id',
            },
            // Filters
            filter: "",
            appliedFilter: "",
        }
    },
    components: {
        TableLoading
    },
    watch:{
        'page': function (page, _) {
            this.updatePage(page);
        },
        'ordering': {
            handler: function (sorter, _) {
                this.updateOrdering(sorter);
            },
            deep: true
        },
        '$route.query.page': function (page, _) {
            this.updatePage(page);
        },
        '$route.query.per_page': function (per_page, _) {
            this.updatePerPage(per_page);
        },
    },
    methods: {
        // MetaData in Table (filter, page, per_page and delete alert)
        applyFilter(filter) {
            const query = Object.assign({}, this.$route.query);
            if ((validator.isNull(filter) || validator.isEmpty(filter)) && 'filter' in query) {
                delete query.filter;
            } else {
                query.filter = filter;
            }
            this.$router.push({query}).catch(_ => {});

            this.appliedFilter = filter;
            this.filter = filter;
            this.get_queryset();
        },
        updatePerPage(value) {
            const query = Object.assign({}, this.$route.query);
            if (value === 50 && 'per_page' in query) {
                delete query.per_page;
            } else {
                query.per_page = value;
            }
            this.$router.push({query}).catch(_ => {});

            if (!validator.isNull(value)) {
                this.per_page = parseInt(value);
            }
            if ((this.data.total / value) < this.page) {
                // Restart overpass paginator
                this.page = 1;
            } else {
                this.get_queryset();
            }
        },
        updatePage(value) {
            const query = Object.assign({}, this.$route.query);
            if (value === 1 && 'page' in query) {
                delete query.page;
            } else {
                query.page = value;
            }
            this.$router.push({query}).catch(_ => {});

            if (!validator.isNull(value)) {
                this.page = parseInt(value);
            }

            this.get_queryset();
        },
        updateOrdering(value) {
            if (!validator.isNull(value) && validator.isObject(value)) {
                this.ordering = value;
            }

            this.get_queryset();
        },
        set_delete(item) {
            this.delete_data = item;
            this.confirm_delete = true;
        },
        finish_delete() {
            this.confirm_delete = false;
            this.delete_data = 0;
        },
        ...mapGetters(['privilege_required'])
    },
    created() {
        if (this.$route.name === this.route) {
            // Set page by route query
            this.per_page = this.$route.query.per_page || 50;
            this.page = this.$route.query.page || 1;
            const filter = this.$route.query.filter || '';
            this.filter = filter;
            this.appliedFilter = filter;

            this.get_queryset();
        }
    }
};