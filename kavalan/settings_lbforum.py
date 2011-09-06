#Settings for LBForum
from kavalan.settings import *
import os

INSTALLED_APPS += (
    'pagination',
    'lbforum',
    'djangohelper',
    'onlineuser',
    'attachments')

TEMPLATE_CONTEXT_PROCESSORS += ('djangohelper.context_processors.ctx_config',)
MIDDLEWARE_CLASSES += (
    'pagination.middleware.PaginationMiddleware',
    'onlineuser.middleware.OnlineUserMiddleware')

CTX_CONFIG = {
        'LBFORUM_TITLE': 'Kavalan Forum',
        'LBFORUM_SUB_TITLE': 'Kavalan System Forum based on LBForum',
        'FORUM_PAGE_SIZE': 50,
        'TOPIC_PAGE_SIZE': 20,

        'LOGIN_URL': LOGIN_URL,
        'LOGOUT_URL': LOGOUT_URL,
        'REGISTER_URL':'',
        }

BBCODE_AUTO_URLS = True
#add allow tags
HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
#add forbid tags
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []

"""
#default html safe settings
acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
    'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
    'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
    'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
    'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
    'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
    'thead', 'tr', 'tt', 'u', 'ul', 'var']
acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
    'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
    'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
    'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
    'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
    'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
    'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
    'usemap', 'valign', 'value', 'vspace', 'width', 'style']
"""

#always show topic post in topic page.
LBF_STICKY_TOPIC_POST = True
#show last topic in index page
LBF_LAST_TOPIC_NO_INDEX = True

#add v2ex template dir to TEMPLATE_DIRS
import lbforum
V2EX_TEMPLATE_DIR = os.path.join(lbforum.__path__[0], 'templates_v2ex')
TEMPLATE_DIRS += (
        V2EX_TEMPLATE_DIR,
)
