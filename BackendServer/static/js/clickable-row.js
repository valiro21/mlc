/**
 * Created by andreiwork on 23.04.2017.
 */
jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});