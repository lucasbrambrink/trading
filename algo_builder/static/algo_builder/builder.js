$(document).ready(function(){	
	$('#sma_conditions').hide();
	$('.draggable').draggable();

	$('.droppable').droppable({	
 		drop: function(event, ui) {
 			$('#sma_conditions').show()
 				.animate({
				    width: "45%",
				    height: "55%",
				    opacity: 1,
				    fontSize: "3em",
				    borderWidth: "4px"
				  }, 500 );
 			// possible to run AJAX post/get request if we want
 			$(ui.draggable).hide()
 			$(ui.draggable).css('color','white');
    		$( this )
	          .css('background-color','green')
	          // .css('color','white')
	          .find( "p" )
	            .html( "Dropped!" );
            $(this.ui)
    		}
  		});

	    $('.draggable').hover(
	    	function() {
            	var id = $(this).attr('id');
            	console.log(id)
            	console.log()
            	$('.description_header')
            		.text(id)
            	$('.description_text')
            		.text("SMA is very interesting indeed")

            })

});
