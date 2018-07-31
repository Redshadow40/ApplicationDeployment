var tables;

$(document).ready(function() {
	var javalog = $('#loginfo').text();
	if (javalog == '')
		$('#log').html('<font color="#767a7e">salt log output...</font>');
	else
		$('#log').html(javalog);
        $('#ApplyID').click(function(event){
                $('#ChkApply').attr("value", "true");
                formSubmit(event);
        });
        $('#ResetTables').click(function(event){
                $('#ChkReset').attr("value", "true");
                formSubmit(event);
        });
	$('.tableInput').change(entityCheck);
	setInterval(function(){
		checkJobs();
	}, 10000);
});
function checkJobs(){
	$.getJSON("/activeTables/", function(data){
		var jobs = data['jobs'];
		for (var table in tables){
			if (jobs.includes(table)){
				$('#'+table).text(table + '(active job)');
				$('#'+table+'Num').attr('disabled', 'true');
				$('#'+table+'Num').css('opacity', '.5');
				$('#'+table+'Box').attr('disabled', 'true');
                                $('#'+table+'Box').css('opacity', '.5');
			}
			else {
				$('#'+table).text(table);
                                $('#'+table+'Num').removeAttr('disabled', 'false');
                                $('#'+table+'Num').css('opacity', '1');
                                $('#'+table+'Box').removeAttr('disabled', 'false');
                                $('#'+table+'Box').css('opacity', '1');
			}
		}
	});
}
function entityCheck(){
	if (this['type'] == 'number')
       	{
              	if (this['value'] < 1){
			var oldID = tables[this['name']].substring(1);
                        this['value'] = oldID;
                	alert("Incorrect Entity ID Value");
        	}
		else{
			var dup = false;
			for (var table in tables){
				var currentID = tables[table].toString();	
				if (table != this['name'] && parseInt(currentID.substring(1)) == this['value']){
					var oldID = tables[this['name']].substring(1);
		                        this['value'] = oldID;
                		        alert("Duplicate Entity ID Value found");
					dup = true;
					break;
				}
			}
			if (!dup){
				tables[this['name']] = newIDSetup(this['value']);
			}
		}
   	}
}
function newIDSetup(number){
	var newID = number.toString();
	if (newID.length < 2)
                return 'l00' + newID;
        else if (newID.length < 3)
                return 'l0' + newID;
        else
                return 'l' + newID;
}
function formSubmit(event){
	$('#basediv').css("opacity", ".5");
        $('#basefooterdiv').css("opacity", ".5");
        $('#tableform').trigger('submit');
        $('.tableInput').attr("disabled", "true");
        $('.loader').css("opacity", "1");
        $('.loader').css("display", "inline");
}
function selectAll(source) {
        checkboxes = document.getElementsByName('tableReset[]');
        for (var i=0; i < checkboxes.length; i++)
                if (!checkboxes[i].disabled)
                        checkboxes[i].checked = source.checked;
        enableReset();
}
function enableReset(){
  	checkboxes = document.getElementsByName('tableReset[]');
  	var checked = true;
  	for (var i = 0; i < checkboxes.length; i++){
    		if (checkboxes[i].checked == true){
      			checked = false;
    		}
    		$('#ResetTables').attr('disabled', checked);
  	}
}
function setTables(tableList){
	tables = tableList;
}
