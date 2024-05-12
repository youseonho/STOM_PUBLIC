from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def color_format(color, style=''):
    _format = QTextCharFormat()
    _format.setForeground(color)
    if 'bold' in style:   _format.setFontWeight(QFont.Bold)
    if 'italic' in style: _format.setFontItalic(True)
    return _format


STYLES = {
    'keyword':  color_format(QColor(255, 100,   0)),
    'operator': color_format(QColor(230, 230,  50)),
    'brace':    color_format(QColor(230, 230, 240)),
    'defclass': color_format(QColor(230, 100,    0), 'bold'),
    'string':   color_format(QColor(100, 230, 100)),
    'string2':  color_format(QColor(100, 230, 100)),
    'string3':  color_format(QColor(100, 230, 100)),
    'comment':  color_format(QColor(100, 230, 100), 'italic'),
    'self':     color_format(QColor(230,  50, 230)),
    'numbers':  color_format(QColor( 50, 230, 230)),
    'type':     color_format(QColor(100, 100, 230))
}


class PythonHighlighter(QSyntaxHighlighter):
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass',
        'raise', 'return', 'try', 'while', 'yield', 'None', 'True', 'False'
    ]
    types = [
        'int', 'float', 'round', 'str', 'boolean', 'datetime', 'print'
    ]
    operators = [
        '=', '==', '!=', '<', '<=', '>', '>=', '\+', '-', '\*', '/', '//', '\%', '\*\*',
        '\+=', '-=', '\*=', '/=', '\%=', '\^', '\|', '\&', '\~', '>>', '<<'
    ]
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]'
    ]
    string3 = [
        '"""'
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        rules = []
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in PythonHighlighter.keywords]
        rules += [(r'\b%s\b' % t, 0, STYLES['type']) for t in PythonHighlighter.types]
        rules += [(r'%s' % o, 0, STYLES['operator']) for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in PythonHighlighter.braces]
        rules += [(r'%s' % s, 0, STYLES['string3']) for s in PythonHighlighter.string3]
        rules += [
            (r'\bself\b', 0, STYLES['self']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),
            (r'#[^\n]*', 0, STYLES['comment']),
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers'])
        ]
        self.rules = [(QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, format_ in self.rules:
            index = expression.indexIn(text)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format_)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

    def match_multiline(self, text, delimiter, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()

        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)

        if self.currentBlockState() == in_state:
            return True
        else:
            return False
