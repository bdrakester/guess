<!DOCTYPE html>
<html>
<head>
<title>Guess!</title>
<link rel="stylesheet" type="text/css" href="static/css/style.css">
</head>
<body>
<h1 class="title">Congratulations!! </h1>
<h2 class="title">You are right, the number was {{number}}</h2>
<center><img src="static/img/dancingbaby.gif"></center>
<br><br>
<h2 class="title">Play Again?</h2>
<center>
<form action="/newgame" method="POST">
	<input type="submit" value="New Game">
</form>
</center>
</fieldset>

</body>
<html>
