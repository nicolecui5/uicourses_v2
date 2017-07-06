# UICourses v2

## Database -> JSON API
### Scripts
- `server.py`: a simple TCP server that acts as an API that pulls data from the database and parse them into json format.
- `dbutil.py`: database lookup functions used by `server.py`
- `options.py`: database options used in `dbutil.py`. Mostly hardcoded column names.
- `util.py`: general utilities (logging, etc)
- `credentials.py`: not to be committed. The format is shown in `credentials.py.format` - one has to rename it to `credentials.py` and fill in the credential strings.

### Usage
To start the server, run
```
./server.py <port>
```

Just shoot a GET request in the following format:
```
http://<domain>:<port>/dbapi?subject=<subject>&code=<course_code>&[suffix=<suffix>]&key=<api_key>
```
such as
```
http://uicourses.com:7000/dbapi?subject=cs&code=374&key=mykey
```

## GUI to insert to database
### Scripts
- `post_api`

### HTML pages
- [Forms](https://github.com/sumerinlan/uicourses_v2/tree/master/HTML%20%E8%A1%A8%E6%A0%BC)

### Usage guide
- [Wiki](https://github.com/sumerinlan/uicourses_v2/wiki/数据的填写与录入)
- [Link to forms](http://uicourses.com/forms)

## Copyright
### Coauthored by:
- Liu, Fangxing
- Sun, Hanze
- Wang, Sibo
- Wen, Xin
- Wu, Xintong
- Yao, Ruiqian
- Zhi, Qile.

Copyright owned by coauthors. All rights reserved.
