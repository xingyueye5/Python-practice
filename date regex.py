import pyperclip,re
text=input()
date=re.compile(r'''(
([0,1,2][1-9]|10|20|30|31|[1-9])  ##date
/
(0[1-9]|10|11|12|[1-9])           #month
/
([1,2]\d{3})                ##year
)''',re.VERBOSE)
mod=date.findall(text)
if len(mod)==0:
    print('Invalid date')
else:
    print('Valid')
    for group in mod:
        if len(group[1])==1:
            print('date: ','0'+group[1])
        else: print('date: ',group[1])
        if len(group[2])==1:
            print('date: ','0'+group[2])
        else: print('date: ',group[2])
        print('year: ',group[3])


