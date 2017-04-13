/*!
 * Zepto HTML5 Drag and Drop Sortable
 * Author: James Doyle(@james2doyle) http://ohdoylerules.com
 * Repository: https://github.com/james2doyle/zepto-dragswap
 * Licensed under the MIT license
 */
; (function ($) {
    $.fn.dragswap = function (options) {
        var dragSrcEl;
        function getPrefix() {
            var el = document.createElement('p'),
            getPre, transforms = {
                'webkitAnimation': '-webkit-animation',
                'OAnimation': '-o-animation',
                'msAnimation': '-ms-animation',
                'MozAnimation': '-moz-animation',
                'animation': 'animation'
            };
            document.body.insertBefore(el, null);
            for (var t in transforms) {
                if (el.style[t] !== undefined) {
                    el.style[t] = "translate3d(1px,1px,1px)";
                    getPre = window.getComputedStyle(el).getPropertyValue(transforms[t]);
                    // return the successful prefix
                    return t;
                }
            }
            document.body.removeChild(el);
        }
        this.defaultOptions = {
            element: 'li',
            overClass: 'over',
            moveClass: 'moving',
            dropClass: 'drop',
            dropAnimation: false,
            exclude: '.disabled',
            prefix: getPrefix(),
            dropComplete: function () {
                return;
            }
        };

        function excludePattern(elem) {
            return elem.is(settings.excludePatt);
        }

        function onAnimEnd(elem) {
            var $elem = $(elem);
            $elem.addClass(settings.dropClass);
            // add an event for when the animation has finished
            $elem.on(settings.prefix + 'End', function () {
                // remove the class now that the animation is done
                $elem.removeClass(settings.dropClass);
            }, false);
        }

        function handleDragStart(e) {
            if (!excludePattern($(this))) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            $(this).addClass(settings.moveClass);
            // get the dragging element
            dragSrcEl = this;
            // it is moving
            //console.log(e);
            if (e.originalEvent.dataTransfer) {
              var dt = e.originalEvent.dataTransfer;
              dt.effectAllowed = 'move';        
              dt.setData('text', this.innerHTML);
                
            }
            else if(e.dataTransfer){
              var dt = e.dataTransfer;
              dt.effectAllowed = 'move';        
              dt.setData('text', this.innerHTML);
            }
        }

        function handleDragEnter(e) {
            // this / e.target is the current hover target.
            $(this).addClass(settings.overClass);
        }

        function handleDragLeave(e) {
            $(this).removeClass(settings.overClass); // this / e.target is previous target element.
            
        }

        function handleDragOver(e) {
            if (e.preventDefault) {
                e.preventDefault(); // Necessary. Allows us to drop.
            }
           if (e.originalEvent.dataTransfer) {
                e.originalEvent.dataTransfer.dropEffect = 'move'; // See the section on the DataTransfer object.
            }
            else if(e.dataTransfer){
                e.dataTransfer.dropEffect = 'move'; // See the section on the DataTransfer object.
            }
            return false;
        }

        function handleDrop(e) {
            // this / e.target is current target element.
            if (e.stopPropagation) {
                e.stopPropagation(); // Stops some browsers from redirecting.
            }
            if (!excludePattern($(this))) {
                console.log('prevent drop');
                return false;
            }

            // Don't do anything if dropping the same column we're draggi.
            if (dragSrcEl != this) {
                // Set the source column's HTML to the HTML of the column dropped on.
                var oldEl = {
                    html: this.innerHTML,
                    id: this.id
                };
                var newEl = {
                    html: dragSrcEl.innerHTML,
                    id: dragSrcEl.id
                };
                // swap all the data
                dragSrcEl.innerHTML = oldEl.html;
                dragSrcEl.id = oldEl.id;
                this.innerHTML = newEl.html;
                this.id = newEl.id;
                if (settings.dropAnimation) {
                    onAnimEnd(this);
                    onAnimEnd(dragSrcEl);
                }
                $(this).siblings().removeAttr('draggable');
                $(this).siblings().filter(settings.excludePatt).attr('draggable', true);
                
                //******retrieved both id
                var receiverid = oldEl.id[4];
                var starterid = newEl.id[4];

                //**** fetch hidden info
                var oldreceiveraddr = document.getElementById(receiverid).getElementsByTagName("p")[0].innerHTML;
                // var oldreceiverendtime = document.getElementById(receiverid).getElementsByTagName("p")[1].innerHTML;
                var replacedaddr = document.getElementById(starterid).getElementsByTagName("p")[0].innerHTML;
                // var replacedendtime = document.getElementById(starterid).getElementsByTagName("p")[1].innerHTML;

                //**** replace div hidden info
                document.getElementById(receiverid).getElementsByTagName("p")[0].innerHTML = replacedaddr;
                // document.getElementById(receiverid).getElementsByTagName("p")[1].innerHTML = replacedendtime;
                document.getElementById(starterid).getElementsByTagName("p")[0].innerHTML = oldreceiveraddr;
                // document.getElementById(starterid).getElementsByTagName("p")[1].innerHTML = oldreceiverendtime;

                //**** replace received travel ban time, travel ban url 
                // get previous add and endtime
                if(receiverid==1){
                    var rlastaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
                } else {
                    var rlastaddr = document.getElementById(receiverid-1).getElementsByTagName("p")[0].innerHTML;
                }

                //replace url
                document.getElementById(receiverid).getElementsByClassName("itinerary-hop-row")[0].getElementsByTagName("a")[0].href = "https://www.google.com/maps?saddr="+rlastaddr+"&daddr="+replacedaddr;

                //// replace beswapped travel ban time, travel ban url and attraction start time
                // get previous add and endtime
                if(starterid==1){
                    var slastaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
                } else {
                    var slastaddr = document.getElementById(starterid-1).getElementsByTagName("p")[0].innerHTML;
                }

                //replace url
                var oldurl = document.getElementById(starterid).getElementsByClassName("itinerary-hop-row")[0].getElementsByTagName("a")[0].href;
                document.getElementById(starterid).getElementsByClassName("itinerary-hop-row")[0].getElementsByTagName("a")[0].href = "https://www.google.com/maps?saddr="+slastaddr+"&daddr="+oldreceiveraddr;

                // reset map
                initMap();

                //update all travel ban time

                // request all addresses from the hidden
                var itemCount = document.getElementById("itemCount").innerHTML;
                console.log("youyouyouyouyouyoyu");
                var startaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
                var addrlist = [startaddr];
                for(var i = 0; i<itemCount; i++){
                    addrlist.push(document.getElementById(i+1).getElementsByTagName("p")[0].innerHTML);
                }
                addrlist.push(startaddr);

                var travelMode = document.getElementById('mode').value;
                for(var i=0;i<addrlist.length-1;i++){
                    start = addrlist[i];
                    end = addrlist[i+1];
                    calcRoute(start, end,i,itemCount,travelMode);
                }

                updateendtime(itemCount);

                console.log('dropped');
                settings.dropComplete();
            }
            return false;
        }

        var settings = $.extend({}, this.defaultOptions, options);
        if (settings.exclude) {
            if (typeof settings.exclude != 'string') {
                var excludePatt = '';
                for (var i = 0; i < settings.exclude.length; i++) {
                    excludePatt += ':not(' + settings.exclude[i] + ')';
                }
                settings.excludePatt = excludePatt;
            }
            else {
                settings.excludePatt = ':not(' + settings.exclude + ')';
            }
        }

        var method = String(options);
        var items = [];
        // check for the methods
        if (/^(toArray|toJSON)$/.test(method)) {
            if (method == 'toArray') {
                $(this).find(settings.element).each(function (index, elem) {
                    items.push(this.id);
                });
                return items;
            } else if (method == 'toJSON') {
                $(this).find(settings.element).each(function (index, elem) {
                    items[index] = {
                        id: this.id
                    };
                });
                return JSON.stringify(items);
            }
            return;
        }



        return this.each(function (index, item) {
            var $this = $(this);
            // select all but the disabled things
            var $elem = $this.find(settings.element);

            var target = this;
            var config = { childList: true };
            var observer = new MutationObserver(function (mutations) {
                console.log(mutations);
                for(var i=0; i<mutations.length; i++){
                  if(mutations[i].addedNodes.length != 0){
                    for(var j=0; j<mutations[i].addedNodes.length; j++){
                      $(mutations[i].addedNodes[j]).siblings().removeAttr('draggable');
                      $(mutations[i].addedNodes[j]).siblings().filter(settings.excludePatt).attr('draggable', true);
                    }
                  }
                }
             
            });

            observer.observe(target, config);

            function handleDragEnd(e) {
                $this.removeClass(settings.moveClass);
                // this/e.target is the source node.
                //console.log('handleDragEnd');
                $elem = $this.find(settings.element);
                $elem.each(function (index, item) {
                    // console.log(item);
                    $(item).removeClass(settings.overClass);
                    $(item).removeClass(settings.moveClass);
                });

            }
            // set the items to draggable
            $elem.filter(settings.excludePatt).attr('draggable', true);

            $this.off('dragstart');
            $this.off('dragenter');
            $this.off('dragover');
            $this.off('dragleave');
            $this.off('drop');
            $this.off('dragend');

            $this.on('dragstart', settings.element, handleDragStart);
            $this.on('dragenter', settings.element, handleDragEnter);
            $this.on('dragover', settings.element, handleDragOver);
            $this.on('dragleave', settings.element, handleDragLeave);
            $this.on('drop', settings.element, handleDrop);
            $this.on('dragend', settings.element, handleDragEnd);

        });
    };
})(Zepto);

