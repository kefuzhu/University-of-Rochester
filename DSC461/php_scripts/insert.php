<?php
$server = "localhost";
$user = "root";
$password = "1";
$db = "test";

print "Testing connection with ".$db;

// creating the connection

$conn = new mysqli($server, $user, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
else print "<br>Connection OK!";

// SQL statement for creating a table
$sql_insert = "INSERT INTO MyTbl
		VALUES (4, '$_POST[first]', '$_POST[last]')";

if ($conn->query($sql_insert) === TRUE) {
    echo "<br>Values added";
} else {
    echo "<br>Error adding values " . $conn->error;
}


?>

