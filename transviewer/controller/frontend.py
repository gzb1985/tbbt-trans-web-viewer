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

MAX_SEASON = 10

@frontend.route('/')
def index():
    episodes = []
    si = 1
    while si <= MAX_SEASON:
        ep_num = Episode.query.filter_by(season=si).count()
        if ep_num != 0:
            episodes.append(ep_num)
        si = si + 1
    return render_template('index.html', episodes = episodes)

@frontend.route('/comments')
def comments():
    return render_template('comments.html')

@frontend.route('/episode/<int:season>/<int:episode>')
def get_episode(season, episode):
    ep = Episode.query.filter_by(season=season, episode=episode).first()
    return render_template('episode.html', season=season, episode=episode, title=ep.title)

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
