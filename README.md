Video On Demand Chat [ Project for COMP 307 (Web Development) ]

Authors: Matthew Etchells (260680753), Adam Gilker (260676031), Chen Yue (260909729)

The only dependencies for the project are the python modules:

    django 
    channels 
    channels-redis 
    six

To run the project, enter the vodchatserver directory, then run:

    python3 manage.py makemigrations
    python3 manage.py migrate

Which will initialize the database with the appropriate tables, and create a new file called db.sqlite3. Then run:

    python3 manage.py runserver

An instance of redis must be running for the websocket functionality. 

    redis-server

    OR

    docker run -d -p 6379:6379 redis

Visit localhost:8000 in the browser to check that the server is running.