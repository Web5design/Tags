"""
module provides functions to store and retrieve paths of
files selected to tagging

paths are stored as tab-separated list in file in
'~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data/OpenmetaTags/selection
"""

from openmeta import tags_to_str
from alfredlist import AlfredItemsList
import os

dir_path = os.path.expanduser('~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data/OpenmetaTags/')
# create directory if it doesn't exist
if not os.path.isdir(dir_path):
    os.mkdir(dir_path)
full_path = dir_path + 'selection'

# create selection file if it doesn't exist
try:
    open(full_path, 'r')
except IOError:
    open(full_path, 'w').close()


def change_list(items, change_f):
    # load items from file
    previous = set()
    with open(full_path, 'r') as f:
        text = f.read()
        if text:
            previous = set(text.split('\t'))

    # change items from file using change_f and items
    if isinstance(items, str):
        items = set(items.split('\t'))
    new = change_f(previous, items)
    with open(full_path, 'w') as f:
        f.write('\t'.join(new))


def add(items):
    change_list(items, lambda p, i: p.union(i))


def remove(items):
    change_list(items, lambda p, i: p - set(i))


def clear():
    with open(full_path, 'w') as f:
        f.write('')


def to_alfred_xml(arg):
    items = set()
    with open(full_path, 'r') as f:
        text = f.read()
        if text:
            items = set(text.split('\t'))
    al = AlfredItemsList()
    for item in items:
        al.append(
            arg=arg,
            title=item,
            subtitle=tags_to_str(item, False),
            icon=item)
    return al


def to_list():
    with open(full_path, 'r') as f:
        return f.read().split('\t')
