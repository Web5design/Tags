"wrapper around openmeta CLI"

import subprocess
import shlex
import os

# set your path to openmeta
# if it's in usr/bin no change is required
openmeta_path = 'openmeta'


def add_tags(path, tags):
    if not isinstance(tags, str):
        tags = ' '.join(tags)
    subprocess.call(
        'openmeta -a {1} -p "{0}"'.format(path, tags),
        shell=True
    )


def remove_tags(path, tags=None):
    original_tags = set(tags_to_str(path, include_path=False).split(' '))
    clear_tags(path)
    if tags:
        if isinstance(tags, str):
            tags = shlex.split(tags)
        remaining_tags = original_tags - set(tags)
        add_tags(path, remaining_tags)


def clear_tags(path):
    subprocess.call(
        'openmeta -s -p "{0}"'.format(path),
        shell=True
    )


def tags_to_str(path, include_path=True):
    om_output = subprocess.check_output(
        'openmeta -p "{0}"'.format(path),
        shell=True
    )
    om_tag_line = om_output.split('\n')[1]
    tags = om_tag_line[6:]
    prefix = ''
    if include_path:
        prefix = os.path.split(path)[-1] + ': '
    return prefix + tags
