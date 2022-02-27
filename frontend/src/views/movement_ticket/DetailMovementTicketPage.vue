<template>
    <CCard v-if="this.$route.name === (route + '.add') || this.$route.name === (route + '.edit')">
        <CCardHeader v-if="this.$route.name === (route + '.add')">
            <CIcon name="cil-plus"/>
            Añadir Vale de Movimiento
        </CCardHeader>
        <CCardHeader v-else>
            <CIcon name="cil-library"/>
            Editar Vale de Movimiento
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="danger" size="sm"
                         :to="{name: 'movement_ticket.detail', params: {id:$route.params.id}}">
                    <CIcon name="cil-ban" /> Cancelar
                </CButton>
            </div>
        </CCardHeader>
        <CCardBody>
            <CForm v-model:was-validated="wasValidated">
                <CSelect
                    label="Medio Basico *"
                    :horizontal="horizontal"
                    :options="basic_medium"
                    placeholder="Seleccione un Medio Basico"
                    required
                    :value.sync="basic_medium_id"
                    :isValid="is_valid_basic_medium_id"
                    invalid-feedback="Debe seleccionarse un Medio Basico."
                  />
                <CSelect v-if="this.$store.state.user.is_superuser || !privilege_required(privilege, privileges.OWN)"
                    label="Solicitante *"
                    :horizontal="horizontal"
                    :options="responsible"
                    placeholder="Seleccione un Solicitante"
                    required
                    :value.sync="requester_id"
                    :isValid="is_valid_requester_id"
                    invalid-feedback="Debe seleccionarse un Solicitante."
                  />
                <CInput
                    label="Ubicacion Actual *"
                    placeholder="Ubicacion Actual"
                    :horizontal="horizontal"
                    required
                    :value.sync="actual_location"
                    :isValid="is_valid_actual_location"
                    invalid-feedback="No puede estar vacio."
                  />
                <CInput
                    label="Ubicacion Nueva *"
                    placeholder="Ubicacion Nueva"
                    :horizontal="horizontal"
                    required
                    :value.sync="new_location"
                    :isValid="is_valid_new_location"
                    invalid-feedback="No puede estar vacio."
                  />
                <CButton type="submit" @click="add" class="mr-1" color="success"
                         v-if="this.$route.name === (route + '.add') && privilege_required(privilege, privileges.ADD)">
                    <CIcon name="cil-check-circle"/> Enviar
                </CButton>
                <CButton type="submit" @click="edit" class="mr-1" color="primary"
                         v-else-if="privilege_required(privilege, privileges.MODIFY)">
                    <CIcon name="cil-check-circle"/> Editar
                </CButton>
                <CButton type="reset" color="danger" @click="reset"><CIcon name="cil-ban"/> Limpiar</CButton>
            </CForm>
        </CCardBody>
    </CCard>
    <CCard v-else-if="this.$route.name === (route + '.detail')">
        <CCardHeader>
            <CIcon name="cil-library"/>
            Ver Vale de Movimiento ({{ basic_medium_name + ' - ' + requester_name }})
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="warning" size="sm" class="text-white mr-2"
                         :to="{name: 'movement_ticket.edit', params: {id:$route.params.id}}">
                    <CIcon name="cil-pencil" /> Editar
                </CButton>
                <CButton color="danger" size="sm"
                         v-if="privilege_required(privilege, privileges.DELETE)"
                         @click="set_delete()">
                    <CIcon name="cil-trash" /> Eliminar
                </CButton>
            </div>
        </CCardHeader>
        <CCardBody>
            <CDataTable :items="detail" :fields="fields" :noItemsView="{
                noResults: 'No hay resultados',
                noItems: 'No hay elementos'
            }" :header="false" striped border>
                <template #p="{item}">
                    <td v-if="typeof item.v == 'boolean'" class="text-right col-md-4">
                        <b>{{item.p}}</b>
                    </td>
                    <td v-else-if="item.v && item.v !== 'None' && item.v !== ''" class="text-right col-md-4">
                        <b>{{item.p}}</b>
                    </td>
                </template>
                <template #v="{item}">
                    <td v-if="typeof item.v == 'boolean'" class="col-md-8">
                        <CBadge v-if="item.v" color="success" size="sm">Verdadero</CBadge>
                        <CBadge v-else color="danger" size="sm">Falso</CBadge>
                    </td>
                    <td v-else-if="item.v && item.v !== 'None' && item.v !== ''" class="col-md-8">
                        {{item.v}}
                    </td>
                </template>
            </CDataTable>
        </CCardBody>
        <!-- Delete Confirmation Modal -->
        <CModal :centered="true" :scrollable="false" title="Eliminar!" size="sm" color="warning"
                :show.sync="confirm_delete">
            ¿Estas seguro de que quieres eliminar el vale de movimiento
            "({{ basic_medium_name + ', ' + requester_name }})"?
            <template #footer>
                <CButton color="default" size="sm" @click="finish_delete()">Cancelar</CButton>
                <CButton color="danger" size="sm" @click="remove()">¡Eliminar!</CButton>
            </template>
        </CModal>
    </CCard>
