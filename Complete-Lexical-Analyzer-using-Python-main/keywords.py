keyword = ['and', 'as', 'assert', 'break', 'class', 'def', 'del',
'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global','if', 'import',
'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'with', 'yield']

def is_keyword(a , cnt):
    if a in keyword:
        print('<KEYWORD , "%s" , "%s">' % (a , cnt))
    return a in keyword
