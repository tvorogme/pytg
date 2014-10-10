# -*- coding: utf-8 -*-
from types import ListType, GeneratorType


def coroutine(func):
	"""
	Skips to the first yield when the generator is created.
	Used as decorator, @coroutine
	:param func: function (generator) with yield.
	:return: generator
	"""

	def start(*args, **kwargs):
		cr = func(*args, **kwargs)
		cr.next()
		return cr

	return start


def remove_color(txt):
	"""
	Removes invisible, color defining characters from the cli output. 
	:rtype : str
	:param txt: String maybe containing color codes.
	:return:  Cleaned String.
	"""
	colors = (
		"\033[0;31m", "\033[1;31m", "\033[0m", "\033[32;1m", "\033[37;1m",
		"\033[33;1m", "\033[34;1m", "\033[35;1m", "\033[36;1m", "\033[0;36m",
		"\033[7m", "\033[K"
	)
	for c in colors:
		txt = txt.replace(c, '')
	return txt


def clear_prompt(txt):
	"""
	Removes telegram's leading ">" in front of text input.
	:param txt: String maybe containing telegram's default_prompt.
	:return:  Cleaned String.
	"""
	if len(txt) > 0 and txt[0] == '>':
		return txt[1:].strip()
	return txt


@coroutine
def start_pipeline(target):
	if type(target) is not GeneratorType:
		raise TypeError('target must be GeneratorType')
	try:
		while True:
			item = (yield)
			target.send(item)
	except GeneratorExit:
		pass


@coroutine
def broadcast(targets):
	if type(targets) is not ListType:
		raise TypeError('targets must be ListType')
	for t in targets:
		if type(t) is not GeneratorType:
			raise TypeError('targets item must be GeneratorType')
	try:
		while True:
			item = (yield)
			for target in targets:
				target.send(item)
	except GeneratorExit:
		pass
