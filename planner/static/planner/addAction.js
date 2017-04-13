
function getSearch() {
            $.ajax({
                url: "/planner/get_attrList_json",
                dataType : "json",
                
            });
        }

function timeLengthFunc(minutes){
  var h = Math.floor(minutes / 60);
  var m = minutes % 60;
  m = m < 10 ? '0' + m : m;
  return h + ':' + m;
}

function isInteger(obj) {
    return obj%1 === 0
}

function updateList(response){
    // remove item
    console.log("in updateList");
    var addItem = response[0].fields;
    // console.log(addItem);
    var elements = document.getElementsByClassName("sortable list")[0];
    var childNum = elements.children.length + 1;
    // from last child //
    var lastchild = childNum - 1;
    var lastTime = elements.lastElementChild.getElementsByTagName("p")[1].innerHTML;
    // END ///
    var idStr = "addr-" + childNum;
    var timeEndStr = "time-end-" + childNum;
    var itemStr = "item" + childNum;
        /// <--- Calculate time-end STRAT----> ///
    var timeLength;
    if (addItem.recommended_length_of_visit == "no info"){
        timeLength = 1;
    }
    else{
        timeLength = addItem.recommended_length_of_visit;
    }
    var timeDuration = timeLengthFunc(timeLength * 60);
    /// <--- Calculate time-end END----> ///
    // <----- Find Lat and Lng for first and second -----> ///
    var lastLocation = elements.lastElementChild.getElementsByTagName("p")[0].innerHTML;
    var partsOfStr = lastLocation.split(',');
    var lastLat = partsOfStr[0];
    var lastLng = partsOfStr[1];
    var curLat = addItem.lat;
    var curLng = addItem.lng;
    var hrefgoogle = "https://www.google.com/maps?saddr=" + lastLat +"," + lastLng + "&daddr="+curLat+"," + curLng
    // <------ END ------> ///
    // <----- Deal with URL ---->//
    var realURL;
    if(addItem.url == ""){
        realURL = "#";
    }
    else{
        realURL = addItem.url;
    }
    // <---- END ----->
    var onlytimeStr = "time-" + childNum;
    var addZeroStr = "0" + childNum;
    var timedurationStr = "time-duration-" + childNum;
    var imageurlStr = "url(" + String(addItem.imageurl) + ")";
    var rateStarStr;
    if(isInteger(addItem.rate) == true){
        rateStarStr = "i-stars i-stars--small-" + addItem.rate+ " rating-large";
    }
    else{
        rateStarStr = "i-stars i-stars--small-" + Math.floor(addItem.rate)+ "-half rating-large";
    }
    var rateDisStr = addItem.rate+" star rating";
    // <----- Deal with URL ---->//
    var costStr;
    if(addItem.cost == ""){
        costStr = "Free";
    }
    else{
        costStr = "About $ " + addItem.cost;
    }
    //<---- END ---->  //
    var removeStr = "removeElement(" + childNum + ")";

    // update item Count
    document.getElementById("itemCount").innerHTML = childNum;
    var itemCount = childNum;  
    // console.log(itemCount);

    //calc time 
    // startTime = "11:59pm";
    var latestaddr = document.getElementById(itemCount-1).getElementsByTagName("p")[0].innerHTML;
    var currentaddr = addItem.lat + "," + addItem.lng;
    // // var homeaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
    var zhongjianzhi = "0:45";
    // console.log("itemCount")
    var latestendTime = document.getElementById(itemCount-1).getElementsByTagName("p")[1].innerHTML;
    var startTime = add(latestendTime, zhongjianzhi);
    console.log("***********************latestendTime = "+latestendTime + " zhongjianzhi = "+zhongjianzhi + " = startTime => "+ startTime);
    
    $(elements).append(
        "<div id=" + childNum + " draggable ='true'>"+
        "<p class='hidden' id= " + idStr + " >" +addItem.lat +"," +addItem.lng+ "</p>" + 
        "<p class='hidden' id= " + timeEndStr + " >" +"11:59" + "</p>" + 
        "<li id="+itemStr+" draggable ='true'>" +
        "<div class='itinerary-hop-row'>" +
        "<span class='down-arrow'></span>" + "<span class='travelTime'>" + zhongjianzhi + "</span>" + 
        "<a class='directions text-link' rel='nofollow' href=" + hrefgoogle + " target='_blank'>Get details &raquo;</a>" +
        "</div>"+

        "<div class='visit-row'>" +
        "<div class='visit-contents'>" +
        "<div class='left-col bar overlap'>" +
        "<div class='visit-time'>" +
        "<div class='time' id=" + onlytimeStr +">" +startTime +"</div>" +
        "</div>" +
        "<div class='visit-duration'><div class='edit-duration'>" +
        "<div class='minus reduceTime' onClick='subtractTime(this)' id="+ addZeroStr +">-</div>" +
        "<div class='duration'>" +
        "<div class='durationTime' id="+timedurationStr+" >" + timeDuration +"h</div>" +
        "</div>" +
        "<div class='plus addTime ' onClick='addTime(this)'' id="+ addZeroStr+">+</div>" +
        "</div>" +
        "</div></div>" +
        "<div class='right-col'>" +
        "<div><div class='copyright-info'><div class='visit-row-medium'>" +
        "<div class='photo clickable-image attLink' style='background-image: " + imageurlStr + "' ></div>" +
        "</div></div>" +
        "<div class='detail'>" +
        "<div class='name attLink clickable-text'><a id='attrtitle' href="+realURL+">" +addItem.name+"</a></div>" +
        "<div class='clear'></div>" +
        "<div class='rating-stars '>" +
        "<div class='" + rateStarStr + "' title='" + rateDisStr+"'>" +
        "<img class='offscreen' height='303' src='https://s3-media1.fl.yelpcdn.com/assets/srv0/yelp_design_web/41341496d9db/assets/img/stars/stars.png' width=84' alt='" + rateDisStr+"'>" +
        "</div>" +
        "</div>" +
        "<div class='tags-attractions'><span class='tag' data-cat-id='70'>" +addItem.category+"</span>" +
        "</div>" +
        "<div class='desc'><blockquote class='trim-desc' data-more-link='/plan/84f74934-fc04-4fab-bee3-6d2828540ad7/united-states/san-francisco/alcatraz-island-a63897243' cite='https://www.inspirock.com/united-states/san-francisco/alcatraz-island-a63897243'>" + addItem.shortdesc+ "</blockquote>" +
        "</div>" +
        "<div class='tags-and-tours'>" +
        "<a class='tours-link text-link attLink jumper' href='/''>"+costStr+"</a>" +
        "</div>" +
        "</div>" +
        "<div class='delete' id='delete' onclick=" +removeStr +">" +
        "<div class='fa fa-times'>x</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" +
        "</div>" + 
        "</li>" +
        "</div>");
    // console.log(elements);
    initMap();

    //update all travel ban time

    // request all addresses from the hidden
    var startaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
    var addrlist = [startaddr];
    for(var i = 0; i<itemCount; i++){
        // console.log("hey");
        // console.log(document.getElementById(i+1).getElementsByTagName("p")[0].innerHTML);
        addrlist.push(document.getElementById(i+1).getElementsByTagName("p")[0].innerHTML);
    }
    addrlist.push(startaddr);
    // console.log(addrlist);

    var selectedMode = document.getElementById('mode').value;

    for(var i=0;i<addrlist.length-1;i++){
        start = addrlist[i];
        end = addrlist[i+1];
        calcRoute(start, end,i,itemCount,selectedMode);
    }

    updateendtime(itemCount);

    // update cost
    var totalMoney = document.getElementsByClassName("date TotalMoany")[0];
    var moneyStr = totalMoney.innerHTML;
    var howMuch = parseFloat(moneyStr.split(' ')[1]);
    howMuch = howMuch + parseFloat(addItem.cost);
    howMuch = howMuch.toFixed(1);
    totalMoney.innerHTML = "$ " + howMuch;


}



function add_alert(itemid) {
    // var objects = getAttrList()
    var itemWhole = document.getElementById(itemid);
    var itemTextElement = document.getElementById(itemid).getElementsByClassName("attractionTitle")[0];
    var itemTextName   = itemTextElement.innerHTML;
    // Clear input box and old error message (if any)
    itemWhole.innerHTML = '';
    displayError('');

    $.ajax({
        url: "/planner/add-item/" + itemid,
        type: "GET",
        // data: "id="+itemid+"&attractionTitle=" + itemTextElement +"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response) {
            if (Array.isArray(response)) {
                updateList(response);
            } else {
                displayError(response.error);
            }
        }
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    var errorElement = document.getElementsByClassName("error");
    errorElement.innerHTML = message;
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    console.log("before return");
    return "unknown";
}

window.onload = getSearch;

// window.setInterval(getSearch, 5000);