// drag&drop
$(function() {
        
        $('.sortable_exclude_dynamic').dragswap({
            element : 'li',
            dropAnimation: true,
            exclude : ['.correct', '.empty']
        });  
        
        $('.sortable_exclude_dynamic').append(
            '<li id="item1">Item 1</li>'
            +'<li id="item2">Item 2</li>'
            +'<li id="item3" class="correct">Item 3</li>'
            +'<li id="item4">Item 4</li>'                                  
            +'<li id="item5" class="empty"></li>'
            +'<li id="item6" class="correct">Item 6</li>'
            +'<li id="item7" class="correct">Item 7</li>');
        
        $('.sortable').dragswap({
            element : 'li',
            dropAnimation: true  
        });
        
        $('.funcs').dragswap({
            dropAnimation: false,
            dropComplete: function() {
                var sortArray = $('.funcs').dragswap('toArray');
                $('#arrayResults').html('['+sortArray.join(',')+']');
                var sortJSON = $('.funcs').dragswap('toJSON');
                $('#jsonResults').html(sortJSON);
            }
        });
    });


function callback(response, status) {
  if (status == 'OK') {
    var origins = response.originAddresses;
    var destinations = response.destinationAddresses;

    for (var i = 0; i < origins.length; i++) {
      var results = response.rows[i].elements;
      for (var j = 0; j < results.length; j++) {
        var element = results[j];
        
        var duration = element.duration.text;
        console.log("******"+duration);
        
      }
    }
  }
}

