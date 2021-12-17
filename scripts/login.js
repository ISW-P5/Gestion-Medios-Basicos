// Comprobar si esta vacio el texto
function isNullOrEmpty(value) {
    return (value.length === 0 || !value.trim());
}

function showError(message) {
    var element = $("#message-error");
    element.html(message);
    element.show();
}

function validate_login() {
    // Restart error
    hide_errors();
    var error = false;

    // Validate Username
    if(!validate_username()) {
        $("div#username-error").show();
        error = true;
    }

    // Validate Password
    if(!validate_password()) {
        $("div#password-error").show();
        error = true;
    }

    if (!error) {
        // Validate Login (Usamos momentaneamente un validador de usuarios y contraseñas hasta que se implemente el backend)
        if (!validate_user_login()) return false;
    }

    // Allow send data
    return false;
}

function validate_user_login() {
    // Allow access
    var username = $('form input[name="username"]').val();
    var password = $('form input[name="password"]').val();

    var valid_username_and_password = ["admin", "jdepa", "vicedecano"];
    var urls = ["principal_page_admin.html", "principal_page_jefe_depa.html",
                "principal_page_vicedecano.html"];
    
    for(var i = 0; i < urls.length; i++) {
        if (username === valid_username_and_password[i] && password === valid_username_and_password[i]) {
            
            //$(location).attr('href', urls[i]);
            window.location.href = urls[i];
            return true;
        }
    }

    // Show error
    showError("Usuario o contraseña incorrectos.");
    return false;
}

function validate_username() {
    // Extract username
    var username = $('form input[name="username"]').val();

    // Validate username (empty)
    return !isNullOrEmpty(username);
}

function validate_password() {
    // Extract password
    var password = $('form input[name="password"]').val();

    // Validate password (empty)
    if (isNullOrEmpty(password)) return false;

    // Validate password (min 4)
    return password.length >= 4;
}

// Esconder mensaje de error por defecto
function hide_errors() {
    $("div#message-error").hide();
    $("div#username-error").hide();
    $("div#password-error").hide();
}

$(document).ready(function () {
    // Capturar evento onSubmit del formulario y validarlo
    $(document).on('submit', 'form#form-login', () => validate_login());

    $('form input[name="username"]').keyup(function () {
        // Validate Username
        if(!validate_username()) {
            $("div#username-error").show();
        } else {
            $("div#username-error").hide();
        }
    });

    $('form input[name="password"]').keyup(function () {
        // Validate password
        if(!validate_password()) {
            $("div#password-error").show();
        } else {
            $("div#password-error").hide();
        }
    });
});
