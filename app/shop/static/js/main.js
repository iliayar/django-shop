;(function () {
    'use strict';

    var contentWayPoint = function() {
	var i = 0;
	$('.animate-box').waypoint( function( direction ) {
	    if(direction == 'down') {
		var el = $(this.element);
		el.addClass('fadeInUp animated');
		el.removeClass('animate-box');
	    }
	} , { offset: '95%' } );
    };

    var openImg = function (src) {
	var viewer = $('#imgViewer')
	viewer.removeAttr('hidden')
	$('#viewerImg').attr('src', src)
    };
    var closeImg = function(){
	var viewer = $('#imgViewer')
	viewer.attr('hidden', '0')
    };

    // Document on load.
    $(function(){

	contentWayPoint();
	
	$('.viewable').click(e => {
	    openImg($(e.target).attr('src'))
	})

	$('#imgViewer').click(closeImg)

    });


}());
