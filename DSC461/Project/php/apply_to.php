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
      !(/^[0-9]*$/i).test(f.value)?f.value = f.value.replace(/[^0-9]/ig,''):null;
      }
      function valid_3(f) {
      !(/^(A\d{5}){1}$/).test(f.value)?f.value = f.value.replace(/[^(A{1}\d{5})$]/g,''):null;
      }
      </script>
      <form action='apply_to.php' method='post'>
      ApplicantID: <input type='text' name='ApplicantID' onkeyup='valid_3(this)' onblur='valid_3(this)'><br>
      PositionID: <input type='number' name='PositionID' min='10000000' max='99999999'><br>
      AdsPlatform: <input type='text' name='AdsPlatform' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
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
    if ($_POST[action] == 'Insert' && $_POST[ApplicantID] && $_POST[PositionID]) {
      if(!ereg("^A[0-9]{5}$",$_POST[ApplicantID])){
        echo "<br><b>Must Enter Correct ID Format.</b>";
      } else{
        $sql_insert = "INSERT INTO APPLY_TO
          VALUES ('$_POST[ApplicantID]', '$_POST[PositionID]', '$_POST[AdsPlatform]')";
      echo "<br><b>Equivalent SQL query:</b><br>$sql_insert<br>";

        if ($conn->query($sql_insert) === TRUE && $conn->affected_rows == 1) {
            echo "<br><b>Values added</b>";
        } else {
            echo "<br><b>Error adding values: </b>" . $conn->error;
        }

      }
    } elseif ($_POST[action] == 'Insert') {
      echo "<br><b>Error adding values: </b>" . "The ID field is empty!";
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
        $sql_delete = "DELETE FROM APPLY_TO
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

      $sql_select = "SELECT * FROM APPLY_TO
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
        <th>ApplicantID</th>
        <th>PositionID</th>
        <th>AdsPlatform</th>
        </tr>";

        // Fill in data
        while($row = $result->fetch_assoc())
        {
        echo "<tr>";
        echo "<td>" . $row['ApplicantID'] . "</td>";
        echo "<td>" . $row['PositionID'] . "</td>";
        echo "<td>" . $row['AdsPlatform'] . "</td>";
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
      $sql_select = "SELECT * FROM APPLY_TO";

      echo "See values below:";
      if ($result = $conn->query("SELECT * FROM APPLY_TO")) {
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
      <th>ApplicantID</th>
      <th>PositionID</th>
      <th>AdsPlatform</th>
      </tr>";

      // Fill in data
      while($row = $result->fetch_assoc())
      {
      echo "<tr>";
      echo "<td>" . $row['ApplicantID'] . "</td>";
      echo "<td>" . $row['PositionID'] . "</td>";
      echo "<td>" . $row['AdsPlatform'] . "</td>";
      echo "<tr>";
      }
      echo "</table>";
      echo "</div>";
    }
    
  echo "</article>
</section>";

echo "</body>";
?>

