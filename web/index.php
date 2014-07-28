<!DOCTYPE HTML>

<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<META http-equiv='refresh' content='30'> 
<title>UPLOAD LOG</title>

<script src="js/jquery-1.11.0.min.js"></script>
<link rel="stylesheet" href="css/bootstrap.min.css">
<link rel="stylesheet" href="css/bootstrap-theme.min.css">
<script src="js/bootstrap.min.js"></script>

<link rel="stylesheet" href="flow.css">

<script>
$(function () { 
    $("[data-toggle='tooltip']").tooltip(); 
});
</script>

</head>

<body>

<div class="panel panel-default">
  <div class="panel-body">
    <h1><span class="label label-success">Upload log</span></h1>
    <a href="flow.html" class="btn btn-default btn-xs pull-right"><span class="glyphicon glyphicon-stats"></span> View log file</a>

<table class="table table-striped table-hover table-bordered">
<tr>
  <th>Дата</th>
  <th>Имя файла</th>
  <th>Машина</th>
  <th>Комплекты, шт.</th>
  <th>Формы, шт</th>
  <th>Вывод</th>
  <th>залито вывод</th>
  <th>залито кинап</th>
</tr>
<?php
include "data.php"
?>
</table>

</div>
</div>
</body>
</html>
