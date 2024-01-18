- map_my_crop contain enviroment folder django project folder and requirement.txt
- requirment.txt file contain all the packages. I have use in project or we can use ENV(enviroment) wich conatin all required packeges.
- go through with mmc_assistment folder which contain sqlite data base, inner project folder, api app folder and manage.py file.
- to run the project use use following command
- python manage.py runserver
- After succesfull execution
- use following API
- Register user
curl --location 'http://127.0.0.1:8000/userapi/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "akk",
    "email": "akk@gmail.com",
    "password": "ankit@123"

}'

- Get authentication key
- curl --location 'http://127.0.0.1:8000/gettoken/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=admin' \
--data-urlencode 'password=1234'

- Get historical wheather data
- curl --location 'http://127.0.0.1:8000/sample/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NTg0Nzk1LCJpYXQiOjE3MDU1ODQxOTUsImp0aSI6IjY5NjBmNTlhNTM2MjQ5YWI4MGNiNTEyNzEwNzNhOGFjIiwidXNlcl9pZCI6MX0.Qd5iQVYHBzR3uVg4DorbZh1kH-WaDJMaiZowHbckEEY' \
--header 'Content-Type: application/json' \
--data '{
    "latitude": 17.4162,
    "longitude": 78.463,
    "start_date": "2024-01-01",
    "end_date": "2024-01-10"

}'

