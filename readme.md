#Heroku云部署：将Python web应用部署在heroku中-详细步骤#
前言：本教程基于《Flask web开发：基于python的web应用开发实战》一书、网上部分教程和自己部署经历汇总而来。需要说明的是，《Flask web开发》一书中关于heroku云部署一章有有诸多问题，而且heroku平台也不断更新，导致部署代码有许多不同。以下代码为实际操作，排除多种报错，直至成功部署。

heroku官方部署教程见 [链接](链接 "https://devcenter.heroku.com/articles/getting-started-
with-python#introduction")

个人部署文件GitHub地址 [heroku部署web](heroku部署web "https://github.com/lq-jarhead/heroku")
## 0.部署前介绍 ##
### 1.部署环境 ###
主要软件及版本见下面：

1. os-电脑系统为`Ubuntu-16.04`
2. python- 为系统自带 `python2.7.13`
3. git-在Ubuntu终端中安装 `version 2.7.4`
4. Heroku-在Ubuntu终端中安装 `node-v9.2.0`
6. 说明：
	1. 和web应用相关的模块见requirements.txt需求文件
	2. 在heroku官网上部署说明中，默认要求为py3.6，这里py2.7同样可行

### 2.部署路线 ###
你可能没有仔细看官网全英文介绍，也搞不懂《Flask web开发》部署章节区区几页纸的内容，在你的脑海里，对于部署感到很茫然，为什么是这样部署就可以了呢？以下几点解释能让你更好知道，我们为什么可以这么做！

- 什么是部署？
	- 这个问题比较大，详细的你可以百度一下。在本文档里面，部署的意思就是-将我们的本地web备份到heroku平台，而后在平台上运行，这样其他人就可以访问和使用了。
- 为什么选择Heroku平台？
	- 相比较阿里云等平台，heroku几乎是免费的，再者，Heroku对Python的支持非常良好，让部署过程变得轻松简单起来。
- 简要解释下部署的方法。
	-  1.在终端窗口中，我们安装并登录heroku客户端，创建一个app文件夹和数据库（**注意，客户端的操作实际体现在云端建立文件夹和数据库**）
	-  2.借助git，将本地web应用推送到前面新建的文件夹，这样就可以了！
	-  3.最后一步, 就是执行heroku特有的代码`hero run manage.py deploy`。就这么简单！我们托管给heroku平台，平台执行我们的应用，包括初始化数据库等。执行完毕就可以访问了。

## 1.详细步骤 ##
### 1.浏览器中进入heroku官网[链接](链接 "https://dashboard.heroku.com/")并注册 ###
1. 因为heroku是国外网站，注册的时候没有翻墙的话就会碰到`please confirm you are not a robot` 警告--因为你看不到验证图片。亲测下载个蓝灯，打开蓝灯就能看到验证码这一栏。
2. 邮箱注册，使用QQ邮箱提醒不可用，最后使用的是outlook邮箱可行
3. 注册时，nation就默认为美国吧。

### 2.本地git，heroku安装及操作 ###
1. 安装git  `sudo apt-get install git`即可
2. 安装heroku  `wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh`
3. 在本地建立一个文件夹`heroku` 在heroku文件夹中启动终端,并登陆`heroku login`
4. 按照提示，输入注册用**邮 箱**和**密 码**，出现`logged in as <your email>`代表登录成功。

### 3.平台上新建数据库及文件 ###
上面我们登录进去了，就可以建立我们的app程序/文件夹了，app程序其实就是herokuapp.com的一个子域名，我建立的是**i309**,部署成功后，就可以直接通过地址https://i309.herokuapp.com来访问我的Web应用，名字具有唯一性，重复会有提醒直至是唯一的。

1. 平台上新建app文件`heroku create i309 `这个后面没有报错就是成功了，这个没有多大问题
2. 平台上新建数据库 `heroku addons:create heroku-postgresql:hobby-dev`
		
		/myporoject$ heroku addons:add heroku-postgresql:hobby-dev
		#以下代码表示数据库成功建立
		creating heroku-postgresql:hobby-dev on *guogaitou... free
		Database has been created and is available
		!This database is empty and. If upgrading , you can transfer
		!data from another database with py:copy
		Created postgresql-metric-57886 as DATABASE_URL
		Use herku addons:docs heroku-postgresql to view documentation

3. 升级为主数据库`heroku pg:promote DATABASE_URL` 因为heroku存在升级，此处和《Flask web开发》不同。有必要升级数据库吗？很有必要！借鉴网上教程没有升级数据库，尝试超过10次都显示application error，所以**一定要升级数据库**
		
	**重点讲述数据库，这个数据库和我们本地的数据库文件dev-data.sqlite，一点关系都没有！**需要补充几点：

	1. dev_data.sqlite，只是开发环境下的测试数据库文件，部署之后直接舍弃了；而我们新建的postpresql-metric-57886,才是后期web运行需要的数据库文件。详细的信息，建议去heroku个人界面查看**Database**，这个新建的数据库是后期网站运行的基础
	1. postgresql为heroku自带的数据库类型，完美适应python
	2. 网站对于数据选择有多种，这里仅类型为**hobby**的数据库才可以免费试用，而《Flask web开发》一书中此处是dev，测试导致后期部署不成功。

4. 在本地测试我们的web应用

		gunicorn manage:app
		#显示8000端口可以访问，在本地浏览器打开http://127.0.0.1:8000看到你期盼的页面
		#此时就可以将我们应用推送并部署到hueroku平台了
4. 将我们本地的app文件推送至heroku平台
	
	
		$ git push heroku master 
		...
		To https://git.heroku.com/i309/git
			7dee9cb0..747e62e  master->master
		#等待时间较长，最后出现上方语句，代表推送成功
		
		$ heroku run python manage.py deploy
		...
		#在heroku平台上进行初始化设置
		
		$ heroku restart 
		....
		Restarting dynos...done
		#重启平台dyno容器
6. 访问我们的个人web

		方法一：
		$ heroku open 
		#稍等片刻，程序自动打开我们的浏览器并调账到刚部署好的web网站了。

		方法二：
		打开浏览器输入https://<your_app_name>.herokuapp.com
		在这里我的就是https://i309.herokuapp.com
		
### 2后期更新汇总 ###
个人web部署成功了，使用的方法和官网介绍有一定的不同。结合他人的经历，和自己的尝试，亲测上述方法可行。

1. 再次部署时，发现在浏览器无法登陆heroku官网，需要结合翻墙软件，告一段落  11/23/2017 1:03:08 PM 
