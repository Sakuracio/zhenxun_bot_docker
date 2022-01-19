# zxenv

#### 介绍
尝试使用docker快速部署zhenxun_bot的一个方案  

##### 使用方法
请提前下载好docker 国内服务器可以参考使用加速地址   
```shell
# 请使用docker volume或映射目录做好数据持久化运行

docker volume create zhenxun_bot

docker pull hibikier/zhenxun_bot:latest

docker run -d --name zhenxun_bot \
    -v zhenxun_bot:/bot \
    hibikier/zhenxun_bot:latest

# 如果官方镜像拉取速度缓慢可以尝试使用加速镜像

# 加速镜像 香港节点(无法拉取时请使用官方镜像)
docker volume create zhenxun_bot

docker pull registry.cn-hongkong.aliyuncs.com/sakuracio/zhenxun_bot:latest

docker run -d --name zhenxun_bot \
    -v zhenxun_bot:/bot \
    registry.cn-hongkong.aliyuncs.com/sakuracio/zhenxun_bot:latest
	
```

#### FINGERPOST
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)
