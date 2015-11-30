
function login1(event) {
	var email = document.getElementById("email").value;
	var password = document.getElementById("password").value;
	//var encrypted = sjcl.encrypt("password", password);
	//var decrypt = sjcl.decrypt("password", encrypted);
	var statusOfLogin;
	alert("Email: " + email + "\nPassword: " + password);
	
	event.preventDefault();
	
	$.post("/ajax/login",
    {
        email: escape(email),
        password: password
    },
    function(data, status){
        alert("Data: " + data.status + "\nStatus: " + status);
		if(data.status === "ERROR")
		{
			document.getElementById("email").value = "Login Incorrect!";
		}
		else
		{
			document.getElementById("signin").innerHTML = ""
			 $('#experiment').load('/ajax/welcome');
			 //$('#experiment').modal('show');
			 $('#experiment').modal();
			 //$('#exModal').modal('show');
			 //$('#experiment').modal('toggle');
		}
    });
}

function register(event) {
	var email = document.getElementById("newEmail").value;
	var compaEmail = document.getElementById("reNewEmail").value;
	var pass = document.getElementById("newPass").value;
	var compaPass = document.getElementById("reNewPass").value;
	event.preventDefault();
	event.stopPropagation();
	if(email != compaEmail)
	{
		alert("EMAILS DO NOT MATCH!");
		document.getElementById("newEmail").value = '';
		document.getElementById("reNewEmail").value = '';
	}
	else if(pass != compaPass)
	{
		alert("PASSWORDS DO NOT MATCH!");
		document.getElementById("newPass").value = '';
		document.getElementById("reNewPass").value = '';
	}
	else{
		$.post("/ajax/register",
    {
        email: email,
        password: pass
    },
    function(data, status){
        alert("Data: " + data.status + "\nStatus: " + status);	
		document.getElementById("entry_fields").innerHTML = "<div><p><font color='Black'>Registration Successful!\nYou can now login with your detials!</font></p></div>"
    });
	}
}

function logout(event) {
	$.post("/ajax/logout",
    {

    },
    function(data, status){
        alert("Data: " + data.status + "\nStatus: " + status);	
    });
	}
}



