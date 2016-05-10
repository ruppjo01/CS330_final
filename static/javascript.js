var myCenter=new google.maps.LatLng(30,11.09);
var map; 

function initialize() {
  var req = new XMLHttpRequest() 
  req.open("GET",'/student_map',true);
  req.onreadystatechange = function () {
  var mapProp = {
    center:myCenter,
    zoom:2,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
  };
  req.send() 
}

google.maps.event.addDomListener(window, 'load', initialize);