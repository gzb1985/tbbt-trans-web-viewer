# The Big Bang Theory Transcript Viewer

## Features

* A different way to re-watch your favoiter tbbt episode
* Displaying transcript in the colorful speech bubbles

##Install

###Prerequisite

    pip install -r requirements.txt

###Custom the Configuration
    
    transviewer/config.py

###Sync database

    python manage.py createall

###Db populate

    python manage.py populate

###Local run

    python manage.py runserver

###Heroku run

see the scripts in `Procfile`

    web: gunicorn -w 4 -b 0.0.0.0:$PORT -k gevent app:app

## Acknowledgments

* All Transcripts come from [Big Bang Theory Transcripts blog](http://bigbangtrans.wordpress.com) by Ash
* Inspired by The [Big Bang Transcripts Viewer](http://www.codeproject.com/Articles/306758/The-Big-Bang-Transcripts-Viewer) (A WP7 app developed by Marcelo Ricardo de Oliveira)

##Website

Now, the code deployed on Heroku instead SinaAppEngine (SAE). A few modifications should be made if you want to run it on SAE.

[The new website on Heroku](http://tbbttrans.herokuapp.com/)

[The old website](http://tbbtsubs.sinaapp.com/). 

##Screenshot

![Season 6 Episode 1](http://tbbtsubs-img.stor.sinaapp.com/demo_screenshot.png)






