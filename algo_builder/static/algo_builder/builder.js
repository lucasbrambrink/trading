description_text = {
	'SMA': 'The simple moving average calculates the mean stock price for two consecutive periods. It then compares their percent difference and scores each passing stock based on your appetite.',
	'Volatility': "The volatility of a given stock is defined by its standard deviation, the average difference from the mean. This block allows you to target more volatile stocks or stay away from them depending on your risk appetite. It is scored as a percentage of the stock price (e.g. 0.1 means the stock deviates from its mean price by an average of 10% of its value.",
	'Covariance': 'Covariance allows you to compare the behavior of each stock to a benchmark (e.g. GOOG). If they are covariant (their prices move up and down together), it will score the stock based on your appetite.',
	'Event': "Simply, the event block allows you to perform a behavior based on a simple price mark. For example, if AMZN hits $320.00 per share, buy. ",
	'Thresholds': "A passive condition, this block allows your to curate your portfolio. By placing bounds on price and sector, you can set global contraints on how your portfolio acquires new shares.",
	'Diversity': "By diversifying your portfolio, you can hedge your dependencies on certain sectors or industries. Sector and industry maxima instruct the algorithm to pass over any excess shares within a given category.",
	'Build your own Algorithm': "By dragging and dropping blocks over the 'this' conditional, you can specify the behavior of your algorithm per trading session. Fill the corresponding forms and the condition will be added to your algorithm! Note: Be careful about selling conditions. The algorithm generally functions best if it is allowed to sell all your assets each time (to maximize your capital for new investments). But feel free to play around!"
}

function resetForm(A,B){
	document.getElementById(A).reset();
	document.getElementById(B).reset();
}


