<template>
    <CCard v-if="this.$route.name === (route + '.add') || this.$route.name === (route + '.edit')">
        <CCardHeader v-if="this.$route.name === (route + '.add')">
            <CIcon name="cil-plus"/>
            Añadir Usuario
        </CCardHeader>
        <CCardHeader v-else>
            <CIcon name="cil-user"/>
            Editar Usuario
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="danger" size="sm"
                         :to="{name: 'user.detail', params: {id:$route.params.id}}">
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
                    invalid-feedback="No puede estar vacio y solo puede contener letras."
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
            <CIcon name="cil-user"/>
            Ver Usuario ({{ get_full_name() }})
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.MODIFY)">
                <CButton color="warning" size="sm" class="text-white"
                         :to="{name: 'user.edit', params: {id:$route.params.id}}">
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
    name: "DetailUserPage",
    title: 'Admin | Usuario',
    panel_title: 'Usuario',
    mixins: [detail_table],
    data() {
        return {
            // Static Data
            route: 'user',
            privilege: 'user',
            // Values
            id: '',
            username: '',
            password: '',
            email: '',
            first_name: '',
            last_name: '',
            group_id: 0,
            group_name: '',
            groups: [],
            is_staff: false,
        }
    },
    computed: {
        detail() {
            return [
                {'p': 'ID', 'v': this.id},
                {'p': 'Usuario', 'v': this.username},
                {'p': 'Correo electrónico', 'v': this.email},
                {'p': 'Nombre', 'v': this.first_name},
                {'p': 'Apellido', 'v': this.last_name},
                {'p': 'Ubicacion', 'v': this.location},
                {'p': 'Cargo', 'v': this.group_name},
                {'p': 'Es staff', 'v': this.is_staff},
            ];
        }
    },
    methods: {
        get_full_name() {
            let value = this.first_name + ' ' + this.last_name;
            return validator.isEmpty(value) ? this.username : value;
        },
        is_valid_username() {
            return (!validator.isNull(this.username) && !validator.isEmpty(this.username)
                && validator.onlyLettersAndNumbersWithoutSpace(this.username));
        },
        is_valid_password() {
            return (!validator.isNull(this.password) && !validator.isEmpty(this.password) &&
                validator.minLength(8, this.password));
        },
        is_valid_email() {
            return (!validator.isNull(this.email) && !validator.isEmpty(this.email) && validator.isMail(this.email));
        },
        is_valid_first_name() {
            return (!validator.isNull(this.first_name) && !validator.isEmpty(this.first_name) &&
                validator.onlyLetters(this.first_name));
        },
        is_valid_last_name() {
            return (!validator.isNull(this.last_name) && !validator.isEmpty(this.last_name) &&
                validator.onlyLetters(this.last_name));
        },
        is_valid_group_id() {
            return (!validator.isNull(this.group_id) && validator.isNumber(this.group_id) && this.group_id > 0);
        },
        is_valid() {
            return [
                // Validate username
                this.is_valid_username(),

                // Validate password
                this.is_valid_password(),

                // Validate email
                this.is_valid_email(),

                // Validate first name
                this.is_valid_first_name(),

                // Validate last name
                this.is_valid_last_name(),

                // Validate group
                this.is_valid_group_id(),
            ].every((v) => v);
        },
        reset() {
            this.id = '';
            this.username = '';
            this.password = '';
            this.email = '';
            this.first_name = '';
            this.last_name = '';
            this.group_id = 0;
            this.group_name = '';
            this.is_staff = false;
        },
        add_queryset() {
            this.$services.add_User(this);
        },
        edit_queryset() {
            this.$services.edit_User(this, this.$route.params.id);
        },
        get_queryset() {
            this.$services.detail_User(this, this.$route.params.id);
        },
        metadata_queryset() {
            this.$services.getList_Roles(this);
        },
    },
}
</script>