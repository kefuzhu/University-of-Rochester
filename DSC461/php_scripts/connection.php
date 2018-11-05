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
$sql = "CREATE TABLE IF NOT EXISTS MyTable (
	id INT(3) PRIMARY KEY, 
	firstname VARCHAR(10),
	lastname VARCHAR(10))";
$sql_insert = "INSERT INTO MyTable
		VALUES (1, 'Roberto', 'Baggio')";
/*
 $sql_drop = "DROP TABLE MyTable";

if ($conn->query($sql_drop) === TRUE) {
    echo "<br>MyTable dropped";
} else {
    echo "<br>Error dropping table: " . $conn->error;
} */
if ($conn->query($sql) === TRUE) {
    echo "<br>MyTable created";
} else {
    echo "<br>Error creating table: " . $conn->error;
}

if ($conn->query($sql_insert) === TRUE) {
    echo "<br>Values added";
} else {
    echo "<br>Error adding values " . $conn->error;
}


?>

