# 帮助文档

www.github.com.cnpmjs.org


### 配置jupyter

生成配置文件
        jupyter notebook --generate-config

       记录配置文件生成路径，后面修改该配置文件

python
from notebook.auth import passwd
passwd()
'argon2:$argon2id$v=19$m=10240,t=10,p=8$ZX4zzHk5bPaCnLNK7Je9gw$Wvhew+RYn3ezDHEaVLK/Wg'




c.NotebookApp.ip = '*'
c.NotebookApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$ZX4zzHk5bPaCnLNK7Je9gw$Wvhew+RYn3ezDHEaVLK/Wg'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8989



1. 查看当前python的版本号

python -V
2.查看服务器是否有python3

python3 -V
3. 如有，则使用命令查看所有python地址

ls /usr/bin/python*
4. 更改当前版本

alias python='/usr/bin/python3.5'
　　若报错，则先输入bash

5. 成功





jupyter notebook --ip=0.0.0.0 --no-browser --allow-root

ps -aux | grep jupyter


### 1.安装Anaconda。
bash Anaconda3-2020.11-Linux-x86_64.sh
打开命令行输入conda -V检验是否安装及当前conda的版本。

2.conda常用的命令

1）查看安装了哪些包

conda list
2)查看当前存在哪些虚拟环境

conda env list 
conda info -e
3)检查更新当前conda

conda update conda
3.Python创建虚拟环境

conda create -n your_env_name python=x.x
anaconda命令创建python版本为x.x，名字为your_env_name的虚拟环境。your_env_name文件可以在Anaconda安装目录envs文件下找到。

4.激活或者切换虚拟环境

打开命令行，输入python --version检查当前 python 版本。

Linux:  source activate your_env_nam
Windows: activate your_env_name
5.对虚拟环境中安装额外的包

conda install -n your_env_name [package]
6.关闭虚拟环境(即从当前环境退出返回使用PATH环境中的默认python版本)

deactivate env_name
或者`activate root`切回root环境
Linux下：source deactivate 
7.删除虚拟环境

conda remove -n your_env_name --all
8.删除环境钟的某个包

conda remove --name $your_env_name  $package_name 
8、设置国内镜像

http://Anaconda.org的服务器在国外，安装多个packages时，conda下载的速度经常很慢。清华TUNA镜像源有Anaconda仓库的镜像，将其加入conda的配置即可：

####  添加Anaconda的TUNA镜像

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

####  TUNA的help中镜像地址加有引号，需要去掉

####  设置搜索时显示通道地址

conda config --set show_channel_urls yes

9、恢复默认镜像

conda config --remove-key channels



### hive
ssh  dip-hdp-master01
su  - dolphinscheduler
hive
show databases;
use ods;


quit;

### linux
yum可以用于运作rpm包，例如在Fedora系统上对某个软件的管理：
安装：yum install <package_name> 
卸载：yum remove <package_name> 
更新：yum update <package_name> 

apt-get可以用于运作deb包，例如在Ubuntu系统上对某个软件的管理：
安装：apt-get install <package_name> 
卸载：apt-get remove <package_name> 
更新：apt-get update <package_name>





docker run -it --entrypoint=/python ml-api:latest

exit

docker commit afcaf46e8305 ml-api

docker ps -a
docker rm id

docker save -o ml-api.tar ml-api:latest





docker run --name ml_flask_api -v $PWD/ml_work:/ml_work -p 5000:5000 ml-api:latest

docker run -d --entrypoint=python --name ml_flask_api -v $PWD/ml_work:/ml_work -p 5000:5000 ml-api:latest api.py
docker run -d --entrypoint=python --name ml_flask_api -v $PWD/ml_work:/ml_work -p 5000:5000 ml-api-img:latest api.py