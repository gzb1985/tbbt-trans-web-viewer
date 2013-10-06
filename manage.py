#!/usr/bin/env python
#coding=utf-8

import uuid

from flask import Flask, current_app
from flask.ext.script import Server, Shell, Manager, Command, prompt_bool

from transviewer import create_app
from transviewer.extensions import db
from transviewer.models import Episode, Scene, Speech
from scripts import parse_trans

#manager = Manager(create_app(config_obj='transviewer.config.DevelopmentConfig'))
manager = Manager(create_app(config_obj='transviewer.config.ProductionConfig'))
manager.add_command("runserver", Server('0.0.0.0',port=5000))

def _make_context():
    return dict(db=db)
manager.add_command("shell", Shell(make_context=_make_context))

@manager.command
def createall():
    "Creates database tables"
    db.create_all()

import codecs
def populate_tbbt(sn, ep):
    if Episode.query.filter_by(season=sn, episode=ep).first():
        return;
    filename = 's%02de%02d' % (sn, ep)
    print filename
    filename = 'transcripts/tbbt/' + filename + '.txt'
    f = codecs.open(filename, 'r', 'utf-8')
    lines = f.readlines()
    f.close()
    trans = parse_trans(lines)
    episode = Episode(season=sn, episode=ep, title='example')
    episode.scenes = []
    for scene in trans:
        s = Scene(title=scene['scene'])
        s.speeches = []
        for speech in scene['speeches']:
            sp = Speech(figure=speech['figure'], content=speech['content'])
            s.speeches.append(sp)
        episode.scenes.append(s)

    db.session.add(episode)
    db.session.commit()


def db_populate():
    tbbt_ep_nums = [17, 23, 23, 24, 24, 24]
    for s, ep_num in enumerate(tbbt_ep_nums):
        for ep in range(1,ep_num+1):
            populate_tbbt(s+1, ep)

@manager.command
def populate():
    "Populate database"
    db.create_all()
    db_populate()

@manager.command
def dropall():
    "Drops all database tables"
    
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

from scripts import crawl_tbbt
@manager.command
def crawler():
    "get new transcripts"
    db.create_all()
    new_ep = crawl_tbbt()
    if new_ep:
        for ep in new_ep:
            populate_tbbt(ep[0], ep[1])


if __name__ == "__main__":
    manager.run()
