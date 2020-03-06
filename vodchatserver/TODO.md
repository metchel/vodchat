DONE

- can view a list of the videos in the database by going to localhost:8000/videos
- can upload a video by going to localhost:8000/videos/upload
- can view a video by going to localhost:8000/videos/watch?<video-id>

TODO

- authentication/authorization of users
- attach videos to user accounts
- create Comments model (with foreign key to a video id)
- allow uploading of video thumbnails
- set up websocket communication using Django Channels
    -> i.e., for sending push notifications to client browsers when a new comment is posted to a video being watched
- improve frontend
    -> consider using a front end framework instead of Django templates [ VueJs can be used as a lightweight framework ]
    -> consider using Material Design or other for components with nice user interfaces
- Other stuff
