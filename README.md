PyYa.diskSharing
================
Python utilite using httplib to share files throught yandex.disk connected via webdav.

= Installing =
1. You must connect yandex.disk through WebDav and install xclip:

* install _davfs2_ package
* ```mkdir yadisk```
* ```mount -t webdav https://webdav.yandex.ru yadisk```
* install _xclip_ package

2. You must get private OAuth token for application:

* Go to https://oauth.yandex.ru/authorize?response_type=code&client_id=fffac380405a4fedbba9a0b7b48d8aab
* Allow, click "Get token", copy "access_token" md5.
* Put token in "yadisk" script file and uncomment line
* Move or ln it to the /usr/bin dir, make executable

= Usage =

* yadisk FILE - share FILE and copy shortlink to the clipboard via xclip
* yadisk FILE u - make FILE private
* yadisk [PATH] status - check is dir under yadi.sk

