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
$sql_select = "SELECT firstname,lastname FROM MyTable";

echo "<br>See values below:";
if ($result = $conn->query("SELECT * FROM MyTable")) {
    printf("Select returned %d rows.\n", $result->num_rows);
}

$result = $conn->query($sql_select);
echo "<br>";
while($row = $result->fetch_assoc()) {
       	echo "First Name " . $row["firstname"]. " Last Name: " . $row["lastname"]. " <br>";
}


?>

