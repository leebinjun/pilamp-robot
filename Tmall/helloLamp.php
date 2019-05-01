
<?php
  $myfile = fopen("afile.txt", "r") or die("Unable to open file!");
  echo fread($myfile,filesize("afile.txt"));
  fclose($myfile);
?>

