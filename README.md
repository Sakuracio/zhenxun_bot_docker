# 使用 docker 部署 zhenxun_bot

![](https://img.shields.io/badge/Python%E7%89%88%E6%9C%AC-3.9-ff69b4?style=for-the-badge)
![](https://img.shields.io/docker/image-size/hibikier/zhenxun_bot?label=%E9%95%9C%E5%83%8F%E5%A4%A7%E5%B0%8F&style=for-the-badge)
![](https://img.shields.io/docker/pulls/hibikier/zhenxun_bot?label=%E4%B8%8B%E8%BD%BD%E6%AC%A1%E6%95%B0&style=for-the-badge)
![](https://img.shields.io/badge/%E6%94%AF%E6%8C%81%E5%B9%B3%E5%8F%B0-amd64-8B008B?style=for-the-badge)

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
# 如果你使用 Mac OSX 或其他不支持 host 模式的环境 请使用-p 参数映射端口
# DB 示例 postgresql://user:password@127.0.0.1:5432/database
```
### 如果你在 ARM 平台运行请查看
[![Github](https://shields.io/badge/GITHUB-SinKy--Yan-4476AF?logo=github&style=for-the-badge)](https://github.com/SinKy-Yan/zhenxunbot-docker)
[![DOCKER](https://shields.io/badge/docker-jyishit/zhenxun_bot-4476AF?logo=docker&style=for-the-badge)](https://hub.docker.com/r/jyishit/zhenxun_bot/)

**如果你的机器 RAM < 1G  可能无法正常启动**

#### 指路
[![Github](https://shields.io/badge/GITHUB-HibiKier/zhenxun_bot-4476AF?logo=github&style=for-the-badge)](https://github.com/HibiKier/zhenxun_bot)
