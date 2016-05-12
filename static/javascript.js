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
    populatemarkers(map);
  };
  req.send() 
}; 
google.maps.event.addDomListener(window, 'load', initialize);

function placeMarker (lat, lon, map) {
var position = new google.maps.LatLng(lat,lon); 
var marker = new google.maps.Marker({
  position: position,
  map: map
});
};

function populatemarkers(themap) {
  var amap = themap 
  var obj = new XMLHttpRequest() 
  obj.open("GET",'/markers',true);
  obj.onreadystatechange = function () {
    if (obj.readyState == 4 && obj.status==200){
      thejson = JSON.parse(obj.responseText)
      for (i in thejson.json_obj) {
        console.log(thejson.json_obj[i]); 
        var lat = thejson.json_obj[i]['lat'];
        var lon = thejson.json_obj[i]['lon'];
        //console.log(thejson.json_obj[i]['lat']); 
        placeMarker(lat, lon, amap); 
      }
    }
  }; 
  obj.send() 
}; 

