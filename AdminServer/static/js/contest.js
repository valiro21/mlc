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

    $('.table-sort').tableAddCounter();
    $('.table-sort tbody').sortable();
});

(function ($) {
    $.fn.extend({
        tableAddCounter: function (options) {
            var defaults = {
                title: '#',
                start: 1,
                id: true,
                cssClass: true
            };

            var options = $.extend({}, defaults, options);

            return $(this).each(function () {
                if ($(this).is('table')) {

                    if (!options.title) options.title = '';
                    $('th:first-child, thead td:first-child', this).each(function () {
                        var tagName = $(this).prop('tagName');
                        $(this).before('<' + tagName + ' rowspan="' + $('thead tr').length + '" class="' + options.cssClass + '" id="' + options.id + '">' + options.title + '</' + tagName + '>');
                    });

                    $('tbody td:first-child', this).each(function (i) {
                        $(this).before('<td>' + (options.start + i) + '</td>');
                    });

                }
            });
        }
    });
})(jQuery);