var jobRunning = false;
var logPosition = 0;

$(document).ready(function(){
	validationRunningStatus();
	$('#validatebtn').click(function(){
		$('#validatebtn').attr('disabled', 'disabled');
		$('#validatebtn').val('Validating...');
		$('#log').css('display', 'block');
		$('#log').html('');
		beginValidation();
		jobRunning = true;
		logPosition = 0;
	});
	setInterval(function(){
		activeValidationPP()
	}, 2000);
});
function validationRunningStatus(){
	$.getJSON("/checkJobStatus/", function(data){
		if (data['isalive']){
			$('#validatebtn').attr('disabled', 'disabled');
			if (data['typeofJob'] == 'Validation'){
				$('#validatebtn').val('Validating...');
				$('#log').css('display', 'block');
			}else{
				$('#validatebtn').val('Busy...');
                                $('#log').css('display', 'block');
                                $('#log').html("There is currently a running job: " + data['typeofJob']);
			}
			jobRunning = true;
		}	
		else if (filefound){
			$('#validatebtn').removeAttr('disabled', 'disabled');
			$('#validatebtn').val('Validate');
			jobRunning = false;
		}
	});
}
function beginValidation(){
	$.getJSON("beginValidationPP/", function(data){
		$('#log').html($('#log').html() + data['validate'] + '<br>');
        });
}
function activeValidationPP(){
        if (jobRunning){
                $.getJSON("activeValidationPP/" + logPosition, function(data){
                        for (var x in data['activeValidate']){
				if (data['activeValidate'][x].toLowerCase().includes('passed'))
	                                $('#log').html($('#log').html() + '<font color="green">' + data['activeValidate'][x] + '</font><br>');
				else if (data['activeValidate'][x].toLowerCase().includes('failed'))
					$('#log').html($('#log').html() + '<font color="red">' + data['activeValidate'][x] + '</font><br>');
				else if (data['activeValidate'][x].toLowerCase().includes('completed'))
					$('#log').html($('#log').html() + '<font color="blue">' + data['activeValidate'][x] + '</font><br>');
				else
					$('#log').html($('#log').html() + data['activeValidate'][x] + '<br>');
                                $('#log').scrollTop($('#log')[0].scrollHeight);
				logPosition++;
                        }
                });
                validationRunningStatus();
        }
}
