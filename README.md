weixin2weibo
============

SAE上搭建，自动接收微信消息，并发送到指定微博。（适合搭建树洞这种东西）

首次使用需填写代码里微信的token,微博的appkey,appsecret,redirect_url等信息。

然后通过getAccessToken.py获得access_token 和 expires_in，填入index.wsgi中。

这也是一大缺点：

若你的微博应用未通过审核，需要每24小时运行一次getAccessToken.py，

并把获得的expires_in替换掉原来的expires_in，否则24小时后将不能发送微博。

weibo.py 可以在这里下载 http://michaelliao.github.com/sinaweibopy/

SAE 上需要的其他文件比如config.yaml,或者微信验证的问题，这里就不涉及了。
