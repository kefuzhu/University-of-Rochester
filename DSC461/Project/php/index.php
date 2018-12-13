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
  <h1>Careers at Fastest HK Journalist</h1>
  <p><b>Open Positions</b></p>
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
      !(/^[A-z0-9 \,\.\-\#\&\@]*$/i).test(f.value)?f.value = f.value.replace(/[^A-z0-9 \,\.\-\#\&\@]/ig,''):null;
      } 
      </script>
      <form action='index.php' method='post'>
      JobID: <input type='number' name='ID' min='10000001' max='99999999'><br>
      Title: <input type='text' name='Title' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      Type: <select name='Type'>
        <option value=''>Please Select..</option>
        <option value='FullTime'>Full-time</option>
        <option value='PartTime'>Part-time</option>
      </select><br>
      Department: <input type='text' name='Name' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      City: <input type='text' name='City' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
      State: <select name='State'>
        <option value=''>Please Select..</option>
        <option value='AL'>Alabama</option>
        <option value='AK'>Alaska</option>
        <option value='AZ'>Arizona</option>
        <option value='AR'>Arkansas</option>
        <option value='CA'>California</option>
        <option value='CO'>Colorado</option>
        <option value='CT'>Connecticut</option>
        <option value='DE'>Delaware</option>
        <option value='DC'>District Of Columbia</option>
        <option value='FL'>Florida</option>
        <option value='GA'>Georgia</option>
        <option value='HI'>Hawaii</option>
        <option value='ID'>Idaho</option>
        <option value='IL'>Illinois</option>
        <option value='IN'>Indiana</option>
        <option value='IA'>Iowa</option>
        <option value='KS'>Kansas</option>
        <option value='KY'>Kentucky</option>
        <option value='LA'>Louisiana</option>
        <option value='ME'>Maine</option>
        <option value='MD'>Maryland</option>
        <option value='MA'>Massachusetts</option>
        <option value='MI'>Michigan</option>
        <option value='MN'>Minnesota</option>
        <option value='MS'>Mississippi</option>
        <option value='MO'>Missouri</option>
        <option value='MT'>Montana</option>
        <option value='NE'>Nebraska</option>
        <option value='NV'>Nevada</option>
        <option value='NH'>New Hampshire</option>
        <option value='NJ'>New Jersey</option>
        <option value='NM'>New Mexico</option>
        <option value='NY'>New York</option>
        <option value='NC'>North Carolina</option>
        <option value='ND'>North Dakota</option>
        <option value='OH'>Ohio</option>
        <option value='OK'>Oklahoma</option>
        <option value='OR'>Oregon</option>
        <option value='PA'>Pennsylvania</option>
        <option value='RI'>Rhode Island</option>
        <option value='SC'>South Carolina</option>
        <option value='SD'>South Dakota</option>
        <option value='TN'>Tennessee</option>
        <option value='TX'>Texas</option>
        <option value='UT'>Utah</option>
        <option value='VT'>Vermont</option>
        <option value='VA'>Virginia</option>
        <option value='WA'>Washington</option>
        <option value='WV'>West Virginia</option>
        <option value='WI'>Wisconsin</option>
        <option value='WY'>Wyoming</option>
      </select><br>
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

    echo "<br><b>Please fillout the form below to apply: </b><br><br>";
    echo "<form action='index.php' method='post'>
        JobID:<input type='text' name='JobID' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        FirstName: <input type='text' name='FirstName' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        LastName: <input type='text' name='LastName' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        Email: <input type='text' name='Email' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        School: <input type='text' name='School' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        Degree: <input type='text' name='Degree' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        Major: <input type='text' name='Major' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        Source (Where did you find this position): <input type='text' name='Platform' onkeyup='valid_1(this)' onblur='valid_1(this)'><br>
        <input type='submit' name='action' value='submit'>
        </form>";

    // Search
    if ($_POST[action] == 'Search') {
      $att_sel = array();
      foreach ($_POST as $param_name => $param_val) {
        if ($param_val) {
          $att_sel[] = "$param_name = '$param_val'";
        }
      }
      array_pop($att_sel);

      $sql_select = "SELECT P.ID, P.Title, P.Type, D.Name, O.City, O.State
                    FROM POSITION_ AS P
                    LEFT JOIN DEPARTMENT AS D ON P.DepartmentID=D.ID
                    LEFT JOIN OFFICE AS O ON D.OfficeID=O.ID
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
        <th>JobID</th>
        <th>Title</th>
        <th>Type</th>
        <th>Department</th>
        <th>City</th>
        <th>State</th>
        </tr>";

        // Fill in data
        while($row = $result->fetch_assoc())
        {
        echo "<tr>";
        echo "<td>" . $row['ID'] . "</td>";
        echo "<td>" . $row['Title'] . "</td>";
        echo "<td>" . $row['Type'] . "</td>";
        echo "<td>" . $row['Name'] . "</td>";
        echo "<td>" . $row['City'] . "</td>";
        echo "<td>" . $row['State'] . "</td>";
        echo "<tr>";
        }
        echo "</table>";
        echo "</div>";
      } else {
        echo "<br><b>Error searching values: </b>" . "All the fields are empty!";
      }

    }

