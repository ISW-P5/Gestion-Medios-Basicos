// Initialize Bootstrap DatePicker -> only html input
$(function () {
    $(".datepicker").datepicker({
        todayBtn: "linked",
        weekStart: 1,
        todayHighlight: true,
        autoclose: true,
        orientation: "bottom",
        disableTouchKeyboard: true
    });
});