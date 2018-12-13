<!DOCTYPE html>
<html>


<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
/* Set the layout of the whole page */

* {
  box-sizing: border-box;
}

body {
  font-family: Arial, Helvetica, sans-serif;
}

header {
  text-align: center;
  font-size: 15px;
  border-bottom: solid grey;
}

nav {
  float: left;
  width: 25%;
  height: 500px;
  padding: 20px;
}

nav ul {
  list-style-type: none;
  padding: 0;
}

article {
  float: left;
  padding: 20px;
  width: 75%;
}

section:after {
  content: "";
  display: table;
  clear: both;
}

@media (max-width: 600px) {
  nav, article {
    width: 100%;
    height: auto;
  }
}
</style>
</head>


<?php
  echo "<body>";

// Content of header
echo '<header>
  <h2>Job Application Database</h2>
  <p> -- By Fastest HK Journalist (#11)</p>
  <table style="width:80%;" align="center">
    <tr>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/office.php">Offices</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/department.php">Departments</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/recruiter.php">Recruiters</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/position.php">Positions</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/applicant.php">Applicants</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/apply_to.php">Applications</a></th>
    <th><a href="http://betaweb.csug.rochester.edu/~zxu17/adsplatform.php">AdsPlatforms</a></th>
    </tr>
  </table>
</header>';

// Content of control panel
echo "<section>
  <nav>
    <ul>
      <meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
      <meta http-equiv='Content-Style-Type' content='text/css'>
      <meta http-equiv='Content-Script-Type' content='text/javascript'>
      <script type='text/JavaScript'>
      function valid_1(f) {
      !(/^[A-z0-9 \,\.\-\#\&]*$/i).test(f.value)?f.value = f.value.replace(/[^A-z0-9 \,\.\-\#\&]/ig,''):null;
      } 
      function valid_2(f) {
      !(/^[A-z0-9 \@\.\_\-]*$/i).test(f.value)?f.value = f.value.replace(/[^A-z0-9 \@\.\_\-]/ig,''):null;
      } 
      function valid_4(f) {
      !(/^(A\d{5}){1}$/).test(f.value)?f.value = f.value.replace(/[^(A{1}\d{5})$]/g,''):null;
      } 
      </script>
      <form action='applicant.php' method='post'>
      ID (Do not use for Insert): <input type='text' name='Applicant_ID' onkeyup='valid_4(this)' onblur='valid_4(this)'><br>
      Email: <input type='text' name='Email' onkeyup='valid_2(this)' onblur='valid_2(this)'><br>
      FirstName: <input type='text' name='FirstName' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      LastName: <input type='text' name='LastName' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      School: <input type='text' name='School' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      Degree: <input type='text' name='Degree' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      Major: <input type='text' name='Major' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      <input type='submit' name='action' value='Insert'>
      <input type='submit' name='action' value='Delete'>
      <input type='submit' name='action' value='Search'>
      <input type='submit' name='action' value='Reset'>";

      echo "<br>
      		<br>
      		<br>";
  
    $server = "localhost";
    $user = "zxu17";
    $password = "Dvdb25iZ";
    $db = "zxu17_1";

    print "Testing connection with ".$db;

    // creating the connection

    $conn = new mysqli($server, $user, $password, $db);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    else print "<br>Connection OK!</br>";

    // Insert
        if ($_POST[action] == 'Insert') {
          if(!(ereg("@",$_POST[Email]))){
        echo "<br><b>Error adding values: </b>Must Enter a correct email!";
      } else {$sql_insert = "INSERT INTO APPLICANT (Email,FirstName,LastName,School,Degree,Major)
        VALUES ('$_POST[Email]', '$_POST[FirstName]', 
        '$_POST[LastName]', '$_POST[School]', '$_POST[Degree]', '$_POST[Major]')";
        $sql_update = "UPDATE APPLICANT SET Applicant_ID = CONCAT('A',10000+ID)";
            echo "<br><b>Equivalent SQL query:</b><br>$sql_insert<br>";

            if ($conn->query($sql_insert) === TRUE && $conn->query($sql_update) === TRUE && $conn->affected_rows == 1) {
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

      if ($att_del) {
        $sql_delete = "DELETE FROM APPLICANT
                WHERE ". implode(" AND ", $att_del);
        echo "<br><b>Equivalent SQL query:</b><br>$sql_delete<br>";

        if ($conn->query($sql_delete) === TRUE && $conn->affected_rows >= 1) {
              echo "<br><b>Values deleted</b>";
          } else {
              echo "<br><b>Error deleting values: </b>" . $conn->error;
          }
      } else {
        echo "<br><b>Error deleting values: </b>" . "All the fields are empty!";
      }
    }

    // Search
    if ($_POST[action] == 'Search') {
      $att_sel = array();
      foreach ($_POST as $param_name => $param_val) {
        if ($param_val) {
          $att_sel[] = "$param_name = '$param_val'";
        }
      }
      array_pop($att_sel);

      $sql_select = "SELECT * FROM APPLICANT
              WHERE ". implode(" AND ", $att_sel);

      if ($att_sel) {
        echo "<br><b>Equivalent SQL query:</b><br>$sql_select<br>";
        echo "</form>
    		</ul>
  			</nav>
  			<article>";
        echo "<br style='background-color:rgb(255,0,0)'>See values below:";
        if ($result = $conn->query($sql_select)) {
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
        <th>Email</th>
        <th>FirstName</th>
        <th>LastName</th>
        <th>School</th>
        <th>Degree</th>
        <th>Major</th>
        </tr>";

        // Fill in data
        while($row = $result->fetch_assoc())
        {
        echo "<tr>";
        echo "<td>" . $row['Applicant_ID'] . "</td>";
        echo "<td>" . $row['Email'] . "</td>";
        echo "<td>" . $row['FirstName'] . "</td>";
        echo "<td>" . $row['LastName'] . "</td>";
        echo "<td>" . $row['School'] . "</td>";
        echo "<td>" . $row['Degree'] . "</td>";
        echo "<td>" . $row['Major'] . "</td>";
        echo "<tr>";
        }
        echo "</table>";
        echo "</div>";
      } else {
        echo "<br><b>Error searching values: </b>" . "All the fields are empty!";
      }

    }

    // Normally display the table
    if ($_POST[action] == 'Search' && $att_sel) {
      
    } else {
    	echo "</form>
    		</ul>
  			</nav>
  			<article>";
      // SQL statement for creating a table
      $sql_select = "SELECT * FROM APPLICANT";

      echo "See values below:";
      if ($result = $conn->query("SELECT * FROM APPLICANT")) {
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
      <th>Email</th>
      <th>FirstName</th>
      <th>LastName</th>
      <th>School</th>
      <th>Degree</th>
      <th>Major</th>
      </tr>";

      // Fill in data
      while($row = $result->fetch_assoc())
      {
      echo "<tr>";
      echo "<td>" . $row['Applicant_ID'] . "</td>";
      echo "<td>" . $row['Email'] . "</td>";
      echo "<td>" . $row['FirstName'] . "</td>";
      echo "<td>" . $row['LastName'] . "</td>";
      echo "<td>" . $row['School'] . "</td>";
      echo "<td>" . $row['Degree'] . "</td>";
      echo "<td>" . $row['Major'] . "</td>";
      echo "<tr>";
      }
      echo "</table>";
      echo "</div>";
    }
    
  echo "</article>
</section>";

echo "</body>";
?>

