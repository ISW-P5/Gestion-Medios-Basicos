<template>
    <div v-if="this.$route.name === route">
        <CCard>
            <CCardHeader>
                <CIcon name="cil-address-book"/>
                Listado de Actas de Responsabilidad<span v-model="data.count" v-if="data"> ({{ data.count }})</span>
                <div class="card-header-actions" v-if="privilege_required(privilege, privileges.ADD)">
                    <CButton color="success" size="sm" :to="{ name: 'responsibility_certificate.add' }"
                             :disabled="!(data)">
                        <CIcon name="cil-plus" /> Agregar
                    </CButton>
                </div>
            </CCardHeader>
            <!-- Loading Table -->
            <CCardBody v-if="!data" class="p-3">
                <table-loading :rows="25" :columns="fields.length" />
            </CCardBody>
            <!-- Data Table -->
            <CCardBody v-else>
                <CDataTable
                    :items="items"
                    :fields="fields"
                    v-model:tableFilterValue="appliedFilter"
                    @update:table-filter-value="(v) => this.filter = v"
                    v-model:sorterValue="ordering"
                    @update:sorter-value="(v) => this.ordering = v"
                    :noItemsView="{
                        noResults: 'No hay resultados',
                        noItems: 'No hay elementos'
                    }"
                    :tableFilter="{
                        label: 'Filtrar:',
                        placeholder: 'informacion a buscar ...'
                    }"
                    :itemsPerPageSelect="{
                        label: 'Cantidad por página:',
                        values: [25, 50, 75, 100, 150, 200]
                    }"
                    :items-per-page="per_page"
                    @pagination-change="updatePerPage"

                    sorter
                    hover
                    table-filter
                    footer
                    v-model:loading="loading"
                >
                    <!-- Table Filter -->
                    <template #cleaner="{clean}">
                        <CButton class="ml-2" color="success" size="sm" @click="applyFilter(filter)">
                            <CIcon name="cil-filter" />
                        </CButton>
                        <CButton class="ml-1" color="danger" size="sm" v-if="appliedFilter"
                                 @click="() => { applyFilter(''); clean(); }">
                            <CIcon name="cil-filter-x" />
                        </CButton>
                    </template>

                    <!-- Table Custom Fields -->
                    <template #medium="{item}">
                        <td v-if="privilege_required(privilege, privileges.VIEW)">
                            <CLink :to="{name: 'responsibility_certificate.detail', params: {id:item.id}}">
                                {{ item.medium }}
                            </CLink>
                        </td>
                        <td v-else>{{ item.medium }}</td>
                    </template>
                    <template #datetime="{item}">
                        <td>
                            {{ item.datetime | formatDate }}
                        </td>
                    </template>
                    <template #actions="{item}">
                        <td class="py-2">
                            <CButton color="warning" size="sm" class="mr-2 text-white"
                                     v-if="privilege_required(privilege, privileges.MODIFY)"
                                     :to="{name: 'responsibility_certificate.edit', params: {id:item.id}}">
                                <CIcon name="cil-pencil" /> Editar
                            </CButton>
                            <CButton color="danger" square size="sm"
                                     v-if="privilege_required(privilege, privileges.DELETE)"
                                     @click="set_delete(item)">
                                <CIcon name="cil-trash" />
                                Eliminar
                            </CButton>
                            <CButton color="success" size="sm" class="text-white"
                                     v-if="!privilege_required(privilege, privileges.MODIFY) &&
                                           !privilege_required(privilege, privileges.DELETE)"
                                     :to="{name: 'responsibility_certificate.detail', params: {id:item.id}}">
                                <CIcon name="cil-file" /> Ver
                            </CButton>
                        </td>
                    </template>
                </CDataTable>

                <!-- Table Paginator -->
                <CPagination v-if="data.paginator && data.paginator.length > 1" size="sm" align="center"
                        :active-page.sync="page" :pages="data.paginator.length" />
            </CCardBody>
        </CCard>
        <!-- Delete Confirmation Modal -->
        <CModal :centered="true" :scrollable="false" title="Eliminar!" size="sm" color="warning"
                :show.sync="confirm_delete" v-if="delete_data">
            ¿Estas seguro de que quieres eliminar el acta de responsabilidad
            "({{ delete_data.medium + ', ' + delete_data.owner }})"?
            <template #footer>
                <CButton color="default" size="sm" @click="finish_delete()">Cancelar</CButton>
                <CButton color="danger" size="sm" @click="remove()">¡Eliminar!</CButton>
            </template>
        </CModal>
    </div>
    <!-- Route for Add/Edit Page -->
    <router-view v-else></router-view>
</template>

<script>
import validator from "../../helpers/validator";
import loading from "../../mixins/loading";
import table_list from "../../mixins/tablelist";

const fields = [
    { key: 'id', label: '#', _style: 'width:1%' },
    { key: 'medium', label: 'Medio Basico' },
    { key: 'owner', label: 'Responsable', sorter: false },
    { key: 'identity_card', label: 'Carnet de Identidad' },
    { key: 'datetime', label: 'Fecha', filter: false },
    { key: 'actions', label: 'Acciones', sorter: false, filter: false }
];

export default {
    name: "ResponsibilityCertificatePage",
    title: 'Admin | Acta de Responsabilidad',
    panel_title: 'Lista de Actas de Responsabilidad',
    mixins: [loading, table_list],
    data() {
        return {
            // Static Data
            route: 'responsibility_certificate',
            privilege: 'responsibilitycertificate',
            fields,
        }
    },
    computed: {
        // Cleared items
        items() {
            let list = [];
            this.data.items.forEach((value) => {
                list.push({
                    id: value.id,
                    medium: value.medium.name + ' - ' + value.medium.inventory_number,
                    owner: this.get_full_name(value),
                    identity_card: value.identity_card,
                    datetime: value.datetime,
                });
            });
            return list;
        }
    },
    methods: {
        // Extract Data
        get_full_name(item) {
            let value = item.owner.first_name + ' ' + item.owner.last_name;
            return validator.isEmpty(value) ? item.owner.username : value;
        },
        // QuerySet (CRUD)
        get_queryset() {
            this.$services.getList_ResponsibilityCertificate(this);
        },
        remove() {
            this.$services.remove_ResponsibilityCertificate(this, this.delete_data.id);
        },
    },
}
</script>

<style scoped>
    .card-body {
        padding: 0 1.25rem;
    }
</style>