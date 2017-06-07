/**
 * Created by fox on 6/7/17.
 */

$('document').ready(function(){
    /* validation */
 $("#reset-form").validate({
     rules: {
         reset_password: {
             required: true,
             minlength: 6
         },
         reset_password_confirm: {
             required: true,
             equalTo: '#reset_password'
         },
     },
     messages: {
         reset_password:{
             required: "Provide a Password",
             minlength: "Password Needs To Be Minimum of 6 Characters"
         },
         reset_password_confirm:{
             required: "Retype Your Password",
             equalTo: "Password Mismatch! Retype"
         }
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var data = $("#reset-form").serialize();
        $.ajax({
            type : 'POST',
            url  : '/recovery/reset_password',
            data : data,
            beforeSend: function()
            {
                $("#reset_status").fadeIn(100, function(){
                    $("#reset_status").html('<p>Changing password...</p>');
                })
            },
            success :  function(data) {
                if(data === "Password reset done."){
                    $("#reset_status").fadeIn(1000, function(){
                        $("#reset_status").html('<p>Password changed!</p>');
                    });

                }
                else{
                    $("#reset_status").fadeIn(1000, function(){
                        $("#reset_status").html('<p class="alert-danger"> Error: ' + data + '!</p>');
                    });
                }
            },
            error : function (data) {
                $("#reset_status").fadeIn(1000, function(){
                    $("#reset_status").html('<p class="alert-danger">Unexpected error!\n' + data + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */
});