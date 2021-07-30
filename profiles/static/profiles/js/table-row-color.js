$(document).ready(function() {
    $('tr:odd').css('background-color', 'rgba(0,0,0,0.1)');
    $('tr:odd').css('border-bottom', '1px solid rgb(76, 175, 80)').css('border-top', '1px solid rgb(76, 175, 80)');
    $('tr:last').css('border-bottom', 'none');
})