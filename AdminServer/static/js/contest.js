jQuery(document).ready(function(){
    $('.answer').on('change', function (e) {
        // With $(this).val(), you can **(and have to!)** specify the target in your <option> values.
        if ($(this).find(':selected').text() == 'Other') {
            var id = $(this).attr('data-toggle')
            $('#'+id).removeClass('collapse');
        }
        else {
            var id = $(this).attr('data-toggle')
            $('#'+id).addClass('collapse');
        }
    });
});