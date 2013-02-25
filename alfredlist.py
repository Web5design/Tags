from cgi import escape
from uuid import uuid1
from config import pickle_newline_substitution
import pickle


class AlfredItemsList(object):
    def __init__(self, items=None):
        self.items = items or []
        self.pattern = \
            '<item arg="{arg}" uid="{uid}" valid="{valid}">"' + \
            '<title>{title}</title>' + \
            '<subtitle>{subtitle}</subtitle>' + \
            '{icon}' + \
            '</item>'

    def append(
            self,
            arg,
            title,
            subtitle,
            valid='yes',
            icon='iconw',
            uid=None
        ):
        """Use uid = None to preserve order of items"""
        uid = uid or str(uuid1())
        # using uuid is little hacky, there is no other way to
        # prevent alfred from reordering items
        self.items.append(
            (pickle.dumps(arg).replace('\n', pickle_newline_substitution), escape(title), escape(subtitle), valid, icon, uid)
            )

    def __str__(self):
        items = "".join(
            [self.pattern.format(
                arg=arg,
                title=escape(title),
                subtitle=escape(subtitle),
                valid=valid,
                icon=icon,
                uid=uid
                ) for arg, title, subtitle, valid, icon, uid in self.items]
            )
        return '<items>' + items + '</items>'

    def __add__(self, other):
        return AlfredItemsList(self.items + other.items)
