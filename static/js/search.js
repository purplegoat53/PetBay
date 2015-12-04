function search(event) {
	var proname = document.getElementById("name").value;
	event.preventDefault();
	event.stopPropagation();
	/*var url = "/profile/" + proname;
	window.location.assign(url);*/
	jQuery.ajax({ 
        type: "GET", 
        url: "/profile/"+proname, 
        //dataType:"json", 
        //data:"userId=SampleUser", 
        success:function(response){ 

                // Process the expected results...
				var url = "/profile/" + proname;
				window.location.assign(url);
            
        }, 
     error: function(xhr, textStatus, errorThrown) { 
            alert('Profile Not Found!\nTry looking for another username.'); //\n \n  Status = ' + xhr.status); 
         } 

    }); 

}