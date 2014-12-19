$(document).ready(function() {
    var update
        , dataCache;

    /**** Backtest environment setup ****/
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
        .find('[name="start_date"]')
            // Revalidate the start date when it is changed
            .change(function(e) {
                $('#setup').bootstrapValidator('revalidateField', 'start_date');
            })
            .end()
        .find('[name="end_date"]')
            // Revalidate the end date when it is changed
            .change(function(e) {
                $('#setup').bootstrapValidator('revalidateField', 'end_date');
            })
            .end()
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
                .done(function (data) {
                    unblock_form();
                    $("#form_ajax").show();
                    setTimeout(function () {
                        $("#form_ajax").hide();
                    }, 5000);
                    console.log(data);
                    backtest_id = data.backtest_id;

                    // Start update graph
                    update = setInterval(function() {
                        updatePage();

                        // Tried 10 times with errors, stop update
                        if (updateTry < 0) {
                            clearInterval(update);
                        }
                    }, updateRate);
                })
                .fail(function (data) {
                    unblock_form();
                    alert('ajax error');
                    console.log(data.error);
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

    /**** Setup datatables ****/
    $.fn.dataTableExt.sErrMode = 'throw';

    /**** Assets Table Configuration ****/
    var assetsUrlBase = 'http://localhost:8000/backtest/assets/';

    // Setup empty data table
    var assetsTable = $('#assets').DataTable( {
        "ordering": true,
        "searching": false,
        "columns": [
            { "data": "stock.symbol"},
            { "data": "quantity"},
            { "data": "price_purchased"}
        ],
        "ajax": {
            "dataSrc": ""
        }
    } );

    // update table
    function updateAssetsTable(date) {
        // Reload data
        assetsTable.ajax.url( assetsUrlBase + backtest_id + '/' + date ).load();
    }


    /**** Risk Metrics Table Configuration ****/
    /**** Assets Table Configuration ****/
    var riskMetricsUrlBase = 'http://localhost:8000/backtest/risks/';

    // Setup empty data table
    var riskMetricsTable = $('#riskmetrics').DataTable( {
        "ordering": true,
        "searching": false,
        "columns": [
            { "data": "alpha"},
            { "data": "beta"},
            { "data": "sharpe"},
            { "data": "volatility"},
            { "data": "returns"}
        ],
        "paging": false,
        "ajax": {
            "dataSrc": ""
        }
    } );

    // update table
    function updateRiskMetricsTable(date) {
        // Reload data
        riskMetricsTable.ajax.url( riskMetricsUrlBase + backtest_id + '/' + date ).load();
    }


    /**** Graph Configuration ****/
    var backtest_id = ''
        , seriesData = [{
            "key": "returns",
            "values": [[]]
        }]
        , returnsChart
        , updateTry = 10
        , updateRate = 3000
        , dataPointsPerUpdate = 1
        , lastTimestamp;

    // Generate returns graph
    generateGraph();

    // Change date into timestamp
    var dateToTimestamp = function(date) {
        return +new Date(date);
    };

    // Change timestamp into date
    var timestampToDate = function(timestamp) {
        var date = new Date(timestamp);
        date = date.toLocaleDateString();
        date = date.split('/');
        var year = date.pop();
        date.unshift(year);
        date = date.join('/');
        return date
    };

    var cleanData = function(rawData) {
        var data = rawData["data"];
        return [(
            {
                key: 'returns',
                values: _.zip(data["date"], data["returns"])
            })];
    };

    // Wrapping in nv.addGraph allows for '0 timeout render', stores rendered charts in nv.graphs, and may do more in the future... it's NOT required

    function generateGraph() {
        nv.addGraph(function() {
        returnsChart = nv.models.lineWithFocusChart()
            .margin({right: 100})
            //.useInteractiveGuideline(true)
            .x(function(d) { return d[0] })
            .y(function(d) { return d[1] })
            .transitionDuration(500)
            //.showControls(true)       //Allow user to choose 'Stacked', 'Stream', 'Expanded' mode.
            .clipEdge(true);

        returnsChart.xAxis
            .tickFormat(
                function(d) {
                    return d3.time.format.utc("%Y-%m-%d")(new Date(d))
                }
            );

        returnsChart.yAxis
            .tickFormat(d3.format('%,.2f'));

        returnsChart.x2Axis
            .tickFormat(
                function(d) {
                    return d3.time.format.utc("%Y-%m-%d")(new Date(d))
                }
            );

        returnsChart.y2Axis
            .tickFormat(d3.format('%,.2f'));


        console.log(seriesData);
        d3.select('#chart svg')
            .style({
                'min-height': '500px'
            })
            .datum(seriesData)
            .call(returnsChart);

        nv.utils.windowResize(returnsChart.update);

        // Add event listener for hover data points in graph
        var dispatch = d3.dispatch('updateTables');
        returnsChart.lines.dispatch.on('elementMouseover.updateTables', function(e) {
            console.log(e);
            var point = e.point;
            var date = timestampToDate(point[0]);
            updateAssetsTable(date);
            updateRiskMetricsTable(date);
    });

        return returnsChart;
        });
    }

    var updateChart = function(n) {
        $.ajax( {
            url: 'http://localhost:8000/backtest/realtime/' + backtest_id + '/' + n,
            dataType: 'json',
            success: function(data) {
                if (data["error"].length != 0) {
                    console.log("Ajax error: " + data["error"]);
                    updateTry -= 1;
                    return;
                }
                //removeData(seriesData);
                addData(seriesData, data);
                d3.select('#chart svg')
                    .datum(seriesData)
                    .call(returnsChart);

                // The last date
                lastTimestamp = data.data.date[n-1];
            },
            error: function() {
                console.log("error loading dataURL: " + 'http://localhost:8000/backtest/realtime/' + backtest_id + '/' + n);
                updateTry -= 1;
            }
        } );
    };

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

    $("#stop_btn").on('click', function() {
        clearInterval(update);
    });

    $("#continue_btn").on('click', function() {
        updateRate = 10;
        update = setInterval(function() {
            updatePage();
            if (updateTry < 0) {
                clearInterval(update);
            }
    }, updateRate);
    });

    var updatePage = function() {
        updateChart(dataPointsPerUpdate);

        // Covert timestamp to YYYY/MM/DD
        if (lastTimestamp != undefined) {
            var lastDate = timestampToDate(lastTimestamp);
            updateAssetsTable(lastDate);
            updateRiskMetricsTable(lastDate);
        }
    }
});


