import json
import os
from dbutil import *

def info_to_db(db, name):
    cur = db.cursor()
    with open(name) as data_file:
        data = json.load(data_file)
        subject = data['subject']
        code = data['code']
        title = data['title']
        credit = data['credit']
        desc = data['desc']
        geneds = data['geneds']
        if geneds is None:
            geneds = ''
        else:
            geneds = ','.join(geneds) 
        url = data['url']
        cmd = 'INSERT INTO `CourseExplorer` (`Id`, `Subject`, `Code`, `Title`, `Credit`, `Description`, `GenEd`, ' \
              '`Url`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s) '
        val = (subject, code, title, credit, desc, geneds, url)
        cur.execute(cmd, val)
        # if subject == 'PHYS':
        #     print cmd % val

if __name__ == '__main__':
    # Testing connection
    db = connect()
    for root, dirs, files in os.walk('out/'):
        for name in files:
            try:
                info_to_db(db, 'out/' + name)
                log('C', 'db', 'Successfully written %s' % name)
            except:
                log('E', 'db', 'Fail to insert %s' % name)
    # Testing disconnection
    disconnect(db)