$(document).ready(function(){
	var token = $.cookie('csrftoken')
	console.log(token)
	$.cookie.json=true;	

	final_json_object = $.cookie('final_json_object')
	if(!final_json_object){
		final_json_object = {}
		$.cookie('final_json_object', final_json_object)
	}
	algorithm_text = $.cookie('algorithm_text')
	if(algorithm_text) {
        for (var i = 0; i < Object.keys(algorithm_text).length; i++) {
            key = Object.keys(algorithm_text)[i]
            $('#conditions_list').append("<li><h1>" + algorithm_text[key] + "</h1></li>")
        }
    }
	if(!algorithm_text){
		algorithm_text = {}
		$.cookie('algorithm_text', algorithm_text)
	}

	$('.popup_conditions').hide();
	$('.draggable').draggable().click(function(){
	});

	$('#SMA').data({
		'origionalLeft': $("#SMA").css('left'),
    	'origionalTop': $("#SMA").css('top')
	})

  	// $(".form-control").not("[0-9.]").jqBootstrapValidation(); 

  	$("#reset_button").on('click', function() {
  		algorithm_text = {}
		$.cookie('algorithm_text', algorithm_text)
		$('#conditions_list').empty();
	});

	$(".cancel_button").click(function() {

		var block_id = $(this).attr('id').split("_")[0];
		form_id = "#" + block_id + "_conditions"
		$(form_id).animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 400);
		$('#behavior_conditions').animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 400);
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
					width: "100%",
				    height: "100%",
				    opacity: 1,
				    borderWidth: "1px"
				  }, 400 );
			});

	$('#behavior_form').submit(function(e){
		e.preventDefault();
		var behavior = $(this).serialize().split("=")[1]
		console.log('behavior' + behavior)
		post_data += '&behavior=' + behavior
		console.log(post_data)
		resetForm(virgin_form_id,'behavior_form')
		$('.popup_conditions').animate({
			width: '0px',
			height: '0px',
			opacity: 0,
			borderWidth: '0px'
		}, 600);
		var splits = post_data.split('&')
		var block_id_pair = splits[splits.length-1]
		var block_id = "#" + block_id_pair.split('=')[1]
		console.log(block_id)
		$(block_id).show()
			.css({
				'top': $("#SMA").data('origionalTop'),
				'left': $("#SMA").data('origionalLeft'),
			})
		$.ajax({
	            url: "/builder/create_json/",
	            type: "POST",
	            data: {
	                csrfmiddlewaretoken: token,
	                data: post_data
	            },
	            success: function (data) {
	            	var key = Object.keys(data.block)[0]
	            	console.log(Object.keys(data.block))
	 				if(data.block[key]['buy'].length > 0){
	 					var behavior = 'buy'
	 				} else {
	 					var behavior = 'sell'
	 				}
	 				console.log(key)
	 				if(key === 'sma'){
	            		var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < %change SMA ( "+data.block[key][behavior][0]['period1']+","+data.block[key][behavior][0]['period2']+" ) < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ")"
	               		var find_block_id = '#SMA'
	               	} else if(key === 'volatility'){
	               		var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < Volatility ( "+data.block[key][behavior][0]['period']+") < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ')'
						var find_block_id = '#Volatility'
					} else if(key == 'covariance'){
						var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < Covariance ( "+data.block[key][behavior][0]['period']+") < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ')'
						var find_block_id = '#Covariance'
	            	} else if(key === 'event') {
	            		var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < Price of " +data.block[key][behavior][0]['stock'] + " < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ')'
	            		var find_block_id = '#Event'
	            	} else if(key === 'ratio'){
	            		var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < " +data.block[key][behavior][0]['name'] + " < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ')'
	            		var find_block_id = '#Ratio'
	            	} else if(key === 'thresholds') {
	            		var condition = 'Price must be between ' + data.block[key][behavior][0]['price_range'][0] + " and " + data.block[key][behavior][0]['price_range'][1]
	            		if(data.block[key][behavior][0]['sector']['include']){ 
	            			condition += 'and include '
	            			for(var i; i < data.block[key][behavior][0]['sector']['include'].length; i++){
	            				condition += data.block[key][behavior][0]['sector']['include'][i].toString()
	            				if(i+1 < data.block[key][behavior][0]['sector']['include'].length){
	            					condition += ","
	            				}
	            			}
	            		}
	            		if(data.block[key][behavior][0]['sector']['exclude']){ 
	            			condition += 'and exclude '
	            			for(var i; i < data.block[key][behavior][0]['sector']['exclude'].length; i++){
	            				condition += data.block[key][behavior][0]['sector']['exclude'][i].toString()
	            				if(i+1 < data.block[key][behavior][0]['sector']['exclude'].length){
	            					condition += ","
	            				}
	            			}
	            		}
	            		console.log(key)
	            		var find_block_id = '#Thresholds'
	            	} else if(key === 'diversity') {
	            		var condition = 'Portfolio cannot contain more than ' + data.block[key][behavior][0]['num_sector'] + " and " +data.block[key][behavior][0]['num_industry']+" of the same sector and industry, respectively"
	       				console.log(key)
	            		var find_block_id = '#Diversity'
	            	}
	            	$('#conditions_list').append("<li><h1>"+condition+"</h1></li>")

            		$(find_block_id).show()
						.css({
							'top': $("#SMA").data('origionalTop'),
							'left': $("#SMA").data('origionalLeft'),
					});


	            	// Store in Browser
	                final_json_object = $.cookie('final_json_object')
	        		final_json_object[key] = data.block[key]
	                console.log(final_json_object)
	                $.cookie('final_json_object',final_json_object)
	                algorithm_text = $.cookie('algorithm_text')
	                console.log(algorithm_text)
	                algorithm_text[key] = condition
	                $.cookie('algorithm_text',algorithm_text)
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
		}, 400);

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
				    width: "100%",
				    height: "100%",
				    opacity: 1,
				    borderWidth: "1px"
				  }, 400 );
 			$(ui.draggable).hide()
		}
	});

    $('.draggable').mouseover(
    	function() {
        	var id = $(this).attr('id');
        	$('.description_header')
        		.text(id)
        	$('.description_text')
        		.text(description_text[id])
    		$('.droppable').css('border','1px solid black')
    			.css('box-shadow', '7px 7px 5px #888888')
    			.css('padding-top','0px')
    			.css('background-color', 'rgba(0, 0, 0, 0.1)')
    			.css('border-radius','10px')
    });
    $('.draggable').mouseout(
    	function() {
    		var id = 'Build your own Algorithm'
    		$('.droppable').css('border','none')
    			.css('box-shadow', 'none')
    			.css('padding-top','1px')
    			.css('background-color', 'rgba(255, 255, 255, 0)')
    		$('.description_header')
        		.text(id)
        	$('.description_text')
        		.text(description_text[id])
  });
});
