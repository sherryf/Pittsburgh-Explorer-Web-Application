
function save(){
	//e.preventDefault();
	var csrftoken = getCookie('csrftoken');

	var mon =  document.getElementById("#inputMon").innerHTML;
	var date = document.getElementById("#inputDate").innerHTML;
	var dow = document.getElementById("#dow").innerHTML;

	$.ajax({
         url : "/planner/save" ,// the endpoint,commonly same url
         type : "POST", // http method
         data : { csrfmiddlewaretoken : csrftoken, 
         mon : mon,
         date : date,
         dow : dow
 	}, // data sent with the post request
 	success : function() {
      console.log("save success"); // another sanity check
 	},

 // handle a non-successful response
 	error : function() {
 	console.log("error"); // provide a bit more info about the error to the console
 	}
 });
};


function getCookie(name) {
       var cookieValue = null;
       if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
         var cookie = $.trim(cookies[i]);
         // Does this cookie string begin with the name we want?
         if (cookie.substring(0, name.length + 1) == (name + '=')) {
             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
             break;
          }
     }
 }
 return cookieValue;
}




// $('#option2').click(function() {
//     $('select[name=myList] option[value=2]').attr('selected', 'selected');
//     $('select[name=myList]').change();
// });
// $('#option3').click(function() {
//     $('select[name=myList] option[value=3]').attr('selected', 'selected');
//     $('select[name=myList]').change();
// });