// Insert
if ($_POST[action] == 'submit' && $_POST[JobID]) {

  if(!(ereg("@",$_POST[Email]))){
    echo "<br><b>Please enter valid email address</b>";
  } elseif($_POST[JobID] == ''|$_POST[FirstName] == ''|$_POST[LastName] == ''|$_POST[Email] == ''|
           $_POST[School] == ''|$_POST[Degree] == ''|$_POST[Major] == ''|$_POST[Platform] == ''){
    echo "<br><b>Please do not leave any box empty</b>";
  }
  else{
    // Insert values for APPLICANT relation
    $sql_insert = "INSERT INTO APPLICANT (Email,FirstName,LastName,School,Degree,Major)
        VALUES ('$_POST[Email]', '$_POST[FirstName]', 
        '$_POST[LastName]', '$_POST[School]', '$_POST[Degree]', '$_POST[Major]')";

    if ($conn->query($sql_insert) === TRUE && $conn->affected_rows == 1) {
      
        $sql_update = "UPDATE APPLICANT SET Applicant_ID = CONCAT('A',10000+ID)";
        $conn->query($sql_update);

       // Insert values for APPLY_TO relation 
      $sql_insert = "INSERT INTO APPLY_TO
                    VALUES ((SELECT Applicant_ID FROM APPLICANT ORDER BY ID DESC LIMIT 1),
                    '$_POST[JobID]','$_POST[Platform]')";
      if ($conn->query($sql_insert) === TRUE && $conn->affected_rows == 1) {
        echo "<br><b>Thanks! We've received your application. Have a nice day!</b>";
      } else{
        echo "<br><b>Sorry, we did not receive your application. Please make sure you entered a correct JobID and submit a new one. If the problem persists, please contact us: zxu17@ur.rochester.edu</b><br><br>";
        echo "<b>Error message: </b>" . $conn->error;
        $sql = "DELETE FROM APPLICANT ORDER BY ID DESC LIMIT 1";
        $conn->query($sql);
      }
    } else {        
      echo "<br><b>Sorry, we did not receive your application. Please submit a new one or contact us: zxu17@ur.rochester.edu</b><br><br>" . $conn->error;
        echo "<b>Error message: </b>" . $conn->error;
        $sql = "DELETE FROM APPLICANT ORDER BY ID DESC LIMIT 1";
      $conn->query($sql);
    }
  }
} elseif ($_POST[action] == 'submit') {
      echo "<br><b>Please enter a correct JobID and fill out as many fields as you can. If you have any question, please contact us: zxu17@ur.rochester.edu</b>";
}

    // Normally display the table
    if ($_POST[action] == 'Search' && $att_sel) {
      
    } else {
    	echo "</form>
    		</ul>
  			</nav>
  			<article>";
      // SQL statement for creating a table
      $sql_select = "SELECT P.ID, P.Title, P.Type, D.Name, O.City, O.State
                    FROM POSITION_ AS P
                    LEFT JOIN DEPARTMENT AS D ON P.DepartmentID=D.ID
                    LEFT JOIN OFFICE AS O ON D.OfficeID=O.ID";

      echo "See values below:";
      if ($result = $conn->query($SQL_select)) {
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
      <th>JobID</th>
      <th>Title</th>
      <th>Type</th>
      <th>Department</th>
      <th>City</th>
      <th>State</th>
      </tr>";

      // Fill in data
      while($row = $result->fetch_assoc())
      {
      echo "<tr>";
      echo "<td>" . $row['ID'] . "</td>";
      echo "<td>" . $row['Title'] . "</td>";
      echo "<td>" . $row['Type'] . "</td>";
      echo "<td>" . $row['Name'] . "</td>";
      echo "<td>" . $row['City'] . "</td>";
      echo "<td>" . $row['State'] . "</td>";
      echo "<tr>";
      }
      echo "</table>";
      echo "</div>";
    }
    
  echo "</article>
</section>";

echo "</body>";
?>

