<template>
    <CDropdown
            inNav
            class="c-header-nav-items"
            placement="bottom-end"
            add-menu-classes="pt-0"
    >
        <template #toggler>
            <CHeaderNavLink>
                <div class="c-avatar">
                    <img :src="'/api/avatar?u=' + $store.state.user.username + '&width=64&height=64&font-size=36'"
                         class="c-avatar-img"  alt="User Avatar"/>
                </div>
            </CHeaderNavLink>
        </template>
        <CDropdownHeader tag="div" class="text-center" color="light">
            <CIcon name="cil-user"></CIcon>
            <strong>{{ $store.state.user.username }}</strong>
        </CDropdownHeader>
        <!-- #TODO: Add User Profile -->
        <CDropdownItem :href="'#/users/' + $store.state.user.id + '/detail/'">
            <CIcon name="cil-user"/>
            Perfil de Usuario
        </CDropdownItem>
        <CDropdownItem href="/logout">
            <CIcon name="cil-account-logout"/>
            Cerrar Sesion
        </CDropdownItem>
    </CDropdown>
</template>

<script>
export default {
    name: 'TheHeaderDropdownAccnt',
    data() {
        return {
            itemsCount: 42
        }
    }
};
</script>

<style scoped>
    .c-icon {
        margin-right: 0.3rem;
    }
</style>