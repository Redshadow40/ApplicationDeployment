var first_position = {
	left: 20,
	bottom: 30,
	available: true,
};
var second_position = {
	left: 25,
        bottom: 25,
        available: true,
};
var third_position = {
	left: 30,
        bottom: 20,
        available: true,
};
var fourth_position = {
	left: 35,
        bottom: 15,
        available: true,
};

var application_position = [first_position, second_position, third_position, fourth_position];

$(document).ready(function(){
	setTime();
	$('#start').click(function(){
		if ($('#startmenu').css('display') == 'none')
			$('#startmenu').css('display', 'inline');
		else
			$('#startmenu').css('display', 'none');
	});
	$('#application-screen, .application-zone, .application-menu, .application-content').click(function(){
		$('#startmenu').css('display', 'none');
	});
	$('.menuleft button, .menuright button').click(function(){
		switch($(this).attr('id')){
			case "Filemanage-button":
				createApplicationWindow("filemanage/");
				break;
			case "TableEntityID-button":
				createApplicationWindow("tableentityid/");
				break;
			case "Validate-button":
				createApplicationWindow("validation/");
				break;
			case "InstallPP-button":
				createApplicationWindow("installpp/");
                                break;
			case "Sitesurvey-button":
                                createApplicationWindow("sitesurvey/");
                                break;
			case "Upload-button":
				createApplicationWindow("uploadpp/");
				break;
			case "Installwizard-button":
				createApplicationWindow("installwizard/");
				break;
		}
		$('#startmenu').css('display', 'none');
	});

	setInterval(function(){
		setTime()
	}, 5000);
});

function setTime(){
	var date = new Date();
	var hour = date.getHours();
	var twelvehour = "AM";
	if (hour > 12){
		hour = (hour - 2) % 10;
		twelvehour = "PM";
	}
	var minutes = date.getMinutes();
	$('#time').html("<h4>" + hour + ":" + ((minutes < 10)?"0" + minutes: minutes) + " " + twelvehour + "</h4>");
}

function createApplicationWindow(site_address){
	var content = $('#application-screen').html();
	var count = (content.match(/application-zone/g) || []).length;

	if (count > 3)
		alert("Too many applications open, how about closing some first");
	else{
		var position = null;
		for (var i = 0; i < application_position.length; i++){
			if (application_position[i].available){
				application_position[i].available = false;
				position = application_position[i];
				break;
			}
		}
		if (!position){
			alert("something went wrong with opening application");
			return;
		}
		newContent = `<div class="application-zone" id="${position.left}${position.bottom}" style="left: ${position.left}%; bottom: ${position.bottom}%; z-index: 4"> 
                                <div class="application-outline">
                                        <div class="application-menu" data-name="${position.left}${position.bottom}" onclick="bringToFront(this)">
						<font color="white">${site_address}</font>
                                                <button type="button" value="${position.left}${position.bottom}" class="button application-close-button" onclick="closeApplicationWindow(this)">X</button>
                                        </div>
                                        <div class="application-content" data-name="${position.left}${position.bottom}" onclick="bringToFront(this)">
                                                <object type="text/html" data="${site_address}" style="width: 100%; height: 100%;"></object>
                                        </div>
                                </div>
                        </div>`;
		$('#application-screen').append(newContent);
		decrementIndex((position.left).toString() + (position.bottom).toString());
		createTaskbarApp((position.left).toString() + (position.bottom).toString(), site_address);
	}
}

function createTaskbarApp(id, site_address){
	newContent = `<td id="${id}task" style="width: 155px">
			<div class="taskbar-application" data-name="${id}" onclick="bringToFront(this)">
				${site_address}
			</div>			
		</td>`;

	$('#taskbar-content').append(newContent);
}

function decrementIndex(idUsed){
	for (var i = 4; i > 1;i--){
		var found = false;
		for (var y = 0; y < application_position.length; y++){
			if (!application_position[y].available){
				var id = (application_position[y].left).toString() + (application_position[y].bottom).toString();
				var currentZ = parseInt($('#' + id).css('z-index'));
				if (idUsed != id && currentZ == i){
					found = true;
					currentZ -= 1;
					$('#' + id).css('z-index', currentZ.toString());
					idUsed = id;
					break;
				}
			}
		}
		if (!found)
			break;
	}
}

function bringToFront(item){
	var id = item.getAttribute("data-name");
	$('#' + id).css('z-index', '4');
	decrementIndex(id);
}

function closeApplicationWindow(item){
	var id = item.value;
	$('#' + id).remove();
	$('#' + id + 'task').remove();
	for (var i = 0; i < application_position.length; i++){
		if ((application_position[i].left == parseInt(id.slice(0,2))) && (application_position[i].bottom == parseInt(id.slice(2)))){
			application_position[i].available = true;
			break;
		}
	}	
}
