Video On Demand Chat [ Project for COMP 307 (Web Development) ]

To run the project, enter the vodchat directory, then run:

    python3 manage.py migrate

Which will initialize the database with the appropriate tables, and create a new file called db.sqlite3. Then run:

    python3 manage.py runserver

To run a development server. By default, the server will run on port 8000. Visit localhost:8000 in the browser to check that the server is running.

The following endpoints have been implemented:

    localhost:8000 [ Redirects to /videos ]
    localhost:8000/videos/ [ A list of all the video ids that are in the database ]
    localhost:8000/videos/upload [ Upload a new video ]
    localhost:8000/videos/watch?abc123 [ Watch the video that has the id "abc123" ]
    localhost:8000/videos/comment [ POST makes a new one, GET returns a JSON with all of them for this video_id ]
    localhost:8000/accounts/ [ Create an account ]
    localhost:8000/accounts/login [ Log in ]

This is the css library being used. It seems good enough for our purposes.

    https://www.w3schools.com/w3css/default.asp

VueJS is being used only at the videos/watch page for now as the others are simpler pages for now.

Note: Django-channels requires a redis instance to be running for it to work properly. It is being used for getting notifications of new comments at videos/watch. You can run redis through a docker container or just using the redis-server command line tool.
