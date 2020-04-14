# Youtube-Search-and-Player
Custom Youtube search and videoplayer made entirely on Python Web Framework Django. Templates made by using Bootstrap 4.

## How it works

1. It shows top 12 youtube video result of your search. 

2. On clicking at any video, it opens a new page containing the embedded video and a button to redirect to youtube page of the same video.

##### Features:

Shows title, total no. of views, thumbnail and the video uploaded date.

## How to Use

### Initialize the project

##### Create and activate a virtualenv:

1. `virtualenv venv`. This will a create a vitual environment called "venv" that helps with controlling dependencies.
2. `source venv/bin/activate`. 


##### Install dependencies:

(while in the activated virtual environment)
```bash
pip install -r requirements.txt
```
NOTE: After installing dependencies, pip-tools is also installed. You can now use it to manage package dependencies of your project.

Add a new package to requirements.in and run the following command to auto-update requirements.txt file
```bash
pip-compile requirements.in
```

Run the following command to sync your virtualenv
```bash
pip-sync`
```

##### Run the server:
```bash
python manage.py runserver
```
