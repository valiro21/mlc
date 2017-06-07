/**
 * Created by fox on 6/6/17.
 */

$('document').ready(function(){
    /* validation */
 $("#recovery-form").validate({
     rules: {
         recovery_email: {
             required: true,
             email: true
         }
     },
     messages: {
         recovery_email: "Enter a Valid Email"
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var data = $("#recovery-form").serialize();
        $.ajax({
            type : 'POST',
            url  : '/recovery/send_email',
            data : data,
            beforeSend: function()
            {
                $("#recovery_error").fadeIn(100, function(){
                    $("#recovery_error").html('<p>Sending mail...</p>');
                })
            },
            success :  function(data) {
                if(data === "Mail sent."){
                    $("#recovery_error").fadeIn(1000, function(){
                        $("#recovery_error").html('<p>Mail sent!</p>');
                    });

                }
                else{
                    $("#recovery_error").fadeIn(1000, function(){
                        $("#recovery_error").html('<p class="alert-danger"> ' + data + ' </p>');
                    });
                }
            },
            error : function (data) {
                $("#recovery_error").fadeIn(1000, function(){
                    $("#recovery_error").html('<p class="alert-danger">Unexpected error: ' + data + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */
});