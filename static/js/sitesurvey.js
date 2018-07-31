$(document).ready(function(){
        var siteInfo = $('#siteInfo').text();
        if (siteInfo != 'None')
                $('#sitesurveyTable').html(siteInfo);
        else {
                $('#sitesurveyTable').html("Site Survey file not found");
                $('#SaveBtn').attr('disabled', 'disabled');
                $('#DownloadBtn').attr('disabled', 'disabled');
        }
	$('#SaveBtn').click(checkFields);
	$('.surveyInput').change(dataCheck);
});
function dataCheck(){
	if (this['name'].includes('environment')){
		if (this['name'].includes('ip') || this['name'].endsWith('ntp') || this['name'].includes('dns')){
			var patt = new RegExp('^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$');
			if (!patt.test(this['value'])){
				alert("Incorrect value for IP. Expecting XXX.XXX.XXX.XXX format");
				this['value'] = '';
			}
		} else if (this['name'].includes('prefix')){
			var patt = new RegExp('^[0-9]{1,3}$');
			if (!patt.test(this['value'])){
				alert("Incorrect prefix value.");
				this['value'] = '';
			}
		}
	} else if (this['name'].includes('postgres')){
		if (this['name'].includes('cleandatabase')){
			var patt = new RegExp('^(T|t)rue$');
			var patt2 = new RegExp('^(F|f)alse$');
			if (!(patt.test(this['value']) || patt2.test(this['value']))){
				alert("Incorrect Value for cleandatabase. Expecting 'true' or 'false'.");
				this['value'] = '';
			}
		}
	}
}
function checkFields(event){
	var check = true 
	$("#surveyForm :input").each(function(){
		if (this.type == "text" && this.value == ''){
			alert("Fields cannot be empty");
			check = false;
			return false;
		}
	});
	if (!check)
		event.preventDefault();	
}
