Video On Demand Chat [ Project for COMP 307 (Web Development) ]

To run the project, enter the vodchat directory, then run:

    python3 manage.py migrate

Which will initialize the database with the appropriate tables, and create a new file called db.sqlite3. Then run:

    python3 manage.py runserver

To run a development server. By default, the server will run on port 8000. Visit localhost:8000 in the browser to check that the server is running.

VueJS is being used only at the videos/watch page for now as the others are simpler pages for now.

Note: Django-channels requires a redis instance to be running for it to work properly. It is being used for getting notifications of new comments at videos/watch. You can run redis through a docker container or just using the redis-server command line tool.
