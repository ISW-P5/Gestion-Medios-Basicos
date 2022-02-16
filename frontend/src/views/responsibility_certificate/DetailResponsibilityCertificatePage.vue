<template>
    <CCard v-if="this.$route.name === (route + '.add') || this.$route.name === (route + '.edit')">
        <CCardHeader v-if="this.$route.name === (route + '.add')">
            <CIcon name="cil-plus"/>
            Añadir Acta de Responsabilidad
        </CCardHeader>
        <CCardHeader v-else>
            <CIcon name="cil-address-book"/>
            Editar Acta de Responsabilidad
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="danger" size="sm"
                         :to="{name: 'responsibility_certificate.detail', params: {id:$route.params.id}}">
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
                    label="Carnet de Identidad *"
                    placeholder="Carnet de Identidad"
                    :horizontal="horizontal"
                    required
                    :value.sync="identity_card"
                    :isValid="is_valid_identity_card"
                    invalid-feedback="No puede estar vacio y solo puede contener numeros."
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
            <CIcon name="cil-address-book"/>
            Ver Acta de Responsabilidad ({{ basic_medium_name + ' - ' + responsible_name }})
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="warning" size="sm" class="text-white"
                         :to="{name: 'responsibility_certificate.edit', params: {id:$route.params.id}}">
                    <CIcon name="cil-pencil" /> Editar
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
    </CCard>
</template>

<script>
import detail_table from "../../mixins/detailtable";
import validator from "../../helpers/validator";

export default {
    name: "DetailResponsibilityCertificatePage",
    title: 'Admin | Acta de Responsabilidad',
    panel_title: 'Acta de Responsabilidad',
    mixins: [detail_table],
    data() {
        return {
            // Static Data
            route: 'responsibility_certificate',
            privilege: 'responsibilitycertificate',
            // Values
            id: '',
            identity_card: '',
            basic_medium_id: 0,
            basic_medium_name: '',
            basic_medium: [],
            datetime: '',
            responsible_id: 0,
            responsible_name: '',
            responsible: [],
        }
    },
    computed: {
        detail() {
            return [
                {'p': 'ID', 'v': this.id},
                {'p': 'Medio Basico', 'v': this.basic_medium_name},
                {'p': 'Responsable', 'v': this.responsible_name},
                {'p': 'Carnet de Identidad', 'v': this.identity_card},
                {'p': 'Fecha', 'v': this.$options.filters.formatDate(this.datetime)},
            ];
        }
    },
    methods: {
        is_valid_basic_medium_id() {
            return (!validator.isNull(this.basic_medium_id) && validator.isNumber(this.basic_medium_id) &&
                this.basic_medium_id > 0);
        },
        is_valid_identity_card() {
            return (!validator.isNull(this.identity_card) && !validator.isEmpty(this.identity_card) &&
                validator.onlyNumbers(this.identity_card));
        },
        is_valid_responsible_id() {
            return (!validator.isNull(this.responsible_id) && validator.isNumber(this.responsible_id) &&
                this.responsible_id > 0);
        },
        is_valid() {
            return [
                // Validate basic medium
                this.is_valid_basic_medium_id(),

                // Validate identity card
                this.is_valid_identity_card(),

                // Validate responsible
                this.is_valid_responsible_id(),
            ].every((v) => v);
        },
        reset() {
            this.id = '';
            this.identity_card = '';
            this.basic_medium_id = 0;
            this.datetime = '';
            this.responsible_id = 0;
        },
        add_queryset() {
            this.$services.add_ResponsibilityCertificate(this);
        },
        edit_queryset() {
            this.$services.edit_ResponsibilityCertificate(this, this.$route.params.id);
        },
        get_queryset() {
            this.$services.detail_ResponsibilityCertificate(this, this.$route.params.id);
        },
        metadata_queryset() {
            this.$services.getList_MediumsCertificate(this);
            this.$services.getList_Responsible(this);
        },
    },
}
</script>

<style scoped>

</style>