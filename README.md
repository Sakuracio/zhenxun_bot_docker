# 使用 docker 部署 zhenxun_bot

## 使用方法
请提前下载好 docker
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

```

#### FINGERPOST
[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)  
