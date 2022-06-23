import re
from punct import is_punc,puncList
from keywords import is_keyword
from ID import is_ID

Data_type = ['int', 'float', 'str', 'char', 'long', 'double', 'decimal']
file_name1 = input("Enter File Name: ")
file_name = "C:\\Users\Programmer\Documents\Pyproj\CC_Project(Lexical_Analyzer)\\" + file_name1 + ".txt"

try:
    fin = open(file_name)
except:
    print("Input file '%s' does not exists:"% file_name1)
    quit(0)


lines = fin.readlines()
if len(lines) <= 0:
    print("Input file '%s' is empty"% file_name1)
    quit(0)


def breakup_line(line):
    words = line.split()
    newwords = []
    for i in range(len(words)):
        if words[i][0] in ("'",'"') and words[i][-1] in ("'",'"'):
            newwords.append(words[i])
        else:
            t = re.findall(r"[\w]+|[^\s\w]|[-:\w]", words[i])
            newwords.extend(t)
    return newwords

def get_strings(words):
    new_words = []
    adding = False
    tmpstring = ''
    skip = False
    for w in words:
        if ('"' in w or "'" in w) and (w.count('"') < 2 and w.count("'") < 2):
            adding = not adding
        if not adding:
            new_words.append(tmpstring+w)
            tmpstring = ''
            skip = True
        if adding:
            tmpstring += w + ' '
        else:
            if skip:
                skip = False
            else:
                new_words.append(w)
    return new_words


skip = False
cnt = 0
print("<Category , Words , Inner Code>")
for line in lines:
    if '#' in line:
        line = line[:line.index('#')]
    tokens = breakup_line(line)
    final = get_strings(tokens)

    for c, item in enumerate(final):
        cnt += 1
        # print cnt
        if not skip:
            if is_punc(item):
                try:
                    if is_punc(item + final[c+1]):
                        print('<PUNC , "%s" , "%s">' % (str(item + final[c+1]) , cnt))
                        skip = True
                    else:
                        print('<PUNC , "%s" , "%s">' % (item , cnt))
                except:
                    print('<PUNC , "%s" , "%s">' % (item , cnt))
            elif is_keyword(item , cnt):
                pass
            elif(item in Data_type):
                print('<Dtype , "%s" , "%s">' % (item, cnt))
                pass
            elif is_ID(item , cnt):
                pass
            else:
                print('<Non_Lexeme , "%s" , "%s">' % (item , cnt))
        else:
            skip = False
print("<END OF FILE>")
