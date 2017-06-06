$('document').ready(function(){
    /* validation */
    $("#add-problem").submit(submitForm);

    /* form submit */
    function submitForm(){
        var data = $("#add-problem").serialize();
        var contestName = $('#contest-name').val();
        $.ajax({
            type : 'POST',
            url  : '/contest/' + contestName + '/add_problem',
            data : data,
            success :  function(data) {
                $('#error').html(data);
            },
            error : function (data) {
                $('#error').html('An error has occured.');
            }
        });
        return false;
    }
    /* form submit */

});
