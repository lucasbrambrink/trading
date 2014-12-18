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
	var token = $.cookie('csrftoken')
	console.log(token)
	$.cookie.json=true;	

	final_json_object = $.cookie('final_json_object')
	if(!final_json_object){
		final_json_object = {}
		$.cookie('final_json_object', final_json_object)
	}
	algorithm_text = $.cookie('algorithm_text')
	if(!algorithm_text){
		algorithm_text = {}
		$.cookie('algorithm_text', algorithm_text)
	}

	$('.popup_conditions').hide();
	$('.draggable').draggable();
	$('#SMA').data({
		'origionalLeft': $("#SMA").css('left'),
    	'origionalTop': $("#SMA").css('top')
	})

  	// $(".form-control").not("[0-9.]").jqBootstrapValidation(); 

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
					width: "30%",
				    height: "150px",
				    opacity: 1,
				    borderWidth: "1px"
				  }, 400 );
			});

	$('#behavior_form').submit(function(e){
		e.preventDefault();
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
		var behavior = $(this).serialize().split("=")[0]
		post_data += '&behavior=' + behavior
		console.log(post_data)
		$.ajax({
	            url: "/builder/create_json/",
	            type: "POST",
	            data: {
	                csrfmiddlewaretoken: token,
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
	            		console.log(key)
	            		var find_block_id = '#Event'
	            	} else if(key === 'ratio'){
	            		var condition = 'IF' + data.block[key][behavior][0]['range'][0] + " < " +data.block[key][behavior][0]['name'] + " < " + data.block[key][behavior][0]['range'][1] +' THEN ' + behavior + ' (' + data.block[key][behavior][0]['appetite'] + ')'
	            		console.log(key)
	            		var find_block_id = '#Ratio'
	            	} else if(key === 'thresholds') {
	            		var condition = 'Price must be between' + data.block[key][behavior][0]['range'][0] + " and " + data.block[key][behavior][0]['range'][1]
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
	                
	            	// Store in Browser
	                final_json_object = $.cookie('final_json_object')
	                JSON.parse(final_json_object)
	                final_json_object[key] = data.block
	                console.log(final_json_object[key])
	                $.cookie('final_json_object',final_json_object)
	                algorithm_text = $.cookie('algorithm_text')
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
				    width: "30%",
				    height: "150px",
				    opacity: 1,
				    borderWidth: "1px"
				  }, 400 );
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
