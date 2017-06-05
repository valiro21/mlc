/**
 * Created by fox on 6/1/17.
 */

$('document').ready(function(){
    /* validation */
 $("#register-form").validate({
     rules: {
         username: {
             required: true,
             minlength: 3
         },
         password: {
             required: true,
             minlength: 6
         },
         password_confirmation: {
             required: true,
             equalTo: '#password'
         },
         email: {
             required: true,
             email: true
         },
         first_name: {
             required: true,
             minlength: 3

         },
         last_name: {
             required: true,
             minlength: 3
         }
     },
     messages: {
         username: "Enter a Valid Username",
         first_name: "Enter a First Name",
         last_name: "Enter a Last Name",
         password:{
             required: "Provide a Password",
             minlength: "Password Needs To Be Minimum of 8 Characters"
         },
         user_email: "Enter a Valid Email",
         password_confirm:{
             required: "Retype Your Password",
             equalTo: "Password Mismatch! Retype"
         }
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var data = $("#register-form").serialize();
        $.ajax({
            type : 'POST',
            url  : '/register',
            data : data,
            beforeSend: function()
            {
                $("#error").fadeIn(100, function(){
                    $("#error").html('<p>Registering...</p>');
                })
            },
            success :  function(data) {
                if(data === "registered"){
                    $("#error").fadeIn(1000, function(){
                        $("#error").html('<p>Registration Successful!</p>');
                    });

                }
                else{
                    $("#error").fadeIn(1000, function(){
                        $("#error").html('<p class="alert-danger">Unexpected error!' + data + '</p>');
                    });
                }
            },
            error : function (data) {
                $("#error").fadeIn(1000, function(){
                    $("#error").html('<p class="alert-danger">Unexpected error!' + data + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */

});
