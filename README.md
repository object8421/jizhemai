# 基本信息
项目名称：记着买

项目代号：jizhemai

项目概述：简便地解决购物过程中做笔记的需求，并以此为起点，形成平台式的商业项目

发起人所在城市：深圳

团队背景：

@rayxiehui ：
1. 前端工程师，丰富的前端经验；
2. 了解JS,（微信浏览器接口是JSSDK）；
3. 对webapp的实现有一定的经验。

@Langp618
硬件工程师，主要从事产品开发

@ivanlau
1. 学习建筑设计，多年专门ps为主工作经验，可以负责部分视觉的业务以及汇报的东西；
2. 后从事公司信息业务、负责信息化部门多年，作为甲方负责过多个内部IT项目全过程的管理（包括需求调研、开发及项目管理、运维等），系统用户达两千人；
3. 多年业余从事域名、建站(php)等业务，对互联网以及建站技术有一定了解；
4. 业余开过实体与网上服装店，对一般零售业务有一定了解。


观察员：
竹子 @bambooom


# 项目描述

## 构思

购物是一个复杂的决策过程，除了部分不以钱为约束条件的情形，大多数购物决策是相对烧脑的行为。针对消费行为里面大量基于“划算”为目的的决策，提供一个潜在购买商品的记录工具是一个有现实意义的。

就像markdown的流行一样，markdown可以让大多数真正要写博客的人抛开繁琐的标签（如html）、臃肿而封闭的工具（word）以及不稳定的编辑器（如各大在线富文本编辑器），专心地写作，享受写作的过程。对于购物来说也一样。

"让消费者享受购物的乐趣"是项目的宗旨。

## 功能

利用公众号，让用户快速地录入需要记录的待购信息，以尽可能结构化的方式存储数据，以便信息的快速输出和有效利用。

这个定义包含了两个重要的关键词：快速、结构化，这就是这个产品的最核心特点。

产品必须是快速的，用户不需要关心太多的功能以及繁琐的操作，点开公众号，激活功能即可录入数据。

输入的界面，应该尽量简洁，利用微信的接口做尽量多的自动信息采集，必要的操作尽量少，每次行为设计都应该精确计算用户的行为并进行优化。

初期录入定义为照片、价格、描述（非结构化数据的大包裹），在资源许可情况下采集录音，自动获取主要是地理位置。

产品的输入数据设计必须是尽可能的结构化的，这样才有利于数据利用。

快速和结构化显然是矛盾的，如何找到平衡是项目的关键（具体内容可在项目过程中继续探讨）。


## （本期）产品内容

本期内容以基于微信的用户端为主，有余力再做其它功能，描述在“展望”一节。

本期的具体功能为：

- 信端录入信息，通过菜单激活功能，调用浏览器实现图片等信息的上传。
- 调出录入的信息。


## 展望

因为本期时间较短，所以定一个相对可操作可实现的功能作为第一期内容。产品发展的路线图大致如下：


------------------------
本期相对可实现的结果

- 微信录入信息；
- 微信展现信息（单条以及批量展示）；

------------------------
可期待的未来（需要的时间较多）

- 录入的优化，包括后期需优化输入内容，包括页面tag的提示、推送、录入等实现
- 用户分享存储的信息（展示模板，解决朋友圈展示的一些问题）；
- 网页web端的详细功能；

------------------------
稍微遥远的未来（需要的资源较多）

- 对搜索（引擎、分词）等的优化，实现更多的数据可用； 
- 根据数据的进一步利用实现推送（产品、优惠、促销提醒等），实现下一阶段的跨越；
- B2B、B2C、B2B2C的发展。

### *“不想做平台的应用不是好产品 -- 弗莱德·培根”*

实际上项目的目标是做成和平台式的产品。而为了实现这一目标，首先是要聚焦地做好一个工具级的产品。要做用户的贴心小棉袄，那首先就是要足够的便利好用，然后开发共享功能形成进行病毒式的传播。当用户数据有足够多的时候，通过对分词、搜索功能的研发，有效提取相关信息以得出消费的的数据，进行后续的发展（数据分析&大数据嘢亲）。

本项目作为一个数据生成节点，在数据流转过程中是中上游的位置，具有非常大的后发优势。

对于商家来说，只要和用户绑定的关系有足够紧密，商家就有足够理由利用平台进行精准的商业推广。在这个过程里面，如果要深耕这一部分的市场，甚至可以代理商家的网上销售渠道，这就实现了平台的第一步发展。

由于还有太多想法需要更进一步的组织才适合描述得更加清晰，很多包括online与offline之间的导流、本项目与传统电商平台比较之间的优势等更多细节问题欢迎加入项目共同商讨。

## 其它疑问以及思考：
和购物推荐网站之间的差别
实际无论从定位和应用场景来说还是很不一样的。微博是信息的洪流，大V的话语权远大于草根，购买推荐网站就像微博一样，信息的洪流里面是否有多少自己的心愿？记住，要怂。我只想做个安静的...怎么办？精准社交平台微信就是这样的需求。这个项目就是基于类似的产品逻辑，给用户提供的只是个人工具，即便平台化运作，也是后台数据平台而非像推荐系统的平台。

还有一个类型潜在竞品就是各种笔记，但经过我疯狂给周边的朋友同事领导家人推荐两个很多人推广这几个笔记软件之后，发现了，这些功能完备的软件真的不一定适合一些具体业务。

## 本期需要达到的外部环境：
- 空间以及运行的环境
- 数据库
- 域名
- 公众号（服务号）

## 难点：
- 图片等信息的储存以及调用的实现方法。
- 速度速度速度

## 急求同伙
- 微信作业玩的溜的同学
- 了解数据库的同学
- 有兴趣参与本项目的各位

# 画饼
太多激情无法展现于冰冷的显示屏上，欢迎入伙共同探讨共同进步！
这不是对已有互联网世界的功能调整与整合，这是打造互联网商业新入口的事业！成功我们指日可待！ 


![zrkd](https://cloud.githubusercontent.com/assets/8110519/11532201/4c0220b0-993d-11e5-8f40-7d64cdfc346d.jpg)
