<html>
	<body>

		<h1>Job Application Database</h1>
		<p>-- by Fastest HK Journalist (#11)</p >
		<a href="http://betaweb.csug.rochester.edu/~kzhu6/index.html">< Back to main page</a>
		<hr>

	</body>
</html>

<?php
$server = "localhost";
$user = "kzhu6";
$password = "sat2400";
$db = "kzhu6";

print "Testing connection with ".$db;

// creating the connection

$conn = new mysqli($server, $user, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
else print "<br>Connection OK!<br>";

// Insert
if ($_POST[action] == 'Insert') {
	$sql_insert = "INSERT INTO RECRUITER
				   VALUES ('$_POST[ID]', '$_POST[FirstName]', '$_POST[LastName]',
						   '$_POST[Position]','$_POST[DepartmentID]')";

	if ($conn->query($sql_insert) == TRUE && $conn->affected_rows == 1) {
	    echo "<br><b>Values added</b><br>";
	} else {
	    echo "<br><b>Error adding values</b> " . $conn->error . "<br>";
	}
}

// Delete
if ($_POST[action] == 'Delete') {
	$att_del = array();
	foreach ($_POST as $param_name => $param_val) {
		if (is_string($param_val) and $param_val) {
			$param_val = "'$param_val'";
		}
		if ($param_val) {
			$att_del[] = "$param_name = $param_val";
		}
	}
	array_pop($att_del);

	$sql_delete = "DELETE FROM RECRUITER
					WHERE ". implode(" AND ", $att_del);

	if ($conn->query($sql_delete) == TRUE && $conn->affected_rows >= 1) {
			echo "<br>$sql_delete<br>";
		    echo "<br><b>Values deleted</b><br>";
	} else {
		    echo "<br><b>Error deleting values</b> " . $conn->error . "<br>";
	}
}


// SQL statement for creating a table
$sql_select = "SELECT * FROM RECRUITER";

echo "<br>See values below:";
if ($result = $conn->query("SELECT * FROM RECRUITER")) {
    printf("Select returned %d rows.\n", $result->num_rows);
}

$result = $conn->query($sql_select);

// Set styles and Column names
echo "<style>
table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    text-align: left;
    padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}
</style>";

echo "<div style='overflow-x:auto;'>
<table border='1'>
<tr>
<th>ID</th>
<th>FirstName</th>
<th>LastName</th>
<th>Position</th>
<th>DepartmentID</th>
</tr>";

// Fill in data
while($row = $result->fetch_assoc())
{
echo "<tr>";
echo "<td>" . $row['ID'] . "</td>";
echo "<td>" . $row['FirstName'] . "</td>";
echo "<td>" . $row['LastName'] . "</td>";
echo "<td>" . $row['Position'] . "</td>";
echo "<td>" . $row['DepartmentID'] . "</td>";
echo "<tr>";
}
echo "</table>";
echo "</div>";
?>

<html>
	<body>
		<br>
		<form action='recruiter.php' method='post'>
			ID: <input type='text' name='ID'><br>
			FirstName: <input type='text' name='FirstName'><br>
			LastName: <input type='text' name='LastName'><br>
			Position: <input type='text' name='Position'><br>
			DepartmentID: <input type='text' name='DepartmentID'><br>
			<input type='submit' name='action' value='Insert'>
			<input type='submit' name='action' value='Delete'>
		</form>
	</body>
</form>

