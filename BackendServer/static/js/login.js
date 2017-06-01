/**
 * Created by fox on 6/1/17.
 */

$('document').ready(function(){
    /* validation */
 $("#login-form").validate({
     rules: {
         username: {
             required: true,
             minlength: 3
         },
         password: {
             required: true,
             minlength: 6
         },
     },
     messages: {
         username: "Enter a Valid Username",
         password:{
             required: "Provide a Password",
             minlength: "Password Needs To Be Minimum of 8 Characters"
         },
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var data = $("#login-form").serialize();
        $.ajax({
            type : 'POST',
            url  : '/login',
            data : data,
            beforeSend: function() {

            },
            success :  function(data) {
                if(data === "Logged in.") {
                    window.location.href = "/";
                }
            }
        });
        return false;
    }
    /* form submit */

});