<?php
if ($_POST["label"]) {
    $label = $_POST["label"];
}

if(isset($_POST['label']))
{
$fname = $_POST['label'];
echo "<span class='success'>Form Submitted By <b>POST METHOD</b></span><br/>";
echo "First Name : ".$fname;
}

?>