</template>

<script>
import detail_table from "../../mixins/detailtable";
import validator from "../../helpers/validator";

export default {
    name: "DetailMovementTicketPage",
    title: 'Admin | Vale de Movimiento',
    panel_title: 'Vale de Movimiento',
    mixins: [detail_table],
    data() {
        return {
            // Static Data
            route: 'movement_ticket',
            privilege: 'movementticket',
            // Values
            id: '',
            basic_medium_id: 0,
            basic_medium_name: '',
            basic_medium: [],
            actual_location: '',
            new_location: '',
            requester_id: 0,
            requester_name: '',
            responsible: [],
        }
    },
    computed: {
        detail() {
            return [
                {'p': 'ID', 'v': this.id},
                {'p': 'Medio Basico', 'v': this.basic_medium_name},
                {'p': 'Solicitante', 'v': this.requester_name},
                {'p': 'Ubicacion Actual', 'v': this.actual_location},
                {'p': 'Ubicacion Nueva', 'v': this.new_location},
            ];
        }
    },
    methods: {
        is_valid_basic_medium_id() {
            return (!validator.isNull(this.basic_medium_id) && validator.isNumber(this.basic_medium_id) &&
                this.basic_medium_id > 0);
        },
        is_valid_requester_id() {
            return (!validator.isNull(this.requester_id) && validator.isNumber(this.requester_id) &&
                this.requester_id > 0);
        },
        is_valid_actual_location() {
            return (!validator.isNull(this.actual_location) && !validator.isEmpty(this.actual_location) &&
                validator.onlyLettersAndNumbers(this.actual_location));
        },
        is_valid_new_location() {
            return (!validator.isNull(this.new_location) && !validator.isEmpty(this.new_location) &&
                validator.onlyLettersAndNumbers(this.new_location));
        },
        is_valid() {
            return [
                // Validate basic medium
                this.is_valid_basic_medium_id(),

                // Validate requester
                this.is_valid_requester_id(),

                // Validate actual location
                this.is_valid_actual_location(),

                // Validate new location
                this.is_valid_new_location(),
            ].every((v) => v);
        },
        reset() {
            this.id = '';
            this.basic_medium_id = 0;
            this.basic_medium_name = '';
            this.basic_medium = [];
            this.actual_location = '';
            this.new_location = '';
            this.requester_id = 0;
            this.requester_name = '';
            this.responsible = [];
        },
        add_queryset() {
            this.$services.add_MovementTicket(this);
        },
        edit_queryset() {
            this.$services.edit_MovementTicket(this, this.$route.params.id);
        },
        get_queryset() {
            this.$services.detail_MovementTicket(this, this.$route.params.id);
        },
        metadata_queryset() {
            this.$services.getList_Mediums(this);
            if (this.$store.state.user.is_superuser || !this.privilege_required(this.privilege, this.privileges.OWN)) {
                this.$services.getList_Responsible(this);
            } else {
                this.requester_id = this.$store.state.user.id;
            }
        },
        remove() {
            this.$services.remove_MovementTicket(this, this.id);

            // Redirect
            this.$router.push({name: this.route});
        },
    },
}
</script>