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

function addTime(ele){

	var i = parseInt(ele.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id);
	console.log("i = "+i);
	//change duration by 0.5 hr
	prev_val = document.getElementById(i).getElementsByClassName("durationTime")[0].innerHTML;
	// console.log("checkcheckcheck"+prev_val);
	document.getElementById(i).getElementsByClassName("durationTime")[0].innerHTML = timeDurationAdd30(prev_val);

	//get item count and loop over
	itemCount = document.getElementById("itemCount").innerHTML;
	console.log(itemCount);
	j = i+1;
	console.log("start j = "+j);

	while(j<=itemCount){
		console.log("j = "+j);
		prev_val = document.getElementById(j).getElementsByClassName("time")[0].innerHTML;
		document.getElementById(j).getElementsByClassName("time")[0].innerHTML= timeAmpmAdd30(prev_val);
		j++;
	}

	prev_val = document.getElementById("homeTime").innerHTML;
	console.log(prev_val);
	comma = prev_val.search(":");
	time = prev_val.substring(comma-2,comma+3);
	first = prev_val.substring(0,comma-2);
	last = prev_val.substring(comma+3,prev_val.length);

	console.log("first = "+first + " last = "+last + "time = "+time);
	document.getElementById("homeTime").innerHTML = first+timeAmpmAdd30(time)+last ;
}

//function for hitting plus
/* when minus clicked
	update the duration time for 0.5
	decrease all the following time series
*/
function subtractTime(ele){

	var i = parseInt(ele.id);
	console.log("i = "+i);
	//change duration by 0.5 hr
	prev_val = document.getElementById("time-duration-"+i).innerHTML;
	document.getElementById("time-duration-"+i).innerHTML = timeDurationSubtract30(prev_val);

// 	//get item count and loop over
	itemCount = document.getElementById("itemCount").innerHTML;
	console.log(itemCount);
	j = i+1;
	while(j<=itemCount){
		console.log("j = "+j);
		prev_val = document.getElementById(j).getElementsByClassName("time")[0].innerHTML;
		document.getElementById(j).getElementsByClassName("time")[0].innerHTML= timeAmpmSubtract30(prev_val);
		j++;
	}

	prev_val = document.getElementById("homeTime").innerHTML;
	console.log(prev_val);
	comma = prev_val.search(":");
	time = prev_val.substring(comma-2,comma+3);
	first = prev_val.substring(0,comma-2);
	last = prev_val.substring(comma+3,prev_val.length);

	console.log("first = "+first + " last = "+last + "time = "+time);
	document.getElementById("homeTime").innerHTML = first+timeAmpmSubtract30(time)+last ;

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

//function timeAmpmAdd30 increase timeString 1:00 by 30mins
function timeAmpmAdd30(timeString){
	var min = parseInt(timeString.substring(timeString.length-2,timeString.length));
	var hour = parseInt(timeString.substring(0,timeString.length-3));
		if(min+30>=60){
			hour ++;
			min = min-30;
		}else{
			min = min+30;
		}

		if(hour<10){
        	if(min<10){
            	result = "0"+hour+":"+"0"+min; 
        	}else{
             	result = "0"+hour+":"+min;            
        	}
    	}else{
        	if(min<10){
            	result = hour+":"+"0"+min; 
        	}else{
             	result = hour+":"+min;           
        	}
		}
	
	// console.log(result);
	return result;
}

//function timeAmpmSubtract30 decrease timeString 1:00pm by 30mins
function timeAmpmSubtract30(timeString){
	var min = parseInt(timeString.substring(timeString.length-2,timeString.length));
	var hour = parseInt(timeString.substring(0,timeString.length-3));
		if(min-30<=0){
			hour --;
			min = min+30;
		}else{
			min = min-30;
		}

		if(hour<10){
        	if(min<10){
            result = "0"+hour+":"+"0"+min; 
        	}else{
             result = "0"+hour+":"+min;  
            }          
        }else{
    		if(min<10){
    			result = hour+":"+"0"+min;
    		}else{
    			result = hour+":"+min;
    		}
		}
	
	return result;
}





	