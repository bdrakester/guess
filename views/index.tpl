<!DOCTYPE html>
<html>
<head>
<title>Guess!</title>
<link rel="stylesheet" type="text/css" href="static/css/style.css">
</head>
<body>
<h1 class="title">Welcome to Guess! </h1>
<h2 class="title">The number guessing game</h2>
<fieldset>
	<legend>Make a guess...</legend>
	<form action="/" method="POST">
		<p>{{output if defined('output') else ""}}</p>
		<input type="text" name="guess">
		<br>
		<input type="submit" value="Guess!">
	</form>
	<br>
	<form action="/newgame" method="POST">
		<input type="submit" value="New Game">
	</form>
</fieldset>

</body>
<html>
