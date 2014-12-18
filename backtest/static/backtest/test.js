$(document).ready(function() {
    // Setup date picker
    $( "#start_date" ).datepicker({
        minDate: new Date(2000, 1 - 1, 1),
        defaultDate: new Date(2010, 1 - 1, 1),
        maxDate: new Date(2014, 12 - 1, 1),
        changeMonth: true,
        numberOfMonths: 1,
        stepMonths: 12,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#end_date" ).datepicker( "option", "minDate", selectedDate );
        }
    });
    $( "#end_date" ).datepicker({
        minDate: new Date(2000, 1 - 1, 1),
        defaultDate: new Date(2010, 12 - 1, 1),
        maxDate: new Date(2014, 12 - 1, 1),
        changeMonth: true,
        numberOfMonths: 1,
        stepMonths: 12,
        dateFormat: 'yy-mm-dd',
        onClose: function( selectedDate ) {
            $( "#start_date" ).datepicker( "option", "maxDate", selectedDate );
      }
    });

    // Setup form validation
    $( "#setup" )
        .bootstrapValidator({
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            start_date: {
                validators: {
                    notEmpty: {
                        message: 'The start date is required'
                    }
                }
            },
            end_date: {
                validators: {
                    notEmpty: {
                        message: 'The end date is required'
                    }
                }
            },
            initial_balance: {
                validators: {
                    notEmpty: {
                        message: 'The initial balance is required'
                    },
                    greaterThan: {
                        inclusive: true,
                        value: 1,
                        message: 'The initial balance must be equal or greater than 1'
                    }
                }
            },
            frequency: {
                validators: {
                    notEmpty: {
                        message: 'The trading frequency is required'
                    },
                    between: {
                        min: 1,
                        max: 252,
                        message: 'The trading frequency must be between 1 and 252'
                    }
                }
            },
            num_holdings:{
                validators: {
                    notEmpty: {
                        message: 'The num of holdings is required'
                    },
                    greaterThan: {
                        inclusive: true,
                        value: 1,
                        message: 'The num of holdings must be equal or greater than 1'
                    }
                }
            }
        }
    })
        // Submit form using Ajax
        .on('success.form.bv', function(e) {
            e.preventDefault();

            // Get the form instance
            var $form = $(e.target);

            // Get the BootstrapValidator instance
            var bv = $form.data('bootstrapValidator');

            // Use Ajax to submit form data
            $.post($form.attr('action'), $form.serialize(), function () {
                block_form();
            }, 'json')
                .done(function () {
                    unblock_form();
                    $("#form_ajax").show();
                    setTimeout(function () {
                        $("#form_ajax").hide();
                    }, 5000);
                })
                .fail(function () {
                    unblock_form();
                    alert('ajax error');
                });
        });

    //submit_backtest_settings
    function block_form() {
        $("#loading").show();
        $('input').attr('disabled', 'disabled');
    }

    function unblock_form() {
        $("#loading").hide();
        $('input').removeAttr('disabled');
    }

    // Get id
    var path = window.location.pathname.split('/');
    id = path[path.length-2];
    console.log(id);

    // instantiate our graph!
    var rawData = {"error": "", "data": {"date": {"key": "date", "values": ["2000-06-09", "2000-06-12", "2000-06-13", "2000-06-14", "2000-06-15", "2000-06-16", "2000-06-19", "2000-06-20", "2000-06-21", "2000-06-22"]}, "high": {"key": "high", "values": [72.81, 72.62, 71.75, 71.5, 67.94, 66.56, 69.0, 75.88, 79.94, 79.81]}, "close": {"key": "close", "values": [70.88, 66.0, 69.06, 67.75, 65.94, 62.62, 68.0, 73.62, 78.5, 75.75]}, "open": {"key": "open", "values": [69.75, 72.62, 64.5, 70.75, 67.94, 66.19, 62.12, 68.94, 73.38, 79.75]}, "low": {"key": "low", "values": [69.75, 65.25, 64.5, 67.0, 64.81, 62.0, 62.12, 68.38, 73.31, 74.38]}}};

    var dateToTimestamp = function(date) {
        return +new Date(date);
    };

    var cleanData = function(rawData) {
        var data = rawData["data"];
//        _.each(data["open"]["values"], function(elem, index, list) {
//            data["open"]["values"][index] = [dateToTimestamp(data["date"]["values"][index]), elem];
//        });
//        seriesData.push(data["open"]);
//        _.each(data["high"]["values"], function(elem, index, list) {
//            data["high"]["values"][index] = [dateToTimestamp(data["date"]["values"][index]), elem]
//        });
//        seriesData.push(data["high"]);
//        _.each(data["low"]["values"], function(elem, index, list) {
//            data["low"]["values"][index] = [dateToTimestamp(data["date"]["values"][index]), elem]
//        });
//        seriesData.push(data["low"]);
//        _.each(data["close"]["values"], function(elem, index, list) {
//            data["close"]["values"][index] = [dateToTimestamp(data["date"]["values"][index]), elem]
//        });
//        seriesData.push(data["close"]);

        return [(
            {
                key: 'returns',
                values: _.zip(data["date"], data["returns"])
            })];
    };

    var seriesData;

    // Wrapping in nv.addGraph allows for '0 timeout render', stores rendered charts in nv.graphs, and may do more in the future... it's NOT required

    var priceChart;
    nv.addGraph(function() {
        priceChart = nv.models.lineWithFocusChart()
            .margin({right: 100})
            //.useInteractiveGuideline(true)
            .x(function(d) { return d[0] })
            .y(function(d) { return d[1] })
            .transitionDuration(500)
            //.showControls(true)       //Allow user to choose 'Stacked', 'Stream', 'Expanded' mode.
            .clipEdge(true);

        priceChart.xAxis
            .tickFormat(
                function(d) {
                    return d3.time.format.utc("%Y-%m-%d")(new Date(d))
                }
            );

        priceChart.yAxis
            .tickFormat(d3.format('%,.2f'));

        priceChart.x2Axis
            .tickFormat(
                function(d) {
                    return d3.time.format.utc("%Y-%m-%d")(new Date(d))
                }
            );

        priceChart.y2Axis
            .tickFormat(d3.format('%,.2f'));

        $.ajax( {
            url: 'http://localhost:8000/backtest/result/' + id + '/' + 1,
            dataType: 'json',
            success: function(data) {
                if (data["error"].length != 0) {
                    console.log("Ajax error: " + data["error"]);
                    return;
                }
                seriesData = cleanData(data);
                console.log(seriesData);
                d3.select('#chart svg')
                    .style({
                        'min-height': '500px'
                    })
                    .datum(seriesData)
                    .call(priceChart);
                },
            error: function() {
                console.log("error loading dataURL: " + 'localhost:8000/backtest/result/' + id + '/' + 1);
            }
        } );

        nv.utils.windowResize(priceChart.update);

        priceChart.dispatch.on('stateChange', function(e) { nv.log('New State:', JSON.stringify(e)); });

        return priceChart;
    });

    var getResult = function(n) {
        $.ajax( {
            url: 'http://localhost:8000/backtest/result/'  + id + '/' + n,
            dataType: 'json',
            success: function(data) {
                if (data["error"].length != 0) {
                    console.log("Ajax error: " + data["error"]);
                    return;
                }
                //removeData(seriesData);
                addData(seriesData, data);
                d3.select('#chart svg')
                    .datum(seriesData)
                    .call(priceChart);
            },
            error: function() {
                console.log("error loading dataURL: " + 'localhost:8000/backtest/result/' + id + '/' + n);
            }
        } );
    };

    //getResult(1);

    var addData = function(oldData, newData) {
        newData = newData["data"];
        newData = _.zip(newData["date"], newData["returns"]);
        console.log(newData);
        newData.forEach(function(val, index, array) {
            oldData[0].values.push(val);
        });
        console.log(oldData);
    };

    var removeData = function(data) {
        data.forEach( function(series) {
			series["values"].shift();
		} );
    };

    var update = setInterval(function() {
        getResult(1);
    }, 10000);

    $("#stop-btn").on('click', function() {
        clearInterval(update);
    });

    $("#restart-btn").on('click', function() {
        var testResponse = {
            backtest: {
                id: id,
                start_date: "2013-01-01",
                end_date: "2014-01-01",
                initial_balance: 1000000,
                frequency: 12,
                num_holdings: 1
            },
            algorithm: {
                name : "Test",
                sma: {
                    "period1": 15,
                    "period2": 10,
                    "percent_difference_to_buy": 0.1,
                    "appetite": 5
                    }
            }
        };

        $.ajax({
                url: "/backtest/run/",
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $.cookie('csrftoken'),
                    data: JSON.stringify(testResponse)
                },
                success: function (data) {
                    console.log(data);
                    console.log("start backtest");
                },
                error: function (xhr, errmsg, err) {
                    alert("error");
                }
            });
        update = setInterval(function() {
        getResult(1);
    }, 10000);
        $("#restart-btn").prop("disabled",true);
    });
});


