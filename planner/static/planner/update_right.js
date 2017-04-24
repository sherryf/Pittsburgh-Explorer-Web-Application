
function change(id){
	$.ajax({ 
		url: '/planner/get_list/' + id,
		dataType : "json",
		success: updateLeft
	});
	console.log("yes");
};

function updateLeft(items){
	var elements = document.getElementsByClassName("attraction clear-after")[0];
	elements.innerHTML = "";
	console.log(items.length);
	$(items).each(function() {
		var html = "<div id = "+ this.id + ">" +
				   "<li class='attraction clear-after'>" +
				   "<div class='search-item'>" +
						"<span class='attractionDetailsLink clickable-text' data-link='/' data-event-src='browse-results'>"+
							"<div class='search-pic' style='background-image:url(" + this.imageurl + ")'>" +
							"</div>"+
						"</span>" +
						"<div style='height:40px;'>" + 
							"<span class='attractionTitle' datalink='" + this.url + "'>" + this.name + "</span>" +
						"</div>" +
						"<div>"+
							"<button onclick='add_alert("+ this.id +")' class='alert'>Add</button>"+
						"</div>" +
					"</div>" +
				"</li>" +
				"</div>" 

		$(elements).append(html);
	
	}); 
}







// $('#option2').click(function() {
//     $('select[name=myList] option[value=2]').attr('selected', 'selected');
//     $('select[name=myList]').change();
// });
// $('#option3').click(function() {
//     $('select[name=myList] option[value=3]').attr('selected', 'selected');
//     $('select[name=myList]').change();
// });