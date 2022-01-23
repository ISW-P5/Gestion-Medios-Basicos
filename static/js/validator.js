// Validate
const validator = {
    // Validator
    isEmpty: (value) => value.length === 0 || !value.trim(),
    isNull: (value) => value === undefined || value === null,
    isNumber: (value) => !isNaN(value),
    isDate: (value) => !isNaN(new Date(value).getDate()),
    minLength: (n, value) => value.length < n,
    equalLength: (n, value) => value.length === n,
    maxLength: (n, value) => value.length > n,
    regex: (regex, value) => regex.test(value),
    email: (email) => email.match(
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    ),
    onlyNumbers(value) { return this.regex(/^\d+$/, value); },
    onlyLetters(value) { return this.regex(/^[a-zA-Z]+$/, value); },
    onlyLettersAndNumbers(value) { return this.regex(/^[a-zA-Z0-9]+$/i, value); },

    // Extractors
    getValueInput: (input_name) => $('input[name="' + input_name + '"]').val(),
    getValueSelect: (input_name) => $('select[name="' + input_name + '"]').val(),
    getChecked: (input_name) => $('input[name="' + input_name + '"]').checked,

    // Utils
    hide_reset: (array) => {
        for(let i = 0; i < array.length; i++) {
            $(array[i]).hide();
        }
    },
    validate: (expresion, element) => {
        if (expresion) {
            $(element).show();
            return true;
        }
        $(element).hide();
        return false;
    }
};

function n_inv(value) {
    return validator.regex(/\b[A-Za-z]{2}[0-9]{7}\b/, value);
}