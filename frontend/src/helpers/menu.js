function addElementToSidebar(sidebar, element) {
    sidebar[0]._children.push(element);
}

export function getSidebar(permission) {
    // Create sidebar
    let sidebar = [
        {
            _name: 'CSidebarNav',
            _children: []
        }
    ];
    // Access
    if (permission) {
        addElementToSidebar(sidebar, {
            _name: 'CSidebarNavItem',
            name: 'Inicio',
            to: '/',
            icon: 'cil-home'
        });

        // Medio Basico
        if (permission.basicmediumexpedient && permission.basicmediumexpedient.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Medios Basicos',
                to: {name: 'basic_medium'},
                icon: 'cil-book'
            });
        }

        // Vale de Movimiento
        if (permission.movementticket && permission.movementticket.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Vales de Movimiento',
                to: {name: 'movement_ticket'},
                icon: 'cil-library'
            });
        }

        // Vale de Solicitud
        if (permission.requestticket && permission.requestticket.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Vales de Solicitud',
                to: {name: 'request_ticket'},
                icon: 'cil-file'
            });
        }

        // Acta de Responsabilidad
        if (permission.responsibilitycertificate && permission.responsibilitycertificate.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Actas de Responsabilidad',
                to: {name: 'responsibility_certificate'},
                icon: 'cil-address-book'
            });
        }

        // Usuario
        if (permission.user && permission.user.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Usuarios',
                to: {name: 'user'},
                icon: 'cil-user'
            });
        }

        // Grupo
        if (permission.group && permission.group.includes(0)) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Grupos',
                to: {name: 'group'},
                icon: 'cil-group'
            });
        }
    }

    // Documentation and Develop
    addElementToSidebar(sidebar, {
        _name: 'CSidebarNavTitle',
        _children: ['Soporte']
    });
    addElementToSidebar(sidebar, {
        _name: 'CSidebarNavItem',
        name: 'Ayuda',
        to: {name: 'help'},
        icon: 'cil-spreadsheet'
    });
    return sidebar;
}