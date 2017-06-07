/**
 * Created by vrosca on 6/4/17.
 */
jQuery(document).ready(function () {
    bodyLayout.sizePane("east", 700);

    // remove scroll bar from pdf viewer
    $('.ui-layout-center').css({
        overflow: 'hidden'
    });

    $('#language').on('change', function (event){
        target = $(event.target);
        editor.getSession().setMode("ace/mode/" + $(target).val());
    });

    $('#submit-solution').on('click', function () {


        event.preventDefault();

        var data = editor.getValue();

        $.ajax({
            type : 'POST',
            url  : '?contest_id=' + getUrlVars()['contest_id'],
            data : {
                lang: $('#language').find('option:selected').text(),
                data: data
            },
            beforeSend: function() {

            },
            success :  function(data) {
                var err = $('#error-msg');

                if(data === "OK") {
                    problem_name = $('#problem_name').val();
                    window.location.href = "/submissions?problem=" + problem_name;
                }
                else{
                    console.log('here');
                    err.text('An error has occured.');
                    err.removeClass('hidden');
                }
            },
            error: function () {
                var err = $('#error-msg');
                err.removeClass('hidden');
                err.text('An error has occured.');
            }
        });
    })

});

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}
