# black-list-devops


## Paso a paso

  ####  1 Crear el ambiente 
  ####  2 pip install -r requirements.txt 
  ####  3 python run.py 

# curl

## Para agregar un email a la lista negra:

curl -X POST http://127.0.0.1:5001/blacklists \
-H "Content-Type: application/json" \
-H "Authorization: Bearer blacklist-secret-token-2024" \
-d '{
    "email": "test@example.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Spam"
}'

## Para verificar si un email está en la lista negra:

curl http://127.0.0.1:5001/blacklists/test@example.com \
-H "Authorization: Bearer blacklist-secret-token-2024"

## Pruebas de postman en 

 postman_collection.json
