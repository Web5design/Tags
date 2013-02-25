"wrapper around openmeta CLI"

import subprocess
import shlex
from config import openmeta_path


def add_tags(paths, tags):
    """
    paths can be collection of paths or tab separated string,
    tags can be collection or space separated string, with
    double quotes for mutliple words
    """
    if not isinstance(tags, str):
        tags = ' '.join(tags)
    if isinstance(paths, str):
        paths = paths.split('\t')
    for path in paths:
        subprocess.call(
            openmeta_path + ' -a {1} -p "{0}"'.format(path, tags),
            shell=True
        )


def get_tags(path):
    om_output = subprocess.check_output(
        openmeta_path + ' -p "{0}"'.format(path),
        shell=True
    )
    # extract tags from output
    om_tag_line = om_output.split('\n')[1]
    tags = set(shlex.split(om_tag_line[6:]))
    return tags


def remove_tags(paths, tags):
    """
    paths can be collection of paths or tab separated string
    tags can be collection or space separated string, with
    double quotes for mutliple words
    """
    if isinstance(paths, str):
        paths = paths.split('\t')

    for path in paths:
        # appears that openmeta CLI only allows to remove all tags
        # so first do that and then readd remaining tags
        original_tags = get_tags(path)
        clear_tags(path)
        if isinstance(tags, str):
            tags = shlex.split(tags)
        remaining_tags = original_tags - set(tags)
        add_tags(path, remaining_tags)


def clear_tags(paths):
    """
    remove all tags
    paths can be collection of paths or tab separated string
    """
    if isinstance(paths, str):
        paths = paths.split('\t')
    for path in paths:
        subprocess.call(
            openmeta_path + ' -s -p "{0}"'.format(path),
            shell=True
        )


def tags_to_str(paths, include_paths=True):
    """
    returns string representing tags of files
    paths shows only top directory and filename and are comma separated
    paths can be collection of paths or tab separated string
    """

    if isinstance(paths, str):
        paths = paths.split('\t')
    tags = set()
    for path in paths:
        tags |= get_tags(path)

    prefix = ''
    if include_paths:
        prefix = ", ".join(
            # include containig folder for better granularity
            ['/'.join(path.split('/')[-2:]) for path in paths]
        ) + ': '
    return prefix + (" ".join(tags) if tags else '-no tags-')
