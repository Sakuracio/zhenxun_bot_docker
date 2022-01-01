#!/bin/bash

# docker安装
function docker_install() {
	echo "====检查docker是否安装======"
	docker -v
	if [ $? -eq 0 ]; then
		echo "====检查docker已经安装======"
	else
		echo "====未检测到docker===="
		echo "====开始安装docker===="
		echo "嘛 这种东西你还是自己安装吧 安装完成后记得设置容器镜像加速!"
		echo "======================"
		exit
	fi
	echo "====启动docker========"
	#systemctl start docker.service
	echo "====docker启动完成===="
}

# docker 拉取镜像
function docker_pull_images() {
	# 获取已经有的所有镜像
	existImages=($(docker images | awk '{print $1":"$2}' "")) # 获取当前所有镜像
	# 获取镜像个数
	existImagesNum=${#existImages[@]}
	#echo $Doc_Ima_i
	# 需要拉取的镜像
	needImages=(
		"postgres:latest"
		"python:3.8.12"
	)
	needImagesNum=${#needImages[@]}
	#echo needImagesNum

	# 查看镜像是否存在
	for ((i = 0; i < needImagesNum; i++)); do
		#echo ${needImages[$i]}
		isExist=0
		for ((j = 0; j < existImagesNum; j++)); do
			#echo ${existImages[$j]}
			if [[ ${needImages[$i]} == ${existImages[$j]} ]]; then
				isExist=1
				break
			fi
		done
		if [[ $isExist -eq 1 ]]; then
			echo ${needImages[$i]}" 镜像已存在"
		else
		    if [ ! -f /etc/docker/daemon.json ]; then
                echo "设置docker容器加速镜像"
                echo  '{"registry-mirrors":["https://docker.mirrors.ustc.edu.cn/"]}' > /etc/docker/daemon.json
            else
                echo "daemon.json 已经存在 如果拉取速度缓慢 请尝试手动设置docker容器加速镜像"
            fi
			echo ${needImages[$i]}" 镜像不存在 准备拉取 如果拉取速度缓慢 请配置docker镜像加速"
			# 拉取不存在的镜像
			docker pull ${needImages[$i]}
		fi
	done
}
cd /home
# 安装并启动docker
docker_install
# 拉取镜像
docker_pull_images
# 下载文件
if [ ! -d "/home/zxenv/" ]; then
	echo "创建 zxenv 文件夹 开始下载文件"
	mkdir /home/zxenv
else
	echo "zxenv 文件夹已经存在 请确保文件夹干净 开始下载文件"
fi
wget https://gitee.com/Sakuraciowo/zxenv/repository/archive/v3b8f2-0.71?format=tar.gz -O /home/zxenv.tar.gz
tar -zxvf /home/zxenv.tar.gz -C /home/zxenv/
mv /home/zxenv/zxenv-v3b8f2-0.71/gocq /home/zxenv
mv /home/zxenv/zxenv-v3b8f2-0.71/zhenxun_bot /home/zxenv
rm -rf /home/zxenv/zxenv-v3b8f2-0.71
clear
echo "==== bot文件已经下载到/home/zxenv ===="

echo "开始部署 postgres 容器"
docker run -it --name zhenxun_data --restart always -e TZ='Asia/Shanghai' -e POSTGRES_PASSWORD='PASSWORD' -e ALLOW_IP_RANGE=0.0.0.0/0 -v /home/postgres/data:/var/lib/postgresql -p 35432:5432 -d postgres
chmod 777 -R postgres
echo "开始部署 python 容器"
docker run -it --name zhenxun_bot --restart always -e TZ='Asia/Shanghai' -v /home/zxenv:/usr/src/app -w /usr/src/app -d python:3.8.12
chmod 777 -R zxenv
read -p '设置Bot账号：==>> ' SETBOTNUM
sed -i "s/3249605/$SETBOTNUM/g" /home/zxenv/gocq/config.yml

# 获取容器ip
DOCKERIPID=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' zhenxun_data)

echo "设置ws连接地址"
# sed -i "s/127.0.0.1:8080/$DOCKERIPID:8080/g" /home/zxenv/gocq/config.yml

read -p '设置超级用户账号：==>> ' SETSUNUM
sed -i "s/3249605/$SETSUNUM/g" /home/zxenv/zhenxun_bot/.env.dev

echo "设置数据库地址"
sed -i "s/0.0.0.0:5432/$DOCKERIPID:5432/g" /home/zxenv/zhenxun_bot/configs/config.py

# 调整配置
wget https://gitee.com/Sakuraciowo/zxenv/raw/dev/sources.list -O /home/zxenv/sources.list

clear
echo "=========    开始配置 postgres 数据库    ========="
echo "=========    开始配置 postgres 数据库    ========="
echo "=========    开始配置 postgres 数据库    ========="
echo "请依次运行下面的命令    请依次运行下面的命令    请依次运行下面的命令"
echo "
su - postgres
psql
CREATE USER zhenxun WITH PASSWORD 'zhenxun';    #(注意分号一起复制)
CREATE DATABASE zhenxundata OWNER zhenxun;      #(注意分号一起复制)
exit (敲3次 喂！不是exit exit exit)
"
docker exec -it zhenxun_data bash

clear
echo "=========    数据库的配置已经完成 现在继续配置 Bot 环境    ========="
echo "=========    数据库的配置已经完成 现在继续配置 Bot 环境    ========="
echo "=========    数据库的配置已经完成 现在继续配置 Bot 环境    ========="
echo "请依次运行下面的命令    请依次运行下面的命令    请依次运行下面的命令"
echo "
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
mv /etc/apt/sources.list /etc/apt/sources.list.d
cp /usr/src/app/sources.list /etc/apt
apt update && apt -y install libgl1-mesa-glx screen
apt -y install ffmpeg(如果不需要发送语音的功能可以忽略本行)
exit
"
docker exec -it zhenxun_bot bash
clear
echo "
配置已经完成 现在你可以使用下面的命令进入bot容器中
docker exec -it zhenxun_bot bash
你需要
进入   gocq目录登录bot账号
进入真寻Bot目录安装pip依赖 然后使用 python bot.py 你可以使用screen
如果不出意外 你已经安装了 Screen 和 FFmpeg 你可以直接使用
退出容器使用 exit 即可
如果你重启了机器或容器后 提示 数据库连接错误
你需要检查真寻的数据库容器是否正常运行
以及 检查容器IP是否变动 修改IP或锁定IP
如果你要修改文件 直接在主机/home/zxenv中修改即可 再会!!!!!!!
"
