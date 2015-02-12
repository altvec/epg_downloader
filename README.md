# Simple EPG downloader

EPG files are downloaded from s-tv.ru service. Username and Password are stored
in the settings.conf file.

The file must contain following:
```
[Main]
username = %your_user_name%
password = %your_password%
```

Internally this program uses curl, so be sure that it is installed in your
system.
