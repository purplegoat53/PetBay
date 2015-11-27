function upvote(picid) {
	alert(picid);
	
	$.post("/ajax/vote/up",
    {
        picid : picid
    },
    function(data, status){
        alert("Data: " + data.status + "\nStatus: " + status);
    });
}