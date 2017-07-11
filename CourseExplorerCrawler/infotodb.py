import json
import os
import dbutil

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
        url = data['url']
        cmd = 'INSERT INTO `CourseExplorer` (`Id`, `Subject`, `Code`, `Title`, `Credit`, `Description`, `GenEd`, ' \
              '`Url`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s) '
        cur.execute(cmd, [subject, code, title, credit, desc, geneds, url])

if __name__ == '__main__':
    # Testing connection
    db = dbutil.connect()
    for root, dirs, files in os.walk('out/'):
        if root == '':
            for name in files:
                info_to_db(db, 'out/' + name)
    # Testing disconnection
    dbutil.disconnect(db)