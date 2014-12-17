description_text = {
	'SMA': 'The simple moving average calculates the mean stock price for two consecutive periods and compares their percent difference.',
	'Volatility': "The volatility of a given stock is defined by it's standard deviation, the average difference from the mean per data point.",
	'Covariance': 'Hello',
	'Event': "This is soemthing",
	'Thresholds': "A passive condition, this places limits on how your portfolio may behave.",
	'Diversity': "By diversifying your portfolio, you broaden your base."
}

$(document).ready(function(){	
	$('.popup_conditions').hide();
	$('.draggable').draggable();

	$('.conditionals').submit(function(e){
		e.preventDefault();
		$('#behavior_conditions').show()
				.animate({
					width: "22%",
				    height: "250px",
				    opacity: 1,
				    borderWidth: "4px"
				  }, 300 );
			});

	$('.droppable').droppable({	
 		drop: function(event, ui) {
 			$('#Sma_conditions').show()
 				.animate({
				    width: "22%",
				    height: "250px",
				    opacity: 1,
				    borderWidth: "4px"
				  }, 300 );
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
            	$('.description_header')
            		.text(id)
            	$('.description_text')
            		.text(description_text[id])

            })

});
