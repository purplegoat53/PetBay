function vote(picid, voteType) {
	alert(picid);
	
	$.post("/ajax/vote/"+voteType,
    {
        picid : picid
    },
    function(data, status){
        alert("Data: " + data.message + "\nStatus: " + status);
		if(data.message === "Already Voted")
		{
			
		}
		else {
			window.location.reload();
		}
    });
}

function progressHandlingFunction(e){
    if(e.lengthComputable){
		var progress = ((e.loaded / e.total) * 100.0).toFixed(2) + "%";
		$("#proBar2").width(progress);
		$("#proBar2").html(progress);
    }
}


function upload3(event){
    var formData = new FormData($('#uploader')[0]);
	var pic = document.getElementById("input-1");
	//document.getElementById("progressBar").style.display = "block";
	document.getElementById("proBar").style.display = "block";
	event.preventDefault();
	event.stopPropagation();
	//alert("hi");
    $.ajax({
        url: '/ajax/upload',  //Server script to process data
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
		upload: pic,
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    }).done(function(data) {
		$('#upModal').modal('hide');
		//alert("Kate is Slightly Less Gay than before Gay");		
		//window.location.reload();
		$.get("/", function(data, status){
        document.body.parentNode.innerHTML = data;
		$('#upModal').modal();
		var orig_html = $("#entry_fieldsg").html();
		$("#entry_fieldsg").html("Upload Successful!");
		setTimeout(function (){
			//window.location.reload();
			//$("#upModal").modal("hide");
			$("#entry_fieldsg").html(orig_html);
		}, 1000);
    });
	});
	
	
}

function showUp(event) {
	$('#upModal').modal();
	event.preventDefault();
	event.stopPropagation();
}

/*var last_update = new Date() / 1000;

setInterval(function() {
	$.get("/ajax/getnew", {last_time: Math.round(last_update)-6}, function(data) {
		var orig = $("#ajax").html();
		$("#ajax").html(data + orig);
		last_update = new Date() / 1000;
		event.preventDefault();
		event.stopPropagation();
	});
}, 3000);*/


