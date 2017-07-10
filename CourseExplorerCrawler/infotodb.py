f = open('run00.out', 'r')

while True:
    line = f.readline()
    if line == '':
        break
    if line[0:2] == "~~":  # start a new course
        start = 1
        subject = f.readline().strip()
        # print "subject", subject
        code = f.readline().strip()
        # print "code", code
        title = f.readline().strip()
        hour = f.readline().strip()
        # print "hour", hour
        desc = ""
        line = f.readline().strip()
        while line[0:3] == "<p>":
            desc += line
            line = f.readline().strip()
        # print "desc", desc
        gened = line
        if gened != "None":
            gened == f.readline().strip()  # make sure line == list of gened
        url = f.readline().strip()
        # print "gened", gened
        cmd = 'INSERT INTO `CourseExplorer` (`Id`, `Subject`, `Code`, `Title`, `Credit`, `Description`, `GenEd`, ' \
              '`Url`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s) '
        print cmd % (subject, code, title, hour, desc, gened, url)
