<?php
header("Content-Type: text/html;charset=UTF-8");

$host = 'localhost';
$user = 'ysn';
$pw = 'aaaa';
$dbName = 'test';
$mysqli = new mysqli($host, $user, $pw, $dbName);

if ($mysqli) {
    echo "MySQL successfully connected!<br/>";

    $table = $_GET['table'];

    if ($table == 'imu_data') {
        $data = $_SERVER['QUERY_STRING']; // 전체 쿼리 스트링 가져오기
        parse_str($data, $params); // 쿼리 스트링 파싱

        $imuData = explode(";", $params['table']); // ;로 구분된 IMU 데이터 분리

        foreach ($imuData as $dataPoint) {
            parse_str($dataPoint, $imuValues); // 각 데이터 포인트를 개별 변수로 파싱

            $ax = $imuValues['ax'];
            $ay = $imuValues['ay'];
            $az = $imuValues['az'];
            $gx = $imuValues['gx'];
            $gy = $imuValues['gy'];
            $gz = $imuValues['gz'];

            $query = "INSERT INTO imu_data (ax, ay, az, gx, gy, gz) VALUES ('$ax','$ay','$az','$gx','$gy','$gz')";
            
            if (mysqli_query($mysqli, $query)) {
                echo "</br>Data inserted successfully into $table!";
            } else {
                echo "</br>Error inserting data: " . mysqli_error($mysqli);
            }
        }
    } elseif ($table == 'gps_data') {
        $lat = $_GET['lat'];
        $lon = $_GET['lon'];

        $query = "INSERT INTO gps_data (lat, lon) VALUES ('$lat','$lon')";
        
        if (mysqli_query($mysqli, $query)) {
            echo "</br>Data inserted successfully into $table!";
        } else {
            echo "</br>Error inserting data: " . mysqli_error($mysqli);
        }
    } else {
        echo "Invalid table specified.";
    }
} else {
    echo "MySQL could not be connected";
}

mysqli_close($mysqli);
?>