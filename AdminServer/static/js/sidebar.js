jQuery(document).ready(function(){
	//cache DOM elements
	var sidebar = $('.sidebar'),
	    old_type = getMq();

	if ($('#menu').children().length == 0) {
	    sidebar.remove();
	}

	$('.sidebar-item').on('click', function(event){
		var selectedItem = $(this);

        if (getMq() == 'mobile') {
            if (selectedItem.hasClass('selected')) {
                selectedItem.removeClass('selected');
            }
            else {
                var list = sidebar.find('.sidebar-item');
                for(i = 0; i < list.length; i++) {
                    $(list[i]).removeClass('selected');
                }

                selectedItem.addClass('selected');
            }
        }
        else {
            if (!selectedItem.hasClass('active')) {
                if (selectedItem.hasClass('unique')) {
                    var list = sidebar.find('.sidebar-item');
                    for(i = 0; i < list.length; i++) {
                        $(list[i]).removeClass('active');
                    }
                }
                selectedItem.addClass('active');
            }
            else {
                selectedItem.removeClass('active');
                selectedItem.addClass('no-hover');
            }
        }
	});

	$('.sidebar-item').mouseenter (function(event){
	    if (getMq () != 'mobile') {
            var selectedItem = $(this);

            if (!selectedItem.hasClass('no-hover'))
                sidebar.find('.sidebar-item.no-hover').removeClass('no-hover');

            if (!selectedItem.hasClass('selected')) {
                if (!selectedItem.hasClass('no-hover') && !selectedItem.hasClass('active')) {
                    selectedItem.addClass('selected');
                }
            }
        }
	}).mouseleave(function(event){
    	if (getMq () != 'mobile') {
	    	var selectedItem = $(this);

            if (selectedItem.hasClass('selected')) {
                selectedItem.removeClass('selected');
                sidebar.find('.no-hover').removeClass('no-hover');
            }
        }
	});

	$(document).on('click', function(event) {
	    if (getMq () != 'mobile') {
            if( !$(event.target).is('.sidebar-item') ) {
                sidebar.find('.sidebar-item.selected').removeClass('selected');
            }
		}
	});

	$( window ).resize(function() {
        type = getMq ();
        if (type != old_type) {
            if (type == 'mobile') {
                var list = sidebar.find('.sidebar-item');
                for(i = 0; i < list.length; i++){
                    $(list[i]).removeClass('selected');
                    if ($(list[i]).hasClass('active')) {
                        $(list[i]).removeClass('active');
                        $(list[i]).addClass('selected');
                    }
                }
            }
            else if (type == 'desktop') {
                var list = sidebar.find('.sidebar-item');
                for(i = 0; i < list.length; i++) {
                    if ($(list[i]).hasClass('selected')) {
                        $(list[i]).removeClass('selected');
                        $(list[i]).addClass('active');
                    }
                }
            }
            old_type = type;
        }
    });

	function getMq () {
	    var type = window.getComputedStyle(document.body).getPropertyValue('--type');
	    return type;
	}
});