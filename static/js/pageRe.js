function executeQuery() {
  $.ajax({
    url: '/',
	type: 'GET',
    success: function(data) {
      // do something with the return value here if you like
	  document.body.parentNode.innerHTML = data;
    }
  });
  setTimeout(executeQuery, 5000); // you could choose not to continue on failure...
}

$(document).ready(function() {
  // run the first time; all subsequent calls will take care of themselves
  setTimeout(executeQuery, 5000);
});