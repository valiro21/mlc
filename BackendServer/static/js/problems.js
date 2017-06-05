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
            url  : '',
            data : {
                lang: $('#language option:selected').text(),
                data: data
            },
            beforeSend: function() {

            },
            success :  function(data) {
                if(data === "OK") {
                    window.location.href = "../submissions";
                }
            }
        });
    })

});