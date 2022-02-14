export default {
    // Validator
    isEmpty: (value) => value.length === 0 || !value.trim(),
    isNull: (value) => value === undefined || value === null,
    isNumber: (value) => !isNaN(value),
    isDate: (value) => !isNaN(new Date(value).getDate()),
    isObject: (r) => typeof r.data === 'object',
    isString: (r) => typeof r.data === 'string',
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
    inventoryNumberIsValid(value) { return this.regex(/\b[A-Za-z]{2}[0-9]{7}\b/, value); }
};