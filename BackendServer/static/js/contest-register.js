/**
 * Created by andreiwork on 05.06.2017.
 */

$('document').ready(function(){
    /* validation */
 $("#contest-register").validate({
     rules: {
         checkbox: {
             required: true
         }
     },
     messages: {
         checkbox: "You must agree with the terms and conditions"
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var sPageURL = decodeURIComponent(window.location),
            contest_id = sPageURL.split('/')[4],
            data2 = $("#contest-register").serialize();

        $.ajax({
            type : 'POST',
            url  : '/contest/' + contest_id + '/register',
            data : data2,
            beforeSend: function()
            {
                $("#contest-register-error").fadeIn(100, function(){
                    $("#contest-register-error").html('<p>Registering...</p>');
                })
            },
            success :  function(data2) {
                if(data2 === "registered"){
                    $("#contest-register-error").fadeIn(1000, function(){
                        $("#contest-register-error").html('<p>Registration Successful!</p>');
                    });

                }
                else{
                    $("#contest-register-error").fadeIn(1000, function(){
                        $("#contest-register-error").html('<p class="alert-danger">Unexpected error! ' + data2 + '</p>');
                    });
                }
            },
            error : function (data2) {
                $("#contest-register-error").fadeIn(1000, function(){
                    $("#contest-register-error").html('<p class="alert-danger">Unexpected error! ' + data2 + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */

});