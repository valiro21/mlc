/**
 * Created by fox on 6/1/17.
 */

$('document').ready(function(){
    /* validation */
 $("#login-form").validate({
     rules: {
         login_username: {
             required: true,
             minlength: 3
         },
         login_password: {
             required: true,
             minlength: 6
         },
     },
     messages: {
         login_username: "Enter a Valid Username",
         login_password:{
             required: "Provide a Password",
             minlength: "Password Needs To Be Minimum of 6 Characters"
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
                    $("#login_status").fadeIn(1000, function(){
                        $("#login_status").html('<p>Password changed!</p>');
                    });
                    window.location.href = "/";
                }
                else{
                    $("#login_status").fadeIn(1000, function(){
                        $("#login_status").html('<p>' + data + '</p>');
                    });
                }
            },
            error : function(data) {
                $("#login_status").fadeIn(1000, function(){
                        $("#login_status").html('<p>' + data + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */

});