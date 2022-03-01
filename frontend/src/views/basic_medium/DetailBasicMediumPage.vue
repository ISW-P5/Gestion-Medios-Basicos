<template>
    <CCard v-if="this.$route.name === (route + '.add') || this.$route.name === (route + '.edit')">
        <CCardHeader v-if="this.$route.name === (route + '.add')">
            <CIcon name="cil-plus"/>
            Añadir Medio Basico
        </CCardHeader>
        <CCardHeader v-else>
            <CIcon name="cil-book"/>
            Editar Medio Basico
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="danger" size="sm"
                         :to="{name: 'basic_medium.detail', params: {id:$route.params.id}}">
                    <CIcon name="cil-ban" /> Cancelar
                </CButton>
            </div>
        </CCardHeader>
        <CCardBody>
            <CForm v-model:was-validated="wasValidated">
                <CInput
                    label="Nombre *"
                    description="Nombre del Medio Basico"
                    placeholder="Nombre"
                    :horizontal="horizontal"
                    required
                    :value.sync="name"
                    :isValid="is_valid_name"
                    invalid-feedback="No puede estar vacio y solo puede contener letras."
                  />
                <CInput
                    label="Numero de Inventario *"
                    placeholder="MB1234567"
                    :horizontal="horizontal"
                    required
                    :value.sync="inventory_number"
                    :isValid="is_valid_inventory_number"
                    invalid-feedback="No puede estar vacio y debe contener 2 letras a continuacion de 7 digitos."
                  />
                <CSelect
                    label="Responsable *"
                    :horizontal="horizontal"
                    :options="responsible"
                    placeholder="Seleccione un Responsable"
                    required
                    :value.sync="responsible_id"
                    :isValid="is_valid_responsible_id"
                    invalid-feedback="Debe seleccionarse un Responsable."
                  />
                <CInput
                    label="Ubicacion *"
                    placeholder="Ubicacion"
                    :horizontal="horizontal"
                    required
                    :value.sync="location"
                    :isValid="is_valid_location"
                    invalid-feedback="No puede estar vacio."
                  />
                <CFormGroup class="form-group form-row">
                    <template #label>
                        <label class="col-form-label col-md-2">Habilitado</label>
                    </template>
                    <template #input>
                        <CSwitch
                            color="success"
                            :checked.sync="is_enable"
                            shape="pill"
                        />
                    </template>
                </CFormGroup>
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
            <CIcon name="cil-book"/>
            Ver Medio Basico ({{ name + ' - ' + inventory_number }})
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="warning" size="sm" class="text-white mr-2"
                         :to="{name: 'basic_medium.edit', params: {id:$route.params.id}}">
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
            ¿Estas seguro de que quieres eliminar el medio basico "{{ name + ' - ' + inventory_number }}"?
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
    name: "DetailBasicMediumPage",
    title: 'Admin | Medio Basico',
    panel_title: 'Medio Basico',
    mixins: [detail_table],
    data() {
        return {
            // Static Data
            route: 'basic_medium',
            privilege: 'basicmediumexpedient',
            // Values
            id: '',
            name: '',
            inventory_number: '',
            location: '',
            responsible_id: 0,
            responsible_name: '',
            responsible: [],
            is_enable: true,
        }
    },
    computed: {
        detail() {
            return [
                {'p': 'ID', 'v': this.id},
                {'p': 'Nombre', 'v': this.name},
                {'p': 'Numero de Inventario', 'v': this.inventory_number},
                {'p': 'Responsable', 'v': this.responsible_name},
                {'p': 'Ubicacion', 'v': this.location},
                {'p': 'Habilitado', 'v': this.is_enable},
            ];
        }
    },
    methods: {
        is_valid_name() {
            return (!validator.isNull(this.name) && !validator.isEmpty(this.name) && validator.onlyLetters(this.name));
        },
        is_valid_inventory_number() {
            return (!validator.isNull(this.inventory_number) && !validator.isEmpty(this.inventory_number) &&
                validator.inventoryNumberIsValid(this.inventory_number));
        },
        is_valid_responsible_id() {
            return (!validator.isNull(this.responsible_id) && validator.isNumber(this.responsible_id) &&
                this.responsible_id > 0);
        },
        is_valid_location() {
            return (!validator.isNull(this.location) && !validator.isEmpty(this.location) &&
                validator.onlyLettersAndNumbers(this.location));
        },
        is_valid() {
            return [
                // Validate name
                this.is_valid_name(),

                // Validate inventory number
                this.is_valid_inventory_number(),

                // Validate responsible
                this.is_valid_responsible_id(),

                // Validate location
                this.is_valid_location(),
            ].every((v) => v);
        },
        reset() {
            this.id = '';
            this.name = '';
            this.inventory_number = '';
            this.location = '';
            this.responsible_id = 0;
            this.is_enable = true;
        },
        add_queryset() {
            this.$services.add_BasicMedium(this);
        },
        edit_queryset() {
            this.$services.edit_BasicMedium(this, this.$route.params.id);
        },
        get_queryset() {
            this.$services.detail_BasicMedium(this, this.$route.params.id);
        },
        metadata_queryset() {
            this.$services.getList_Responsible(this);
        },
        remove() {
            this.$services.remove_BasicMedium(this, this.id);

            // Redirect
            this.$router.push({name: this.route});
        },
    },
}
</script>