function updateendtime(itemCount){
    var prevendtime = "";
    var duration = "";
    // console.log("itemCount="+itemCount);

    for(var i = 0; i<itemCount; i++){
        // get prevendtime and duration
        if(i==0){
            // console.log(i+1);
            prevendtime = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[1].innerHTML;
            // console.log(prevendtime);
            
        }else {
            prevendtime = document.getElementById(i).getElementsByTagName("p")[1].innerHTML;
            // console.log(prevendtime); //9:30

        }
        traveltime = document.getElementById(i+1).getElementsByClassName("itinerary-hop-row")[0].getElementsByTagName("span")[1].innerHTML;
        // console.log(traveltime); //32min
        duration = document.getElementById(i+1).getElementsByClassName("durationTime")[0].innerHTML; 
        // console.log(duration); //1:00h

        //update new start time
        document.getElementById(i+1).getElementsByClassName("time")[0].innerHTML = add(prevendtime, traveltime);
        //update new end time
        document.getElementById(i+1).getElementsByTagName("p")[1].innerHTML = add1(prevendtime, traveltime, duration) ;
    }
}

function add(prevendtime, traveltime){
    console.log("kicking into added time");
    console.log("traveltime = "+traveltime +"prevendtime = "+prevendtime);
//     //09:30 + 32min
    var prehour = parseInt(prevendtime.substring(0,2));
    // console.log(prehour);
    var premin = parseInt(prevendtime.substring(3));
    var thour = parseInt(traveltime.substring(0,2));
    // console.log("traveltime -------"+traveltime);
    var tmin = parseInt(traveltime.substring(traveltime.length-2,traveltime.length));
    var newhour = 0;
    var newmin = 0;
    var result = "result";

    // console.log("prehour="+prehour+" premin="+premin+" dmin="+tmin);

    if (premin+tmin>=60){
        newhour = prehour+thour + 1;
        newmin = premin+tmin-60;
    } else{
        newhour = prehour+thour;
        newmin = premin+tmin;
    }   

    if(newhour<10){
        if(newmin<10){
            result = "0"+newhour+":"+"0"+newmin; 
        }else{
             result = "0"+newhour+":"+newmin;            
        }
    }else{
        if(newmin<10){
            result = newhour+":"+"0"+newmin; 
        }else{
             result = newhour+":"+newmin;           
        }
        
    }
    
    // console.log(result);
    return result;
    }

