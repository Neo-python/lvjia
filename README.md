# 绿佳食品数据管理系统
![Python](https://img.shields.io/badge/Python-3.6-519dd9.svg)
![Flask](https://img.shields.io/badge/Flask-1.0.2-519dd9.svg)
![PyMySQL](https://img.shields.io/badge/PyMySQL-0.9.3-519dd9.svg)
![redis](https://img.shields.io/badge/redis-3.1.0-519dd9.svg)

### 项目介绍
##### 1.项目目标
为食品生产厂家提供: 客户数据管理/产品数据管理/订单数据管理/财务数据管理/出货,生产报表打印
##### 2.开发详情
2019-02-14立项,2019-02-26交付客户,经过客户的同意.在抹除与客户有关的信息的情况下,允许开源.
##### 3.使用说明
    整体架构
        nginx + uwsgi 部署服务
        python相关依赖库通过 pip install -r requirements.txt 安装
        静态文件下载链接:https://share.weiyun.com/5SVx4yF
        数据库结构文件:lvjia_database.sql.快速建立数据库结构 --> 进入mysql后 执行 source /this_sqlFile_path/lvjia_database.sql;
        config.py中的配置信息,需要根据自己的情况设定
    其他:
        因为是定制系统,出货与生产的报表模板需要使用此项目的小伙伴自行设计咯.
### 其他
##### 对python开发感兴趣的,打算学习python开发的可以了解一下
        https://ke.qq.com/teacher/526599801
        这是我三年前跟着学习的一位教python开发的编程老师:雨辰.这位老师课程内容全是干货,不说废话来增加无意义的课程时间.
        
    


