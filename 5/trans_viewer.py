# -*- coding: utf-8 -*- 

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from util import deployed_on_sae
from private_const import app_secret_key

from sae.const import MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB

if deployed_on_sae:
	import sae.storage

app = Flask(__name__)

app.debug = True
app.secret_key = app_secret_key

app.config['SQLALCHEMY_ECHO'] = False
if deployed_on_sae:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER,MYSQL_PASS,MYSQL_HOST,MYSQL_PORT,MYSQL_DB)
	class nullpool_SQLAlchemy(SQLAlchemy):
		def apply_driver_hacks(self, app, info, options):
			super(nullpool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
			from sqlalchemy.pool import NullPool
			options['poolclass'] = NullPool
			del options['pool_size']
	db = nullpool_SQLAlchemy(app)
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////./test.db'
	db = SQLAlchemy(app)

class Episode(db.Model):
	__tablename__ = 'episode'
	id = db.Column(db.Integer, primary_key=True)
	season = db.Column(db.Integer, nullable=False)
	episode = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(80), nullable=False)
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

class Scene(db.Model):
	__tablename__ = 'scene'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
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


class Speech(db.Model):
	__tablename__ = 'speech'
	id = db.Column(db.Integer, primary_key=True)
	figure = db.Column(db.String(40), nullable=False)
	content = db.Column(db.String(512), nullable=False)
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

#db.drop_all()
db.create_all()

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/episode/<int:season>/<int:episode>')
def get_episode(season, episode):
	return render_template('episode.html', season=season, episode=episode)

from trans_parser import parse_trans
@app.route('/trans/<int:season>/<int:episode>')
def get_trans(season, episode):
	ep = Episode.query.filter_by(season=season, episode=episode).first()
	if ep:
		data = {'status': 'success', 'trans': ep.to_json()}
	else:
		data = {'status': 'error'}
	resp = jsonify(data)
	resp.status_code = 200
	return resp

@app.route('/addtrans/<int:season>/<int:episode>')
def add_trans_to_db(season, episode):
	if deployed_on_sae:
		s = sae.storage.Client()
		filename = 's%02de%02d' % (season, episode)
		ob = s.get('tbbtsubfile', filename + '.txt')
		lines = ob.data.split('\r\n')
	else:
		filename = 's%02de%02d' % (season, episode)
		f = open('storage/tbbtsubfile/' + filename + '.txt','r')
		lines = f.readlines()
		f.close()
	trans = parse_trans(lines)
	episode = Episode(season=season, episode=episode, title='example')
	episode.scenes = []
	for scene in trans:
		s = Scene(title=scene['scene'])
		s.speeches = []
		for speech in scene['speeches']:
			sp = Speech(figure=speech['figure'], content=speech['content'])
			s.speeches.append(sp)
		episode.scenes.append(s)
	
	if not Episode.query.filter_by(season=season, episode=episode).first() :
		db.session.add(episode)
		db.session.commit()
		return 'ok'
	else: 
		return 'exsit'

if __name__ == '__main__':
    app.run()