# -*- coding: utf-8 -*- 

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from flask import jsonify

from util import deployed_on_sae
from private_const import app_secret_key

if deployed_on_sae:
	import sae.storage

app = Flask(__name__)

app.debug = True
app.secret_key = app_secret_key

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/episode/<int:season>/<int:episode>')
def get_episode(season, episode):
	return render_template('episode.html', season=season, episode=episode)

from trans_parser import parse_trans
@app.route('/trans/<int:season>/<int:episode>')
def get_trans(season, episode):
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
	data = {'status': 'success', 'trans': parse_trans(lines)}
	resp = jsonify(data)
	resp.status_code = 200
	return resp


if __name__ == '__main__':
    app.run()