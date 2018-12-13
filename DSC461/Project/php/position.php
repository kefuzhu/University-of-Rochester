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
      !(/^(E\d{5}){1}$/).test(f.value)?f.value = f.value.replace(/[^E\d$]/g,''):null;
      }
      </script>
      <form action='position.php' method='post'>
      ID: <input type='number' name='ID' min='10000001' max='99999999'><br>
      Type: <select name='Type'>
        <option value=''>Please Select..</option>
        <option value='FullTime'>Full-time</option>
        <option value='PartTime'>Part-time</option>
      </select><br>
      Title: <input type='text' name='Title' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      DepartmentID: <input type='number' name='DepartmentID' min='101' max=999><br>
      RecruiterID: <input type='text' name='RecruiterID' onkeyup='valid_3(this)' onblur='valid_3(this)'><br>
      PostDate: <input type='text' name='PostDate' minlength='10' maxlength='10' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      Salary: <input type='number' min='0' max='10000000'><br>
      VisaSponsorship: <select name='VisaSponsorship'>
        <option value=''>Please Select..</option>
        <option value='YES'>YES</option>
        <option value='NO'>NO</option>
        </select><br>
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
    if ($_POST[action] == 'Insert' && $_POST[ID]) {
    	if(!(ereg("^E[0-9]{5}$",$_POST[RecruiterID]))){
        echo "<br><b>Error adding values: </b>Must enter a valid RecuiterID!";
      } elseif(!(preg_match("/^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/",$_POST[PostDate]))){
      	echo "<br><b>Error adding values: </b>Must enter a valid PostDate format!";
      } else{

        if($_POST[Type] == '' && $_POST[VisaSponsorship] == ''){
          $sql_insert = "INSERT INTO POSITION_(ID,Title,DepartmentID,RecruiterID,PostDate,Salary)
                        VALUES ('$_POST[ID]', '$_POST[Title]', '$_POST[DepartmentID]', 
                        '$_POST[RecruiterID]', '$_POST[PostDate]', '$_POST[Salary]')";
        } elseif($_POST[Type] = ''){
          $sql_insert = "INSERT INTO POSITION_(ID,Title,DepartmentID,RecruiterID,PostDate,Salary,VisaSponsorship)
                        VALUES ('$_POST[ID]', '$_POST[Title]', '$_POST[DepartmentID]', 
                        '$_POST[RecruiterID]', '$_POST[PostDate]', '$_POST[Salary]','$_POST[VisaSponsorship]')";
        } elseif($_POST[VisaSponsorship] = ''){
          $sql_insert = "INSERT INTO POSITION_(ID,Type,Title,DepartmentID,RecruiterID,PostDate,Salary)
                        VALUES ('$_POST[ID]', '$_POST[Type]', '$_POST[Title]', '$_POST[DepartmentID]', 
                        '$_POST[RecruiterID]', '$_POST[PostDate]', '$_POST[Salary]')";
        } else{
          $sql_insert = "INSERT INTO POSITION_
                        VALUES ('$_POST[ID]', '$_POST[Type]', '$_POST[Title]', '$_POST[DepartmentID]', 
                        '$_POST[RecruiterID]', '$_POST[PostDate]', '$_POST[Salary]', '$_POST[VisaSponsorship]')";
        }

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
        $sql_delete = "DELETE FROM POSITION_
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

      $sql_select = "SELECT * FROM POSITION_
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
      $sql_select = "SELECT * FROM POSITION_";

      echo "See values below:";
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
    }
    
  echo "</article>
</section>";

echo "</body>";
?>

