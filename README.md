# 使用 docker 部署 zhenxun_bot

## 使用方法
```shell
# 请使用 docker volume 或映射目录做好数据持久化运行
# 官方镜像↓ 建议配合 postgres docker 使用

docker run \
	--name zhenxun_bot \
	--network=host \
	-v /home/zhenxun_bot:/bot \
	-e SU='管理员企鹅号' \ #(可选)
	-e DB='数据库链接地址' \ #(可选)
	hibikier/zhenxun_bot:latest

# 确保映射的目录 /home/zhenxun_bot 为空 可自行设置
# 如果你使用 MacOSX 或其他不支持 host 模式的环境 请使用-p参数映射端口
```
### 如果你在 ARM 平台运行请查看
Github: [SinKy-Yan/zhenxunbot-docker](https://github.com/SinKy-Yan/zhenxunbot-docker)  
docker hub: [jyishit/zhenxun_bot](https://hub.docker.com/r/jyishit/zhenxun_bot/)

#### FINGERPOST
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)  
