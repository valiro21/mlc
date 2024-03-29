/**
 * Created by vrosca on 6/3/17.
 */
var bodyLayout;
jQuery(document).ready(function () {
    jQuery.browser = {};
    (function () {
        jQuery.browser.msie = false;
        jQuery.browser.version = 0;
        if (navigator.userAgent.match(/MSIE ([0-9]+)\./)) {
            jQuery.browser.msie = true;
            jQuery.browser.version = RegExp.$1;
        }
    })();

    jQuery.curCSS = function(element, prop, val) {
        return jQuery(element).css(prop, val);
    };

    bodyLayout = $("body").layout({
        north: {
            enableCursorHotkey: false,
            resizable: false,
            spacing_open: 0,
            spacing_closed: 0,
            showOverflowOnHover: true
        },
        west: {
            showOverflowOnHover: true
        },
        center: {
            showOverflowOnHover: true
        }
    });

    bodyLayout.sizePane("north", 80);
    bodyLayout.allowOverflow("north");
    bodyLayout.sizePane("east", 0);
});
