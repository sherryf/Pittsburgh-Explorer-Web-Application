
var j = jQuery.noConflict();
var specialElementHandlers = {
'#editor': function (element, renderer) {
return true;
}
};

$(document).ready(function() {
	$('#action-download').click(function () {
		console.log(document.getElementsByClassName("sortable list")[0]);
	var doc = new jsPDF();
	doc.fromHTML($('#editor').get(0), 15, 15, {
		'width': 170,
		'elementHandlers': specialElementHandlers
	}, {pagesplit: true});
	doc.text(80, 20, 'Pittsburgh Explorer');
	var date = document.getElementsByClassName("day")[0];
	var dateStr = "Date: " + date.getElementsByClassName("mon")[0].innerHTML + " " +
	date.getElementsByClassName("date")[0].innerHTML + " "+ date.getElementsByClassName("dow")[0].innerHTML;
	doc.setFontSize(10);
	doc.setFontType("italic");
	var startStr = document.getElementsByClassName("stayName")[0].innerHTML;
	doc.text(140, 30, dateStr);
	doc.text(120, 35, sanitize(startStr));
	var number = document.getElementsByClassName("sortable list")[0].children.length;
	var space = number * 15;
	for(var i = 0; i < number; i++){
		var attrName = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("name attLink clickable-text")[0].getElementsByTagName("a")[0].innerText;
		
		doc.setFontSize(12);
		doc.setFontType("bold");
		doc.text(30, 50 + i * space,  attrName);
		var estimTime = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("durationTime")[0].innerHTML;
		doc.setFontSize(12);
		doc.setFontType("normal");
		doc.text(35, 55 + i * space + 2,  "Estimate duration time: " + estimTime);
		var spend = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("tours-link text-link attLink jumper")[0].innerText;
		doc.setFontType("normal");
		doc.text(120, 55 + i * space + 2,  "Estimate cost: " + spend);
		var descript = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("trim-desc")[0].innerText;
		doc.setFontType("normal");
		// var lines =doc.splitTextToSize(descript, (170-15-15));
		// doc.text(35, 55 + i * 20 + 6, descript);
		var lMargin=15; //left margin in mm
    	var rMargin=15; //right margin in mm
    	var pdfInMM=170;  // width of A4 in mm
 		var paragraph="Description: " + document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("trim-desc")[0].innerText;
        var lines =doc.splitTextToSize(paragraph, (pdfInMM-lMargin-rMargin));
		doc.text(35,55 + i * space + 8,lines);
		var link = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("name attLink clickable-text")[0].getElementsByTagName("a")[0].getAttribute("href");
		doc.setTextColor(0, 0, 255);
		doc.setFontType("italic");
		doc.text(35,55 + i * space + 28,link);
		doc.setFontSize(12);
		doc.setTextColor(0, 0, 0);
		doc.setFontType("normal");
		var travelTime = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("travelTime")[0].innerHTML;
		var travelTimeLink = document.getElementsByClassName("sortable list")[0].getElementsByTagName("div")[29*i].getElementsByClassName("directions text-link")[0].getAttribute("href");
		doc.text("TravelTime: "+travelTime, 145,55 + i * space + 35, {url: travelTimeLink});
		doc.line(30, 55 + i * space + 34, 140, 55 + i * space + 34);
		doc.text(140, 55 + i * space + 35, ">>");

	}

	doc.save('sample.pdf');
	
	});
});

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&quot;','"');
}