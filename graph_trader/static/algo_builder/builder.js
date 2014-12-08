$(document).ready(function(){	
	$('.draggable').draggable();

	$('.droppable').droppable({	
 		drop: function(event, ui) {
 			// possible to run AJAX post/get request if we want
 			$(ui.draggable).css('color','white');
    		$( this )
    		  .addClass( "ui-state-highlight" )
	          .css('background-color','green')
	          .css('color','white')
	          .find( "p" )
	            .html( "Dropped!" );
            $(this.ui)
    		}
  		});
});
