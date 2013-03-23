#!/usr/bin/env python
#coding=utf-8

import transviewer
from transviewer.extensions import db

class Speech(db.Model):
    __tablename__ = 'speech'
    id = db.Column(db.Integer, primary_key=True)
    figure = db.Column(db.String(40), nullable=False)
    content = db.Column(db.String(4096), nullable=False)
    scene_id = db.Column(db.Integer, db.ForeignKey('scene.id'))


    def _init__(self, figure, content):
        self.figure = figure
        self.content = content

    def __repr__(self):
        return '<Speech by %r>' % self.figure

    def to_json(self):
        speech = {}
        speech['figure'] = self.figure
        speech['content'] = self.content
        return speech
