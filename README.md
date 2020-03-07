Video On Demand Chat [ Project for COMP 307 (Web Development) ]

To run the project, enter the vodchat directory, then run:

    python3 manage.py migrate

Which will initialize the database with the appropriate tables, and create a new file called db.sqlite3. Then run:
    
    python3 manage.py runserver

To run a development server. By default, the server will run on port 8000. Visit localhost:8000 in the browser to check that the server is running.

The following endpoints have been implemented:

    localhost:8000/videos/ [ A list of all the video ids that are in the database ]
    localhost:8000/videos/upload [ Upload a new video ]
    localhost:8000/videos/watch?abc123 [ Watch the video that has the id "abc123" ]
