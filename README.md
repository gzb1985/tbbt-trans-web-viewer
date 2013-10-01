# The Big Bang Theory Transcript Viewer

## Features

* A different way to re-watch your favoiter tbbt episode
* Displaying transcript in the colorful speech bubbles

##Install

### Clone the code

    git clone https://github.com/gzb1985/tbbt-trans-web-viewer.git
    cd tbbt-trans-web-viewer

### Virtualenv

    pip install virtualenv
    virtualenv venv --distribute
    source venv/bin/activate
    pip install -r requirements.txt

### Populate database

    python manage.py createall
    python manage.py populate

### Local run

    python manage.py runserver

###Custom the Configuration

    transviewer/config.py

### Gunicorn run

    gunicorn -w 4 -b 127.0.0.1:8000 app:app

## Acknowledgments

* All Transcripts come from [Big Bang Theory Transcripts blog](http://bigbangtrans.wordpress.com) by Ash
* Inspired by The [Big Bang Transcripts Viewer](http://www.codeproject.com/Articles/306758/The-Big-Bang-Transcripts-Viewer) (A WP7 app developed by Marcelo Ricardo de Oliveira)

##Screenshot

![Season 6 Episode 1](http://tbbtsubs-img.stor.sinaapp.com/demo_screenshot.png)






