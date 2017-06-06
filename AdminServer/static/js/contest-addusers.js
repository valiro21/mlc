/**
 * Created by andreiwork on 06.06.2017.
 */

$('document').ready(function(){
    /* validation */
 $("#contest-addusers").validate({
     rules: {
        username : {
             required: true
         }
     },
     messages: {
         username: "You must provide an username"
     },
     submitHandler: submitForm
    });
    /* validation */

    /* form submit */
    function submitForm(){
        var sPageURL = decodeURIComponent(window.location),
            contest_id = sPageURL.split('/')[4],
            data2 = $("#contest-addusers").serialize();

        $.ajax({
            type : 'POST',
            url  : '/contest/' + contest_id + '/addusers',
            data : data2,
            beforeSend: function()
            {
                $("#contest-addusers-error").fadeIn(100, function(){
                    $("#contest-addusers-error").html('<p>Registering...</p>');
                })
            },
            success :  function(data2) {
                if(data2 === "registered"){
                    $("#contest-addusers-error").fadeIn(1000, function(){
                        $("#contest-addusers-error").html('<p>User added or updated successful!</p>');
                    });

                }
                else{
                    $("#contest-addusers-error").fadeIn(1000, function(){
                        $("#contest-addusers-error").html('<p class="alert-danger">Unexpected error! ' + data2 + '</p>');
                    });
                }
            },
            error : function (data2) {
                $("#contest-addusers-error").fadeIn(1000, function(){
                    $("#contest-addusers-error").html('<p class="alert-danger">Unexpected error! ' + data2 + '</p>');
                });
            }
        });
        return false;
    }
    /* form submit */

});