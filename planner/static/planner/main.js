/* When the user clicks on the button, 
		toggle between hiding and showing the dropdown content */
		function myFunction(index) {
		    document.getElementById("myDropdown "+index).classList.toggle("show");
		}

		// Close the dropdown if the user clicks outside of it
		window.onclick = function(event) {
		  if (!event.target.matches('.dropbtn')) {

		    var dropdowns = document.getElementsByClassName("dropdown-content");
		    var i;
		    for (i = 0; i < dropdowns.length; i++) {
		      var openDropdown = dropdowns[i];
		      if (openDropdown.classList.contains('show')) {
		        openDropdown.classList.remove('show');
		      }
		    }
		  }
		}

// On click open alert window for adding options
// function add_alert(){
// 	alert("I am an alert box!");
// }

// // Mapping from Xinran
// function initialize()
// {
// var mapProp = {
//   center:new google.maps.LatLng(40.4406,-79.9959),
//   zoom:5,
//   mapTypeId:google.maps.MapTypeId.ROADMAP
//   };
// var map=new google.maps.Map(document.getElementById("googleMap")
//   ,mapProp);
// }

// google.maps.event.addDomListener(window, 'load', initialize);