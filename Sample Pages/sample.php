Test Page (at least vulnerable to xss - don't use on live)<br/>
<?php
echo "<br/>GET input0:<br/>";
echo "<br/>input0=".($_GET["input0"])."<br/>";
echo "strlen(input0)=".strlen($_GET["input0"])."<br/>";
echo "mb_strlen(input0)=".mb_strlen($_GET["input0"], '8bit')."<br/><br/>";

echo "<br/>POST input1:<br/>";
echo "<br/>input1=".($_POST["input1"])."<br/>";
echo "strlen(input1)=".strlen($_POST["input1"])."<br/>";
echo "mb_strlen(input1)=".mb_strlen($_POST["input1"], '8bit')."<br/><br/>";

echo "<br/>COOKIE input2:<br/>";
echo "<br/>input2=".($_COOKIE["input2"])."<br/>";
echo "strlen(input2)=".strlen($_COOKIE["input2"])."<br/>";
echo "mb_strlen(input2)=".mb_strlen($_COOKIE["input2"], '8bit')."<br/><br/>";
?>
<?php
parse_str(file_get_contents("php://input"), $_POST_RAW);

$req_dump=str_repeat("-=", 20)."\r\n\$_SERVER:\r\n".print_r($_SERVER,true)."\r\n\$_POST:\r\n".print_r($_POST,true)."\r\n\$_GET:\r\n".print_r($_GET,true)."\r\n\$_FILES:\r\n".print_r($_FILES,true)."\r\n\$_POST_RAW:\r\n".print_r($_POST_RAW,true)."\r\n\$_COOKIE:\r\n".print_r($_COOKIE,true)."\r\n";

echo "<pre>".$req_dump."</pre>";

echo "<br/>generic parameter ( \$_REQUEST[\"input\"] ) input:<br/>";
echo "<br/>input=".($_REQUEST["input"])."<br/>";
echo "strlen(input)=".strlen($_REQUEST["input"])."<br/>";
echo "mb_strlen(input)=".mb_strlen($_REQUEST["input"], '8bit')."<br/><br/>"; 
?>

