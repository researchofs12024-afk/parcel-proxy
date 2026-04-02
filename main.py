import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">

<script src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=057a4a253017791fe6072d7b089a063a&autoload=false"></script>
</head>

<body>
<div id="map" style="width:100%;height:100vh;"></div>

<script>
kakao.maps.load(function() {

    var map = new kakao.maps.Map(document.getElementById('map'), {
        center: new kakao.maps.LatLng(37.5665, 126.9780),
        level: 2
    });

    var polygons = [];

    function draw(data) {

        polygons.forEach(p => p.setMap(null));
        polygons = [];

        if (!data.features) return;

        data.features.forEach(feature => {

            var coords = feature.geometry.coordinates;

            coords.forEach(polygonSet => {
                polygonSet.forEach(ring => {

                    var path = ring.map(coord => {
                        return new kakao.maps.LatLng(coord[1], coord[0]);
                    });

                    var polygon = new kakao.maps.Polygon({
                        path: path,
                        strokeWeight: 2,
                        strokeColor: '#FF0000',
                        fillColor: '#FF0000',
                        fillOpacity: 0.3
                    });

                    polygon.setMap(map);
                    polygons.push(polygon);

                });
            });

        });
    }

    kakao.maps.event.addListener(map, 'click', function(mouseEvent) {

        var lat = mouseEvent.latLng.getLat();
        var lng = mouseEvent.latLng.getLng();

        var bbox = (lng-0.0003) + "," + (lat-0.0003) + "," + (lng+0.0003) + "," + (lat+0.0003);

        fetch("https://parcel-proxy.onrender.com/parcel?bbox=" + bbox)
        .then(res => res.json())
        .then(data => {
            draw(data);
        });

    });

});
</script>

</body>
</html>
"""

components.html(html_code, height=800)
