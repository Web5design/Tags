import pickle
import fileslist
import openmeta
from config import pickle_newline_substitution

paths = fileslist.to_list()


def dispatch(query, modifier=None):
    query = query.replace(pickle_newline_substitution, '\n')

    tags, arg = pickle.loads(query)
    if arg == '--add':
        if modifier:
            return
        openmeta.add_tags(paths, tags)
    elif arg == '--rem':
        if modifier:
            return
        openmeta.remove_tags(paths, tags)
    elif arg == '--clear tags':
        if modifier:
            return
        openmeta.clear_tags(paths)
    elif arg == '--clear selection':
        if modifier:
            return
        fileslist.clear()
    else:
        if modifier == 'alt':
            openmeta.remove_tags(arg, tags)
        elif modifier == 'fn':
            fileslist.remove(arg)
        else:
            openmeta.add_tags(arg, tags)
