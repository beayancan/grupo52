# IIC2413 - Entrega 4


## Instrucciones

* La base de datos en mongo debe llamarse `grupo52`
* Para importar la base de dato usuarios.json a la collection `usuarios` se debe utilizar el comando
`mongoimport --db grupo52 --collection usuarios --drop --file usuarios.json --jsonArray`
* Para importar la base de dato messages.json a la collection `messages` se debe utilizar el comando
`mongoimport --db grupo52 --collection messages --drop --file messages.json --jsonArray`

* Para hacer la busqueda de texto es necesario un indice, por lo que se debe utilizar el comando
`db.messages.createIndex({message: "text"})`


 ## Funcionamiento

 * Para buscar un mensaje por su `id`, es necesario ir a la ruta `/message_id/<id mensaje>`. En donde `<id mensaje>` es un valor entre 1000 en adelante.

 * Para buscar la información de un usuarios y los mensajes asociados a este, es necesario ir a la ruta `/user_messages/<id usuario`, en donde `<id usaurio>` corresponde a un número desde 0 hasta 118. Los mensajes apareceran en el atributo `messages` del usuario retornado

* Para buscar los mensajes que dos usuarios es necesario ir a la ruta `/between_users/<id_user_1>/<id_user_2>`, en donde cada `<id_user>` corresponde a uno de los usuarios. Este retorna los mensajes enviados entre ellos, independiente del orden en que se ingresen los usuarios, estando ordenados los mensajes por fecha de envío. Por ejemplo: los usuarios 21 y 31.

* Para buscar frases que obligatoriamente deben estar presentes en mensajes, es necesario ir a la ruta `/find_words/<frases>` en donde frases debe corresponder a una lista separada por comas con los string de frases que se busquen. Por ejemplo
`/find_words/["Hola", "mi vida"]`

* Para buscar mensajes con frases que no necesariamente deben estar todas presentes en mensajes, es necesario ir a la ruta `/find_words_2/<frases>` en donde frases debe corresponder a una lista separada por comas con los string de frases que se busquen. Por ejemplo
`/find_words/["Hola", "mi vida"]` (a diferencia de la anterior esta tambien tendrá los mensajes que solo tienen "Hola" o solo tienen "mi vida")

* Para mansajes que no contengas ciertas frases, es necesario ir a la ruta `/not_find_words/<frases>` en donde frases debe corresponder a una lista separada por comas con los string de frases que se busquen. Por ejemplo
`/not_find_words/["Hola", "mi vida"]` (Retornará todos los mensajes que NO contengan ni "Hola" ni "mi vida)

* Para añadir un nuevo mensaje, se utilizó el  comando dado por ayudantía, por lo cual, es necesario
utilizar la ruta `/add_message/` y pasarle un json con los comandos necesarios. Se asume que el quien lo utiliza, ingresará adecuadamente los valoros (tipos, orden y nombre de la key) según el estandar predefinido. Además, que no incluirá una key `_id` dentro del json, pues este identificador
se obtiene mediante el propio programa como el maximo identificador + 1 (recordar que comenzaban desde el 1000).

* Para borrar un mensaje, se utiliza la ruta `/remove_message/<id_message>`, en donde se pasará el identificador del mensaje que se quiere borrar. Se asume que quien utiliza el sitio sabe que mensaje quiere borrar, y lo ingresa de forma correcta (recrodar que comienzan desde el 1000)

## Consideraciones
* Se añadió como `_id` a los usuarios el entero que le correspondía de la base de datos original en lugar del objeto por defecto de mongo
* Se añadió como `_id` a los mensajes de `messages.json` un entero que va desde 1000 en adelante según el orden en cual venían, para no tener que utilizar los objetos que mongo entrega por defecto