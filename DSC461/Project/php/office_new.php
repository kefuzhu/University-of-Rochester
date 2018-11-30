<html>
	<body>
		<?php
		# Functino to check empty
		function allexist()
		{
		    foreach(func_get_args() as $arg)
		        if(empty($arg))
		            return false;
		        else
		            continue;
		    return true;
		}

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
		else print "<br>Connection OK!";

		echo"<br>";

		# Insert data into database
		if (isset($_POST['insert'])) {
			$sql_insert = "INSERT INTO OFFICE
						   VALUES ('$_POST[ID]', '$_POST[StreetAddress]', 
								   '$_POST[City]', '$_POST[State]', '$_POST[ZipCode]')";

			if ($conn->query($sql_insert) === TRUE) {
			    echo "<br><b>Values added</b><br>";
			} else {
			    echo "<br><b>Error adding values</b> " . $conn->error . "<br>";
			}
		}

		# Remove data from database
		else if (isset($_POST['delete']) {
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

			$sql_delete = "DELETE FROM OFFICE
							WHERE ". implode(" AND ", $att_del);
			echo "<br>$sql_delete";

			if ($conn->query($sql_delete) === TRUE) {
				    echo "<br>Values deleted";
				} else {
				    echo "<br>Error deleting values " . $conn->error;
				}

		}

			
		}

		// SQL statement for creating a table
		$sql_select = "SELECT * FROM OFFICE";

		echo "<br>See values below:";
		if ($result = $conn->query("SELECT * FROM OFFICE")) {
		    printf("Select returned %d rows.\n", $result->num_rows);
		}

		$result = $conn->query($sql_select);

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
		<th>StreetAddress</th>
		<th>City</th>
		<th>State</th>
		<th>ZipCode</th>
		</tr>";

		while($row = $result->fetch_assoc())
		{
		echo "<tr>";
		echo "<td>" . $row['ID'] . "</td>";
		echo "<td>" . $row['StreetAddress'] . "</td>";
		echo "<td>" . $row['City'] . "</td>";
		echo "<td>" . $row['State'] . "</td>";
		echo "<td>" . $row['ZipCode'] . "</td>";
		echo "<tr>";
		}
		echo "</table>";
		echo "</div>";
		?>

		<br>

		<form action='office.php' method='post'>
			ID: <input type='text' name='ID'><br>
			StreetAddress: <input type='text' name='StreetAddress'><br>
			City: <input type='text' name='City'><br>
			State (2 Characters): <input type='text' name='State' maxlength="2"><br>
			ZipCode: <input type='text' name='ZipCode' maxlength="5"><br>
			<input type='submit' name='insert' value='Insert'>
			<input type='submit' name='delete' value='Delete'>
		</form>

<!-- 		<form action="upload.php">
			<input type="submit" value="Upload Data">
		</form> -->
	</body>
</html>