function progressHandlingFunction(e){
    if(e.lengthComputable){
		$("#proBar2").width(e.loaded);
		$("#proBar2").html(e.loaded);
    }
}

function updateProf(event) {
	var formData = new FormData($('#uploader')[0]);
	var nickname = document.getElementById("nickname").value;
	var description = document.getElementById("description").value;
	var pic = document.getElementById("input-1");
	if(nickname.length <= 0)
		formData.delete("nickname");
	if(description.length <= 0)
		formData.delete("description");
	document.getElementById("proBar").style.display = "block";
	event.preventDefault();
	event.stopPropagation();
	$.ajax({
        url: '/ajax/update_profile',  //Server script to process data
        type: 'POST',
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        },
        //Ajax events
        //beforeSend: beforeSendHandler,
        //success: completeHandler,
        //error: errorHandler,
        // Form data
		data: formData,
		//nickname: nickname,
		//description: description,
		//upload: pic,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    }).done(function(data) {
		window.location.reload();
		
    });
}