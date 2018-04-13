################################################################
### Language and script related data.
################################################################

### character properties

def size_category(c):
    if len(c)>1: raise Exception("isolated characters only")
    if c in "acemnorsuvwxyz": return "x"
    if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZbdfhklt!?": return "k"
    if c in "gpqy": return "y"
    if c in ".,": return "."
    if c in """'"`""": return "'"
    return None

### commonly confused characters in OCR

ocr_confusions_list = [
    ["c","C","e","<"],
    ["l","1","I","|","/","_","i"],
    ["o","O","0","a",""," "],
    ["s","S","5","8","_"],
    ["u","U"],
    ["v","V"],
    ["w","W","v"],
    ["x","X"],
    ["z","Z"],
    ["ë","à","ö",""," "],
    ["e","é","ü","&","Ÿ","c"],
    ["_","i","/",""," ","r","'", "t"],
    ["o","Q","a","d"],
    ["‹","ô"],
    ["e","è","Ÿ","_","†"],
    ["__","-"],
    ["ç","g"],
    ["f","t"],
    ["l","/","i"],
    ["7","T"],
    ["N","M"],
    ["ù","à"],
    ["E","É"],
    ["D","O"],
    ["n","m"],
    ["0","o"],
    [",","'",".","`"],
]

ocr_confusions = {}

for e in ocr_confusions_list:
    for i in range(len(e)):
        ocr_confusions[e[i]] = e

