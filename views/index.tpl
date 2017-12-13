<!DOCTYPE html>
<html>
<head>
<title>Guess!</title>
<link rel="stylesheet" type="text/css" href="static/css/style.css">
</head>
<body>
<h1 class="title">Welcome to Guess! </h1>
<h2 class="title">The number guessing game</h2>
<form action="/" method="POST">
	<fieldset>
	<p>{{output if defined('output') else ""}}</p>
	<legend>Make a guess...</legend>
	<input type="text" name="guess">
	<br>
	<input type="submit" value="Guess!">
	</fieldset>
</form>
</body>
<html>
