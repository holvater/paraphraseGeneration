<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, height=device-height, minimum-scale=1.0, maximum-scale=1.0">
    <title>Parafrasis</title>
    <link rel="shortcut icon" href="favicon.ico"/>
    <link href='http://fonts.googleapis.com/css?family=Muli:300,300italic|Montserrat:700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="style.min.css">
</head>
<body>
    <div class="header">Par&aacute;frasis</div>
    <form action="/" method="post">
        <div class="form">
            <div class="input__wrapper">
                <input id="input--sentence" class="input--sentence" type="text" name="oracionInput" placeholder="Escribe texto aqu&iacute;"><br/>
                <input id="input--number" class="input--number" type="number" name="cantidadInput" value="{{cantidad}}" min="1" max="10"/>
                <label for="input--number">oraciones a generar (entre 1 y 10)</label>
            </div>
            <input class="button" type="submit" name="generar" value="Generar">
        </div>
        <div class="results">
            <h2>FRASE ORIGINAL:</h2>
            <p class="original-sentence">{{oracion}}</p>
            <h2>RESULTADOS:</h2>
            <ul>

                %for oracion in oraciones:
                    <li>
                        {{oracion}}
                    </li>
                %end
            </ul>
            
        </div>
        
    </form>
</body>
</html>