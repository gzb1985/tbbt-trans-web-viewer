# -*- coding: utf-8 -*- 

def parse_trans(lines):
	trans = []
	speeches = []
	scene = {}
	for line in lines:
		t = line.split(':')
		if len(t) == 2:
			figure = (t[0].split())[0] #delete additional content, example: Sheldon (larghing)
			content = t[1].strip()
			if figure == r'Scene':
				if speeches: 
					scene['speeches'] = speeches
					trans.append(scene)
					scene = {}
					speeches = []
				scene['scene'] = content.rstrip(r'.')
			else:
				speeches.append({'figure': figure, 'content': content})
	if speeches:
		scene['speeches'] = speeches
		trans.append(scene)

	return trans
