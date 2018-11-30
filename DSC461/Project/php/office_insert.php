<html>
	<body>
		<b>Insert Data</b>

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
		else print "<br>Connection OK!";

		echo"<br>";

		if ($_POST) {
			$sql_insert = "INSERT INTO OFFICE
					VALUES ('$_POST[ID]', '$_POST[StreetAddress]', 
					'$_POST[City]', '$_POST[State]', '$_POST[ZipCode]')";

			if ($conn->query($sql_insert) === TRUE) {
			    echo "<br><b>Values added</b><br>";
			} else {
			    echo "<br><b>Error adding values</b> " . $conn->error . "<br>";
			}
		}
		?>

		<br>

		<form action='insert.php' method='post'>
			ID: <input type='text' name='ID'><br>
			StreetAddress: <input type='text' name='StreetAddress'><br>
			City: <input type='text' name='City'><br>
			State (2 Characters): <input type='text' name='State' maxlength="5"><br>
			ZipCode: <input type='text' name='ZipCode'><br>
			<input type='submit'>
		</form>


	</body>
</html>