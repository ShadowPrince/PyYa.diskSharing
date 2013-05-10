PyYa.diskSharing
================
Python utilite using httplib to share files throught yandex.disk connected via webdav.

Installing
==========
* install _davfs2_ package
* Go to https://oauth.yandex.ru/authorize?response_type=code&client_id=fffac380405a4fedbba9a0b7b48d8aab
* Allow, click "Get token", copy "access_token" md5.
* Put token in "yadisk" script file and uncomment line
* Move or ln it to the /usr/bin dir, make executable

Usage
=====
* yadisk --help
* yadisk FILE - share FILE and copy shortlink to the clipboard via xclip
* yadisk u FILE - make FILE private
