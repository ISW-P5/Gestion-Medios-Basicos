<template>
    <CCard v-if="this.$route.name === (route + '.add') || this.$route.name === (route + '.edit')">
        <CCardHeader v-if="this.$route.name === (route + '.add')">
            <CIcon name="cil-plus"/>
            Añadir Usuario
            <div class="card-header-actions" v-if="privilege_required(privilege, privileges.ADD)">
                <CButton color="danger" size="sm"
                         :to="{name: 'user', params: {id:$route.params.id}}">
                    <CIcon name="cil-ban" /> Cancelar
                </CButton>
            </div>
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
                    label="Usuario *"
                    placeholder="Usuario"
                    :horizontal="horizontal"
                    required
                    :value.sync="username"
                    :isValid="is_valid_username"
                    invalid-feedback="No puede estar vacio."
                  />
                <CInput
                    label="Contraseña *"
                    placeholder="Contraseña"
                    :horizontal="horizontal"
                    type="password"
                    required
                    :value.sync="password"
                    :isValid="is_valid_password"
                    invalid-feedback="No puede estar vacio, no puede ser comun y debe contener minimo 8 caracteres."
                  />
                <CInput
                    label="Dirección de correo *"
                    placeholder="pepe@gmail.com"
                    :horizontal="horizontal"
                    type="email"
                    required
                    :value.sync="email"
                    :isValid="is_valid_email"
                    invalid-feedback="No puede estar vacio y debe ser una dirección de correo."
                  />
                <CInput
                    label="Nombre *"
                    placeholder="Nombre"
                    :horizontal="horizontal"
                    required
                    :value.sync="first_name"
                    :isValid="is_valid_first_name"
                    invalid-feedback="No puede estar vacio y solo puede contener letras."
                  />
                <CInput
                    label="Apellido *"
                    placeholder="Apellido"
                    :horizontal="horizontal"
                    required
                    :value.sync="last_name"
                    :isValid="is_valid_last_name"
                    invalid-feedback="No puede estar vacio y solo puede contener letras."
                  />
                <CSelect
                    label="Rol *"
                    :horizontal="horizontal"
                    :options="groups"
                    placeholder="Seleccione un Rol"
                    :value.sync="group_id"
                  />
                <CFormGroup class="form-group form-row">
                    <template #label>
                        <label class="col-form-label col-md-2">Es staff</label>
                    </template>
                    <template #input>
                        <CSwitch
                            color="success"
                            :checked.sync="is_staff"
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
                <CButton color="warning" size="sm" class="text-white mr-2"
                         :to="{name: 'user.edit', params: {id:$route.params.id}}">
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
                        <CBadge v-if="item.v" color="success" size="sm">Si</CBadge>
                        <CBadge v-else color="danger" size="sm">No</CBadge>
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
            ¿Estas seguro de que quieres eliminar el usuario "{{ get_full_name() }}"?
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
            // Not show password if is editing and validate when adding
            return (this.$route.name === (this.route + '.add')) ?
                (!validator.isNull(this.password) && !validator.isEmpty(this.password) &&
                validator.minLength(8, this.password)) : true;
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
        remove() {
            this.$services.remove_User(this, this.id);

            // Redirect
            this.$router.push({name: this.route});
        },
    },
}
</script>