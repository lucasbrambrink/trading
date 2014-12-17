description_text = {
	'SMA': 'The simple moving average calculates the mean stock price for two consecutive periods and compares their percent difference.',
	'Volatility': "The volatility of a given stock is defined by its standard deviation, the average difference from the mean. This block allows you to target more volatile stocks or stay away from them depending on your risk appetite. It is scored as a percentage of the stock price (e.g. 0.1 means the stock deviates from its mean price by an average of 10% of its value.",
	'Covariance': 'Hello',
	'Event': "This is soemthing",
	'Thresholds': "A passive condition, this places limits on how your portfolio may behave.",
	'Diversity': "By diversifying your portfolio, you broaden your base."
}

function resetForm(A,B){
	document.getElementById(A).reset();
	document.getElementById(B).reset();
}

$(document).ready(function(){	
	final_json_object = $.cookie('final_json_object')
	if(!final_json_object){
		final_json_object = {}
		$.cookie('final_json_object', final_json_object)
	}
	algorithm_text = $.cookie('algorithm_text')
	if(!algorithm_text){
		algorithm_text = []
		$.cookie('algorithm_text', algorithm_text)
	}

	$('.popup_conditions').hide();
	$('.draggable').draggable();
	$('#SMA').data({
		'origionalLeft': $("#SMA").css('left'),
    	'origionalTop': $("#SMA").css('top')
	})



	$(".cancel_button").click(function() {

		var block_id = $(this).attr('id').split("_")[0];
		form_id = "#" + block_id + "_conditions"
		$(form_id).animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 300);
		find_block_id = "#" + block_id
		$(find_block_id).show()
			.css({
				'top': $("#SMA").data('origionalTop'),
				'left': $("#SMA").data('origionalLeft'),
			})
    });


	$('.conditionals').submit(function(e){
		e.preventDefault();
		form_id = '#' + $(this).attr('id')
		virgin_form_id = $(this).attr('id')
		post_data = $(this).serialize() + '&id=' + $(this).attr('id').split('_')[0]	
		$('#behavior_conditions').show()
				.animate({
					width: "22%",
				    height: "250px",
				    opacity: 1,
				    borderWidth: "4px"
				  }, 300 );
			});

	$('#behavior_form').submit(function(e){
		e.preventDefault();
		resetForm(virgin_form_id,'behavior_form')
		$('.popup_conditions').animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 300);
		$('#behavior_form').animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 300);
		var splits = post_data.split('&')
		var block_id_pair = splits[splits.length-1]
		var block_id = "#" + block_id_pair.split('=')[1]
		console.log(block_id)
		$(block_id).show()
			.css({
				'top': $("#SMA").data('origionalTop'),
				'left': $("#SMA").data('origionalLeft'),
			})
		var behavior = $(this).serialize().split("=")[0]
		post_data += '&behavior=' + behavior
		console.log(post_data)
		$.ajax({
	            url: "/builder/create_json/",
	            type: "POST",
	            data: {
	                csrfmiddlewaretoken:$.cookie('csrftoken'),
	                data: post_data
	            },
	            success: function (data) {
	            	var key = Object.keys(data.block)[0]
	 				if(data.block[key]['buy'].length > 0){
	 					var behavior = 'buy'
	 				} else {
	 					var behavior = 'sell'
	 				}
	 				console.log(data.block[key][behavior][0])
	            	if(key === 'sma'){
	            		var condition = 'IF the average price of the last ' + data.block[key][behavior][0]['period1'] + ' days differs from the previous ' + data.block[key][behavior][0]['period2'] +' days by a percent difference between ' + data.block[key][behavior][0]['range'][0] + '% and ' + data.block[key][behavior][0]['range'][1] +'%, THEN ' + behavior + ' with an appetite of ' + data.block[key][behavior][0]['appetite']
	               		var find_block_id = '#SMA'
	               	} else if(key === 'volatility' || key === 'covariance') {
	               		console.log(key)
	               		if(key==='volatility'){var find_block_id = '#Volatility'}
               			else {var find_block_id = '#Covariance'}
	            	} else if(key === 'event') {
	            		console.log(key)
	            		var find_block_id = '#Event'
	            	} else if(key === 'ratio'){
	            		console.log(key)
	            		var find_block_id = '#Ratio'
	            	} else if(key === 'thresholds') {
	            		console.log(key)
	            		var find_block_id = '#Thresholds'
	            	} else if(key === 'diversity') {
	            		console.log(key)
	            		var find_block_id = '#Diversity'
	            	}
	            	$('#conditions_list').append("<li><h1>"+condition+"</h1></li>")
	                
	            	// Store in Browser
	                final_json_object = $.cookie('final_json_object')
	                final_json_object[key] = data.block
	                $.cookie('final_json_object',final_json_object)
	                console.log(final_json_object)
	                console.log(data);

	            },
	            error: function (xhr, errmsg, err) {
	                alert("error");
	            }
	        },'json');
	});

	$("#behavior_cancel").click(function() {
		$('.popup_conditions').animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 300);

		var splits = post_data.split('&')
		var block_id_pair = splits[splits.length-1]
		var block_id = "#" + block_id_pair.split('=')[1]
		$(block_id).show()
			.css({
				'top': $("#SMA").data('origionalTop'),
				'left': $("#SMA").data('origionalLeft'),
			}) // ('display','block');
    });

	$('.droppable').droppable({	
 		drop: function(event, ui) {
 			var match_to_block = $(ui.draggable).attr('id')
			var match_to_form = "#" + $(ui.draggable).attr('id') + "_conditions";
 			$(match_to_form).show()
 				.animate({
				    width: "22%",
				    height: "250px",
				    opacity: 1,
				    borderWidth: "4px"
				  }, 300 );
 			$(ui.draggable).hide()
		}
	});

    $('.draggable').hover(
    	function() {
        	var id = $(this).attr('id');
        	$('.description_header')
        		.text(id)
        	$('.description_text')
        		.text(description_text[id])

    });


});
