#!/usr/bin/env python
#coding=utf-8

import transviewer
from transviewer.extensions import db

class Scene(db.Model):
    __tablename__ = 'scene'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))
    speeches = db.relationship('Speech', backref='scene', lazy='dynamic')

    def _init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Scene %r>' % self.title

    def to_json(self):
        scene = {}
        scene['scene'] = self.title
        scene['speeches'] = [speech.to_json() for speech in self.speeches ]
        return scene
