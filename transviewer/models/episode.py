#!/usr/bin/env python
#coding=utf-8

import transviewer
from transviewer.extensions import db

class Episode(db.Model):
	__tablename__ = 'episode'
	id = db.Column(db.Integer, primary_key=True)
	season = db.Column(db.Integer, nullable=False)
	episode = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(512), nullable=False)
	scenes = db.relationship('Scene', backref='episode', lazy='dynamic')

	def _init__(self, season, episode, title):
		self.season = season
		self.episode = episode
		self.title = title

	def __repr__(self):
		return '<Episode %r>' % self.title

	def to_json(self):
		episode = {}
		episode['season'] = self.season
		episode['episode'] = self.episode
		episode['title'] = self.title
		episode['scenes'] = [scene.to_json() for scene in self.scenes ]
		return episode

