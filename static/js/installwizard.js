var currentStage = 0;
var jobRunning = false;

$(document).ready(function(){
	setInterval(function(){
		installationRunningStatus();
        }, 2000);
	$('#next-button').click(function(){
		switch (currentStage){
			case 0:
				$('#install-object').attr('data', '/uploadpp/');
				$('#back-button').removeAttr('disabled');
				installFileFound();
				currentStage += 1;
				break;
			case 1:
				$('#install-object').attr('data', '/sitesurvey/');
                                currentStage += 1;
                                break;
			case 2:
				$('#install-object').attr('data', '/review/');
				$('#next-button').html('Install');
                                currentStage += 1;
                                break;
			case 3:
				beginInstallation();
				$('#install-object').attr('data', '/installpp/');
				$('#next-button').attr('disabled', true);
				$('#back-button').attr('disabled', true);
				$('#cancel-button').attr('disabled', true);
				$('#next-button').html('Installing...');
				currentStage += 1;
				break;
			case 4:
				$('#install-object').attr('data', '/finishinstall/');
				$('#next-button').attr('disabled', true);
                                $('#back-button').attr('disabled', true);
				$('#cancel-button').removeAttr('disabled');
				$('#cancel-button').html('Return');
				break;
		}
	});
	$('#back-button').click(function(){
                switch (currentStage){
                        case 1:
				$('#back-button').attr('disabled', true);
                                $('#install-object').attr('data', 'startinstall/');
				$('#next-button').removeAttr('disabled');
                                currentStage -= 1;
                                break;
                        case 2:
                                $('#install-object').attr('data', '/uploadpp/');
				installFileFound();
                                currentStage -= 1;
                                break;
			case 3:
				$('#install-object').attr('data', '/sitesurvey/');
                                $('#next-button').html('Next >');
                                currentStage -= 1;
                                break;
                }
        });
	$('#cancel-button').click(function(){
		currentStage = 0;
		$('#back-button').attr('disabled', true);
		$('#next-button').html('Next >');
		$('#next-button').removeAttr('disabled');
		$('#install-object').attr('data', 'startinstall/');
	});
});
function checkCurrentStatus(){
        if (currentStage == 1)
	        installFileFound();
}
function installFileFound(){
	$.getJSON("/checkInstallFile/", function(data){
		if (!data['filefound'])
			$('#next-button').attr('disabled', true);
		else
			$('#next-button').removeAttr('disabled');
	});
}
function beginInstallation(){
        $.getJSON("/beginInstallPP/");
	jobRunning = true;
}
function installationRunningStatus(){
	if (currentStage == 4 && jobRunning) { 
	        $.getJSON("/checkJobStatus/", function(data){
        	        if (!data['isalive']){
                	        jobRunning = false;
				$('#next-button').html('Next >');
				$('#next-button').removeAttr('disabled');
			}
        	});
	}
}
