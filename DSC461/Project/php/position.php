<html>
<body>

<h1>Job Application Database</h1>
<p>-- by Fastest HK Journalist (#11)</p>
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
else print "<br>Connection OK!</br>";

// Insert
if ($_POST[action] == 'Insert' && $_POST[ID]) {

	if(!(ereg("^\d{4}-\d{2}-\d{2}$",$_POST[PostDate]))){
		echo "<br><b>Must Enter Correct Date Format for PostDate</b>";
	}
	else{
		$sql_insert = "INSERT INTO POSITION_
				VALUES ('$_POST[ID]', '$_POST[Type]', 
				'$_POST[Title]', '$_POST[DepartmentID]', '$_POST[RecruiterID]', '$_POST[PostDate]', '$_POST[Salary]', '$POST_[VisaSponsorship]')";

		if ($conn->query($sql_insert) === TRUE && $conn->affected_rows == 1) {
		    echo "<br><b>Values added</b>";
		} else {
		    echo "<br><b>Error adding values: </b>" . $conn->error;
		}
	}
}

// Delete
if ($_POST[action] == 'Delete') {
	$att_del = array();
	foreach ($_POST as $param_name => $param_val) {
		if ($param_val) {
			$att_del[] = "$param_name = '$param_val'";
		}
	}
	array_pop($att_del);

	$sql_delete = "DELETE FROM POSITION_
					WHERE ". implode(" AND ", $att_del);
	echo "<br>$sql_delete";

	if ($conn->query($sql_delete) === TRUE && $conn->affected_rows >= 1) {
		    echo "<br><b>Values deleted</b>";
		} else {
		    echo "<br><b>Error deleting values: </b>" . $conn->error;
		}

}


// SQL statement for creating a table
$sql_select = "SELECT * FROM POSITION_";

echo "<br style='background-color:rgb(255,0,0)'>See values below:";
if ($result = $conn->query("SELECT * FROM POSITION_")) {
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
<th>Type</th>
<th>Title</th>
<th>DepartmentID</th>
<th>RecruiterID</th>
<th>PostDate</th>
<th>Salary</th>
<th>VisaSponsorship</th>
</tr>";

// Fill in data
while($row = $result->fetch_assoc())
{
echo "<tr>";
echo "<td>" . $row['ID'] . "</td>";
echo "<td>" . $row['Type'] . "</td>";
echo "<td>" . $row['Title'] . "</td>";
echo "<td>" . $row['DepartmentID'] . "</td>";
echo "<td>" . $row['RecruiterID'] . "</td>";
echo "<td>" . $row['PostDate'] . "</td>";
echo "<td>" . $row['Salary'] . "</td>";
echo "<td>" . $row['VisaSponsorship'] . "</td>";
echo "<tr>";
}
echo "</table>";
echo "</div>";
?>

<html>
<form action='position.php' method='post'>
ID: <input type='text' name='ID'><br>
Type: <input type='text' name='Type'><br>
Title: <input type='text' name='Title'><br>
DepartmentID: <input type='text' name='DepartmentID'><br>
RecruiterID: <input type='text' name='RecruiterID'><br>
PostDate: <input type='text' name='PostDate'><br>
Salary: <input type='text' name='Salary'><br>
VisaSponsorship: <input type='text' name='VisaSponsorship'><br>
<input type='submit' name='action' value='Insert'>
<input type='submit' name='action' value='Delete'>
</form>
</html>

