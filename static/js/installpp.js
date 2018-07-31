var jobRunning = false;
var logPosition = 0;

$(document).ready(function(){
	installationRunningStatus();
	setInterval(function(){
		activeInstallPP();
	}, 2000);
});
function installationRunningStatus(){
	$.getJSON("/checkJobStatus/", function(data){
		if (data['isalive']){
			jobRunning = true;
		} else {
			jobRunning = false;
			if ($('#progress-bar').attr('aria-valuenow') != "0" && $('#progress-bar').attr('aria-valuenow') != "100")
				$('#progress-bar').attr('class', 'progress-bar bg-danger');
		}
	});
}
function activeInstallPP(){
        if (jobRunning){
                $.getJSON("activeInstallPP/" + logPosition, function(data){
                        for (var x in data['activeInstall']){
				if (data['activeInstall'][x].includes('passed'))
	                                $('#log').html($('#log').html() + '<img src="/static/images/checkmark.png">' + (data['activeInstall'][x]).replace(" - passed", "").replace(/_/g, " ") + '<br>');
				else if (data['activeInstall'][x].includes('failed'))
					$('#log').html($('#log').html() + '<img src="/static/images/xmark.png">' + (data['activeInstall'][x]).replace(" - failed", "").replace(/_/g, " ") + '<br>');
				else if (data['activeInstall'][x].includes('No changes made'))
					$('#log').html($('#log').html() + '<img src="/static/images/checkmark.png">Stage already Installed<br>');
                                $('#log').scrollTop($('#log')[0].scrollHeight);
				logPosition++;
                        }
			var percentDone = Math.floor((parseInt(data['stagesDone'])/parseInt(data['stageCount'])) * 100);
			$('#progress-bar').css('width', percentDone + '%');
			$('#progress-bar').attr('aria-valuenow', percentDone);
			$('#progress-bar').html(percentDone + '%');
			if (percentDone == 100)
				$('#progress-bar').attr('class', 'progress-bar bg-success');
                });
        }
	installationRunningStatus();
}
