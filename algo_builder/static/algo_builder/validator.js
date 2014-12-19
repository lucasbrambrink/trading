$(document).ready(function(){
	$( "#SMA_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            period1: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            period2: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            range0: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            range1: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            appetite: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    }); 
    $( "#Covariance_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            period: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }

                }
            },
            range0: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            range1: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            appetite: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    });
    $( "#Volatility_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            period: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }

                }
            },
            range0: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            range1: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            appetite: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    });
    $( "#Event_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            stock: {
                validators: {
                    stringCase: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            price: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
            appetite: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    });
    $( "#Threshold_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            price_range0: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }

                }
            },
            price_range1: {
                validators: {
                    digits: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    });
    $( "#Diversity_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            num_sector: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }

                }
            },
            num_industry: {
                validators: {
                    integer: {
                        message: ''
                    },
                    notEmpty: {
                        message: ''
                    }
                }
            },
        }
    });
    $( "#Ratio_form" )
        .bootstrapValidator({
        feedbackIcons: {
            // valid: 'glyphicon glyphicon-ok',
            // invalid: 'glyphicon glyphicon-remove',
            // validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            range0: {
                validators: {
                    digits: {
                        message: ''
                    }

                }
            },
            range1: {
                validators: {
                    digits: {
                        message: ''
                    }
                }
            },
            appetite: {
                validators: {
                    integer: {
                        message: ''
                    }
                }
            },
        }
    });
});
