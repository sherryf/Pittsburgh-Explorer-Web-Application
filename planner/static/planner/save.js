
function save(){
  // e.preventDefault();
  var itemCount = parseInt(document.getElementById("itemCount").innerHTML);
  var csrftoken = getCookie('csrftoken');
  var estimateDate = document.getElementById("#InputDate").getAttribute("value");
  var starttime = document.getElementById("#InputTime").getAttribute("value");
  var interest = document.getElementById("#InputInterest").getAttribute("value");
  var budget = document.getElementById("#InputBudget").getAttribute("value");
  var start = document.getElementById("addr-0").getAttribute("value");
  var plan_id = document.getElementById("daybyday").getAttribute("value");

  var objects = {}
  for (var i = 1; i <= itemCount; i++) {
    var info = {}
    var duration = document.getElementById(i).getElementsByClassName("durationTime")[0].innerHTML;
    var divs =  document.getElementById(i).getElementsByTagName("div");
    for (var j = 0; j < divs.length; j++){
      if (divs[j].id == "id"){
        var id =  divs[j].innerText;
        break;
      }
    }
    info["duration"] = duration
    info["id"] = id
    objects[i] = JSON.stringify(info)
  }
  

  console.log(objects);


  $.ajax({
         url : "/planner/save" ,// the endpoint,commonly same url
         type : "POST", // http itemcounmethod
         data : { 
         csrfmiddlewaretoken : csrftoken,
         estimateDate : estimateDate,
         itemCount : itemCount,
         starttime : starttime,
         interest : interest,
         budget : budget,
         objects : JSON.stringify(objects),
         start : start,
         plan_id : plan_id
  }, // data sent with the post request
  success : function(response) {
      console.log("save success"); 
      // update cost
      console.log(response.plan_id);
      alert("save success");
      document.getElementById("daybyday").setAttribute("value",response.plan_id);

      // another sanity check
  },

 // handle a non-successful response
  error : function() {
  console.log("error"); 
  alert("error");// provide a bit more info about the error to the console
  }
 });

}


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