<?php
// Welcoming script

$name = $_POST['name'];
$email = $_POST['email'];
echo "Welcome ".$name;
echo "<br>with email ".$email;
echo "<br>";
print_r(array_keys($_POST));
print_r(array_values($_POST));
?>
