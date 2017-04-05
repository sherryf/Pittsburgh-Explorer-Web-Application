//this js is created to save current values of the temperary itinery

// setting global variables
var startTime = "9:30am";
var endTime = "17:30pm";
var homeLocation = "40.4548408,-79.9473358";

//function for hitting plus
/* when plus clicked
	update the duration time for 0.5
	increase all the following time series
*/

function addTime(i){
	//change duration by 0.5 hr
	prev_val = document.getElementById("time-duration-"+i).innerHTML;
	document.getElementById("time-duration-"+i).innerHTML = timeDurationAdd30(prev_val);

	//get item count and loop over
	itemCount = document.getElementById("itemCount").innerHTML;
	console.log(itemCount);
	j = i+1;
	while(j<=itemCount){
		console.log(j);
		prev_val = document.getElementById("time-"+j).innerHTML;
		document.getElementById("time-"+j).innerHTML = timeAmpmAdd30(prev_val);
		j++;
	}
}

//function for hitting plus
/* when minus clicked
	update the duration time for 0.5
	decrease all the following time series
*/
function subtractTime(i){
	//change duration by 0.5 hr
	prev_val = document.getElementById("time-duration-"+i).innerHTML;
	document.getElementById("time-duration-"+i).innerHTML = timeDurationSubtract30(prev_val);

// 	//get item count and loop over
	itemCount = document.getElementById("itemCount").innerHTML;
	console.log(itemCount);
	j = i+1;
	while(j<=itemCount){
		console.log(j);
		prev_val = document.getElementById("time-"+j).innerHTML;
		document.getElementById("time-"+j).innerHTML = timeAmpmSubtract30(prev_val);
		j++;
	}
}



//function timeDurationAdd30 increase timeString 1:00h by 30mins
function timeDurationAdd30(timeString){	
	var min = parseInt(timeString.substring(timeString.length-3,timeString.length-1));
	var hour = parseInt(timeString.substring(0,timeString.length-4));
		if(min==30){
			hour = hour+1;
			min = "00"
		}else{
			min = min + 30;
		}
	result = hour+":"+min+"h";	
	return result;
}

//function timeDurationSubtract30 increase timeString 1:00h by 30mins
function timeDurationSubtract30(timeString){	
	var min = parseInt(timeString.substring(timeString.length-3,timeString.length-1));
	var hour = parseInt(timeString.substring(0,timeString.length-4));
		if(min==30){
			min = "00"
		}else{
			
			if(hour!=0){
				hour = hour - 1;
				min = min + 30;
			}
			min = "00";
		}
	result = hour+":"+min+"h";	
	return result;
}

//function timeAmpmAdd30 increase timeString 1:00pm by 30mins
function timeAmpmAdd30(timeString){
	var ampm = timeString.substring(timeString.length-2);
	var min = parseInt(timeString.substring(timeString.length-4,timeString.length-2));
	var hour = parseInt(timeString.substring(0,timeString.length-5));
		if(min>=30){
			if(hour==11){
				if(ampm=='am'){
					ampm = 'pm';
				}else{
					ampm = 'am';
				}
				hour==0;
			}else{
				if(hour==12){hour=1;}else{hour=hour+1;}
			}
			min = min - 30;
			if(min==0){min="00";}
		}else{
			min = min + 30;
		}

	result = hour+":"+min+ampm;	
	return result;
}

//function timeAmpmSubtract30 decrease timeString 1:00pm by 30mins
function timeAmpmSubtract30(timeString){
	var ampm = timeString.substring(timeString.length-2);
	var min = parseInt(timeString.substring(timeString.length-4,timeString.length-2));
	var hour = parseInt(timeString.substring(0,timeString.length-5));
		if(min<30){
			min = min + 30;
			if(hour==12){
				if(ampm=='am'){
					ampm = 'pm';
				}else{
					ampm = 'am';
				}
			}
			if(hour==1){hour=12;}else{hour==hour-1;}
		} else {
			min = min - 30;
		
			if(min==0){min="00";}
		}
		

	result = hour+":"+min+ampm;	
	return result;
}