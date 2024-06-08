<?php
header("Content-Type: text/html;charset=UTF-8");

$host = 'localhost';
$user = 'ysn';
$pw = 'aaaa';
$dbName = 'test';
$mysqli = new mysqli($host, $user, $pw, $dbName);

if($mysqli){
    echo "MySQL successfully connected!<br/>";

    $table = $_GET['table'];

    if ($table == 'gps_data') {
        $lat = $_GET['lat'];
        $lon = $_GET['lon'];
        
     

        $query = "INSERT INTO gps_data (lat, lon) VALUES ('$lat','$lon')";
    } elseif ($table == 'imu_data') {
        $ax = $_GET['ax'];
        $ay = $_GET['ay'];
        $az = $_GET['az'];
        $gx = $_GET['gx'];
        $gy = $_GET['gy'];
        $gz = $_GET['gz'];
       
        $query = "INSERT INTO imu_data (ax, ay, az, gx, gy, gz) VALUES ('$ax','$ay','$az','$gx','$gy','$gz')";
    } else {
        echo "Invalid table specified.";
        exit;
    }

    if (mysqli_query($mysqli, $query)) {
        echo "</br>Data inserted successfully into $table!";
    } else {
        echo "</br>Error inserting data: " . mysqli_error($mysqli);
    }
} else {
    echo "MySQL could not be connected";
}

mysqli_close($mysqli);
?>