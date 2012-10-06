"""Utility function in separate file to prevent cicular imports."""
import pyglet
import os.path

# Joins a list of paths into a single path (OS independent)
list_pj = lambda l: reduce(os.path.join, l) 

# Composition of join and load
load_join_i = lambda l: pyglet.image.load(reduce(os.path.join, l))
load_join_m = lambda l: pyglet.media.load(reduce(os.path.join, l))


