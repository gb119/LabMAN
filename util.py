"""LabMAN.util - collection of utility functions for the LabMAN code base."""
from django.conf import settings
from importlib import import_module
from django.db import models
import bleach

_safe_attrs={
    'a':['class', 'dir', 'id', 'lang', 'name', 'rel', 'rev', 'style', 'target = _blank', 'title', 'xml:lang', 'accesskey', 'tabindex', 'charset', 'coords', 'href', 'hreflang', 'name', 'shape'],
    'abbr':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'acronym':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'address':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'b':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'big':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'blockquote':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'br':['id', 'class', 'title', 'style', 'clear'],
    'caption':['id', 'lang', 'dir', 'title', 'style'],
    'cite':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'code':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'col':['span', 'width', 'id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'char', 'charoff', 'valign'],
    'colgroup':['span', 'width', 'id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'char', 'charoff', 'valign'],
    'dd':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'del':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'dfn':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'dir':['id', 'class', 'dir', 'title', 'style', 'compact'],
    'div':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'dl':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'dt':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'em':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'h1':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'h2':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'h3':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'h4':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'h5':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'h6':['id', 'class', 'lang', 'dir', 'title', 'style', 'align'],
    'hr':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'i':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'img':['src', 'alt', 'longdesc', 'name', 'id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'width', 'height', 'border', 'hspace', 'vspace'],
    'ins':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'kbd':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'li':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'menu':['id', 'class', 'lang', 'dir', 'title', 'style', 'compact'],
    'ol':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'p':['id', 'class', 'lang', 'dir', 'title', 'stye', 'align'],
    'pre':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'q':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'samp':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'small':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'span':['id', 'class', 'dir', 'title', 'style', 'align', 'xml:lang'],
    'strong':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'sub':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'sup':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'table':['id', 'border', 'cellpadding', 'cellspacing', 'align', 'class', 'frame', 'summary', 'lang', 'dir', 'style', 'bgcolor', 'width', 'rules', 'dir'],
    'tbody':['id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'char', 'charoff', 'valign'],
    'td':['abbr', 'axis', 'headers', 'scope', 'rowspan', 'colspan', 'id', 'class', 'lang', 'dir', 'title', 'style', 'bgcolor', 'align', 'char', 'charoff', 'valign'],
    'tfoot':['cellhalign', 'cellvalign', 'id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'char', 'charoff', 'valign'],
    'th':['abbr', 'axis', 'headers', 'scope', 'rowspan', 'colspan', 'id', 'class', 'lang', 'dir', 'title', 'style', 'bgcolor', 'align', 'char', 'charoff', 'valign'],
    'thread':['cellhalign', 'cellvalign', 'id', 'class', 'lang', 'dir', 'title', 'style', 'align', 'char', 'charoff', 'valign'],
    'tr':['id', 'class', 'lang', 'dir', 'title', 'style', 'bgcolor', 'align', 'char', 'charoff', 'valign'],
    'tt':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'ul':['id', 'class', 'lang', 'dir', 'title', 'style'],
    'var':['id', 'class', 'lang', 'dir', 'title', 'style']}

_safe_tags=list(_safe_attrs.keys())
_safe_css=['align-content', 'align-items', 'align-self', 'background', 'background-attachment', 'background-clip', 'background-color',
           'background-image', 'background-origin', 'background-position', 'background-repeat', 'background-size', 'border', 'border-bottom',
           'border-bottom-color', 'border-bottom-left-radius', 'border-bottom-right-radius', 'border-bottom-style', 'border-bottom-width',
           'border-collapse', 'border-color', 'border-image', 'border-image-outset', 'border-image-repeat', 'border-image-slice',
           'border-image-source', 'border-image-width', 'border-left', 'border-left-color', 'border-left-style', 'border-left-width',
           'border-radius', 'border-right', 'border-right-color', 'border-right-style', 'border-right-width', 'border-spacing', 'border-style',
           'border-top', 'border-top-color', 'border-top-left-radius', 'border-top-right-radius', 'border-top-style', 'border-top-width',
           'border-width', 'bottom', 'box-shadow', 'box-sizing', 'caption-side', 'clear', 'clip', 'color', 'column-count', 'column-fill',
           'column-gap', 'column-rule', 'column-rule-color', 'column-rule-style', 'column-rule-width', 'column-span', 'column-width',
           'columns', 'direction', 'display', 'empty-cells', 'flex', 'flex-basis', 'flex-direction', 'flex-flow', 'flex-grow', 'flex-shrink',
           'flex-wrap', 'float', 'font', '@font-face', 'font-family', 'font-size', 'font-size-adjust', 'font-stretch', 'font-style',
           'font-variant', 'font-weight', 'height', 'justify-content', 'left', 'letter-spacing', 'line-height', 'list-style', 'list-style-image',
           'list-style-position', 'list-style-type', 'margin', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top', 'max-height',
           'max-width', 'min-height', 'min-width', 'opacity', 'order', 'outline', 'outline-color', 'outline-offset', 'outline-style', 'outline-width',
           'overflow', 'overflow-x', 'overflow-y', 'padding', 'padding-bottom', 'padding-left', 'padding-right', 'padding-top', 'position',
           'quotes', 'resize', 'right', 'tab-size', 'table-layout', 'text-align', 'text-align-last', 'text-decoration', 'text-decoration-color',
           'text-decoration-line', 'text-decoration-style', 'text-indent', 'text-justify', 'text-overflow', 'text-shadow', 'text-transform',
           'top', 'transform', 'transform-origin', 'transform-style', 'transition', 'transition-delay', 'transition-duration', 'transition-property',
           'transition-timing-function', 'unicode-bidi', 'vertical-align', 'visibility', 'white-space', 'width', 'word-break', 'word-spacing',
           'word-wrap', 'z-index', '']

def clean_html(content):
    """Return content cleaned up of bad tags and styles."""
    return bleach.clean(content,tags=_safe_tags,attributes=_safe_attrs,styles=_safe_css,strip=True,strip_comments=False)

def LabMAN_select_objects(key="link"):
    """Read the LabMAN config for objects that match types of generic relations for select lists.

    key (str): one of "link", "book", "users"
    """
    limit=None
    if key in ["link","book","users"]:
        for app in settings.LABMAN_APPS:
            for model in settings.LABMAN_APPS[app]:
                if key not in model or not model[key]:
                    continue
                if limit is None:
                    limit=models.Q(app_label=app,model=model["name"])
                else:
                    limit=limit | models.Q(app_label=app,model=model["name"])
    return limit
