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
    if (permission[0] > 0) {
        addElementToSidebar(sidebar, {
            _name: 'CSidebarNavItem',
            name: 'Panel Principal',
            to: '/',
            icon: 'cil-speedometer'
        });
        // Console
        if (permission[1] > 0) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Consola',
                to: {name: 'console'},
                icon: 'cil-terminal'
            });
        }
        // Config
        if (permission[2] > 0) {
            addElementToSidebar(sidebar, {
                _name: 'CSidebarNavItem',
                name: 'Configuración',
                to: {name: 'config'},
                icon: 'cil-settings'
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