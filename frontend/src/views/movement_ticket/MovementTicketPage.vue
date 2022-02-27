<template>
    <div v-if="this.$route.name === route">
        <CCard>
            <CCardHeader>
                <CIcon name="cil-library"/>
                Listado de Vales de Movimiento<span v-model="data.count" v-if="data"> ({{ data.count }})</span>
                <div class="card-header-actions" v-if="privilege_required(privilege, privileges.ADD)">
                    <CButton color="success" size="sm" :to="{ name: 'movement_ticket.add' }" :disabled="!(data)">
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
                    <template #basic_medium="{item}">
                        <td v-if="privilege_required(privilege, privileges.VIEW)">
                            <CLink :to="{name: 'movement_ticket.detail', params: {id:item.id}}">
                                {{ item.basic_medium }}
                            </CLink>
                        </td>
                        <td v-else>{{ item.basic_medium }}</td>
                    </template>
                    <template #actions="{item}">
                        <td class="py-2">
                            <CButton color="warning" size="sm" class="mr-2 text-white"
                                     v-if="privilege_required(privilege, privileges.MODIFY)"
                                     :to="{name: 'movement_ticket.edit', params: {id:item.id}}">
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
                                     :to="{name: 'movement_ticket.detail', params: {id:item.id}}">
                                <CIcon name="cil-library" /> Ver
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
            ¿Estas seguro de que quieres eliminar el vale de Movimiento
            "({{ delete_data.medium.name + ', ' + delete_data.requester }})"?
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
    { key: 'basic_medium', label: 'Medio Basico' },
    { key: 'requester', label: 'Solicitante' },
    { key: 'actual_location', label: 'Ubicacion Actual' },
    { key: 'new_location', label: 'Ubicacion Nueva' },
    { key: 'actions', label: 'Acciones', sorter: false, filter: false }
];

export default {
    name: "MovementTicketPage",
    title: 'Admin | Vales de Movimiento',
    panel_title: 'Lista de los Vales de Movimiento',
    mixins: [loading, table_list],
    data() {
        return {
            // Static Data
            route: 'movement_ticket',
            privilege: 'movementticket',
            fields,
        }
    },
    computed: {
        // Cleared items
        items() {
            let list = [];
            this.data.items.forEach((value) => {
                list.push({
                    basic_medium: value.medium.name + ' - ' + value.medium.inventory_number,
                    requester: this.get_full_name(value),
                    ...value
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
            this.$services.getList_MovementTicket(this);
        },
        remove() {
            this.$services.remove_MovementTicket(this, this.delete_data.id);
        },
    },
}
</script>

<style scoped>
    .card-body {
        padding: 0 1.25rem;
    }
</style>