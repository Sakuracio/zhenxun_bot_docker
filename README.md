# zxenv

#### 介绍
尝试使用 docker 快速部署 zhenxun_bot 的一个方案  

##### 使用方法
请提前下载好 docker
```shell
# 请使用 docker volume 或映射目录做好数据持久化运行
# 官方镜像↓ 建议配合 postgres docker 使用

docker run \
	--name zhenxun_bot \
	--network=host \
	-v /home/zhenxun_bot:/bot \
	-e SU='管理员企鹅号' \ #(可选)
	-e DB='数据库连接链接地址' \ #(可选)
	sakuracio/zhenxun_bot:latest

# 确保映射的目录 /home/zhenxun_bot 为空 可自行设置
# 如果官方镜像拉取速度缓慢可以尝试使用加速镜像

# 国内加速镜像 (无法正常拉取时请使用官方镜像)

docker pull cloudbase-100005283109-docker.pkg.coding.net/sakuracio/zhenxun_bot/zhenxun_bot:[版本号]

# 版本号对应真寻 Bot 版本也可到底部制品仓库查看
```

#### FINGERPOST
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)  
[制品仓库](https://cloudbase-100005283109.coding.net/public-artifacts/Sakuracio/zhenxun_bot/packages)  
