$(document).ready(function(){
	$('#submit').click(function(event){
		$('#uploadPPForm').css("opacity", ".5");
		$('#uploadPPForm').trigger('submit');
		$('.loader').css("opacity", "1");
	        $('.loader').css("display", "inline");	
	});
        $('#uploadbtn').change(function(){
                var btnvalue = this.value;
                if (btnvalue.search("tar.gz") < 0){
                        $('#invalidFile').css('display', 'inline');
                        $('#submit').css('display', 'none');
                }
                else {
                        $('#invalidFile').css('display', 'none');
                        $('#submit').css('display', 'inline');
                }
                if (btnvalue == ''){
                        btnvalue = 'Choose file...';
                        $('#invalidFile').css('display', 'none');
                }
                else {
                        btnvalue = btnvalue.replace('C:\\fakepath\\', '');
                }
                $('#lbluploadbtn').text(btnvalue);
        });
});