function add1(prevendtime, traveltime, duration){
//     //09:30 + 32min + 1:00h
    // console.log("into add")
    // console.log(duration);
    var prehour = parseInt(prevendtime.substring(0,2));
    var premin = parseInt(prevendtime.substring(3));
    var tmin = parseInt(traveltime.substring(0,2));
    var dhour = parseInt(duration.substring(0,1));

    var dmin = parseInt(duration.substring(2,duration.length-1));
    var newhour = 0;
    var newmin = 0;
    var result = "result";

    // console.log("prehour="+prehour+" premin="+premin+" tmin="+tmin + " dhour=" +dhour + " dmin ="+dmin);

    if (premin+tmin+dmin>=60){
        newhour = prehour+dhour + 1;
        newmin = premin+tmin+dmin-60;
    } else{
        newhour = prehour+dhour;
        newmin = premin+tmin+dmin;
    }   

    if(newhour<10){
        if(newmin<10){
            result = "0"+newhour+":"+"0"+newmin; 
        }else{
             result = "0"+newhour+":"+newmin;            
        }
    }else{
        if(newmin<10){
            result = newhour+":"+"0"+newmin; 
        }else{
             result = newhour+":"+newmin;           
        }
    }
    
    // console.log(result);
    return result;
    }

/// google MAP get duration trial
    function calcRoute(start, end, i,itemCount, travelMode) {

          // console.log("getting into calcRoute");
          // console.log("i = "+i + ", itemCount = "+itemCount);
          var directionsService = new google.maps.DirectionsService();
          var directionsDisplay = new google.maps.DirectionsRenderer();
          var request = {
            origin:start,
            destination:end,
            travelMode: travelMode
          };
          directionsService.route(request, function(response, status) {
            if (status == 'OK') {
                // console.log("status ok");
              directionsDisplay.setDirections(response);
              // console.log("correct time = "+response.routes[0].legs[0].duration.text);
              durationTime = parseInt(response.routes[0].legs[0].duration.value);
              // console.log(durationTime);

              var hour = 0;
              var min = 0;
              if(durationTime>=3600){
                hour = Math.floor(durationTime/3600);
                min  = Math.round((durationTime-3600*hour)/60)+30;
                // console.log(hour+":"+min);
              }else{
                min = Math.round(durationTime/60)+30;
                // console.log("calc min without 30="+Math.round(durationTime/60));
              }
              
              if(min>=60){hour = hour+1;min=min-60;}
              // var min = parseInt(durationTime.substring(0,durationTime.length-5))+30;
              // console.log(durationTime + "min = "+min);
              if(min<10){result = hour+":0"+min;}else{result = hour+":"+min;}
              if(i==itemCount){
                // console.log("hitting i = 3");
                document.getElementById("backHome").getElementsByTagName("span")[1].innerHTML = result;
              } else {
                document.getElementById(i+1).getElementsByClassName("itinerary-hop-row")[0].getElementsByTagName("span")[1].innerHTML = result;
              }
          };
        })

        }


    function removeElement(i) {
        console.log("getting in to remove Element");
        // index name and url
        var name = document.getElementById("item"+i).getElementsByTagName("a")[1].innerHTML;
        var url = document.getElementById("item"+i).getElementsByClassName("visit-row-medium")[0].getElementsByTagName("div")[0].style.backgroundImage;
        var pictureUrl = url.substring(5,url.length-2)
        var id = document.getElementById("item1").getElementsByClassName("left-col bar overlap")[0].getElementsByTagName("div")[2].innerHTML;
        var webUrl = document.getElementById("item"+i).getElementsByTagName("a")[1].href;

        $("#suggestion_list").prepend(
            // "<p> testing testing </p>"
            
            "<div id = "+id+">"
                +"<li class='attraction clear-after'>"
                    +"<div class='search-item'>"
                        +"<span class='attractionDetailsLink clickable-text' data-link='/'' data-event-src='browse-results'>"
                            +"<div class='search-pic' style='background-image:url("+pictureUrl+")'>"
                            +"</div>"
                        +"</span>"
                        +"<div style='height:40px;'>" 
                            +"<span class='attractionTitle' datalink='"+webUrl+"''>"+name+"</span>"
                        +"</div>"
                        +"<div>"
                            +"<button onclick='add_alert(+"+id+")' class='alert'>Add</button>"
                        +"</div>"
                    +"</div>"
                +"</li>"
                +"</div>"
        )

        document.getElementById("item"+i).remove();
    }

// travel mode change

    function ReCalRouteMode(){
        var selectedMode = document.getElementById('mode').value;
        // console.log(selectedMode);
        // request all addresses from the hidden
                var itemCount = document.getElementById("itemCount").innerHTML;
                // console.log("youyouyouyouyouyoyu");
                var startaddr = document.getElementsByClassName("day-title clearfix ")[0].getElementsByTagName("p")[0].innerHTML;
                var addrlist = [startaddr];

                for(var i = 0; i<itemCount; i++){
                    addrlist.push(document.getElementById(i+1).getElementsByTagName("p")[0].innerHTML);
                }
                addrlist.push(startaddr);

                for(var i=0;i<addrlist.length-1;i++){
                    start = addrlist[i];
                    end = addrlist[i+1];
                    calcRoute(start, end,i,itemCount,selectedMode);
                }

                updateendtime(itemCount);
      

        }





