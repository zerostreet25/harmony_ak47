<?php
$servername = "localhost";
$username = "ysn";
$password = "aaaa";
$dbname = "test";

$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 확인
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 데이터베이스에서 GPS 데이터 가져오기
$sql = "SELECT lat, lon, timestamp FROM gps_data";
$result = $conn->query($sql);

$gps_data = array();

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $gps_data[] = $row;
    }
} else {
    echo "0 results";
}
$conn->close();

?>



<!DOCTYPE HTML>
<!--
	Eventually by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>종합설계프로젝트 1조</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet"  href="assets/css/main.css" /> <!--assets/css/main.css-->
	</head>
	
	<!-- ------------------------------------------------------------------------------ -->
<head>
    <title>노인의 위치 정보 표시</title>
    <!-- Leaflet CSS 파일 -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <!-- Leaflet JavaScript 파일 -->
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        #map { /* 지도를 표시할 공간의 크기를 조정 */
            height: 300px;
            width: 100%;
        }
    </style>
</head>
<body>
    <h1>사용자의 위치 정보</h1>
    <!-- 지도를 표시할 div 요소 -->
    <div id="map"></div>

    <script>
         var gpsData = <?php echo json_encode($gps_data); ?>;
        // Leaflet을 사용하여 지도 생성
        var map = L.map('map').setView([0, 0], 13);

        // OpenStreetMap 타일 레이어 추가
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // 위도(latitude)와 경도(longitude)를 받아와서 지도에 마커로 표시하는 함수
        function addMarker(latitude, longitude) {
            var marker = L.marker([latitude, longitude]).addTo(map);
            map.setView([latitude, longitude], 13); // 마커가 있는 위치로 지도 중심 이동
        }

        // 예시로 위도와 경도를 전달하여 마커 표시
        // var latitude = 37.5665; // 위도
        // var longitude = 126.9780; // 경도

        // addMarker(latitude, longitude);

        gpsData.forEach(function(data) {
            addMarker(data.lat, data.lon);
        });
    </script>
</body>

	<!-- ------------------------------------------------------------------------------ -->

	<body class="is-preload">

		<!-- Header -->
			<header id="header">
				<h1></h1>
				<p></p>
			</header>
			<header id="header2">
				<h1></h1>
				<a href="sms:01039316380?body= 위도: ${latestData.lat}, 경도: ${latestData.lon}"> 119 문자 보내기 </a>
			</header>
			<script src="assets/js/main.js"></script>

	</body>
</html>