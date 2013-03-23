#! /usr/bin/env python
#coding=utf-8

import datetime
import os

from flask import Module, Response, request, flash, jsonify, g, current_app,\
    abort, redirect, url_for, session
from flask import render_template

import transviewer
from transviewer.extensions import db
from transviewer.models import Episode, Scene, Speech

frontend = Module(__name__)

MAX_SEASON = 6

@frontend.route('/')
def index():
    episodes = []
    for i in range(1,MAX_SEASON+1):
        e = Episode.query.filter_by(season=i).count()
        episodes.append(e)
    return render_template('index.html', episodes = episodes)

@frontend.route('/episode/<int:season>/<int:episode>')
def get_episode(season, episode):
    return render_template('episode.html', season=season, episode=episode)

@frontend.route('/trans/<int:season>/<int:episode>')
def get_trans(season, episode):
    ep = Episode.query.filter_by(season=season, episode=episode).first()
    if ep:
        data = {'status': 'success', 'trans': ep.to_json()}
    else:
        data = {'status': 'error'}
    resp = jsonify(data)
    resp.status_code = 200
    return resp
