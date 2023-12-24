Al solicitar Token: 
    token, create = Token.objects.get_or_create(user=user)
    return Response({"token":token.key, "estado":create})

create me indica si es la primera vez que se usa el token, 
o sea si fue creado. 

Es útil por ejemplo si acaba de iniciar sesión. Se le crea un token.
Si luego debe pedirlo nuevamente, create será False. Por lo que el usuario continua
con su sesión. 

Mirar eso de Django Channels y ver en qué aplicar mejor