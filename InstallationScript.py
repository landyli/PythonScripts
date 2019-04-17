#!/usr/bin/python3.6
# -*- coding:utf-8 -*-
# 注意：本脚本使用root用户。需要安装python3.6.5
# Author:  WangJi
# Version: 1.0.1
# Last editing time:  2019-04-11 12:00:00
import subprocess
import sys
import os

#定义开头显示的提示选择信息
info = '''    
    ----- Select Install option -----
    1.Install Nginx-1.12.2
    2.Install mysql-5.7.22
    3.Install PHP-7.2.17
    4.Install Redis-5.0.4
    5.Install BBR
    6.Install rsync
    7.修改系统时间和安装常用软件
    9.Exit Program
    ---------------------------------
    '''

my_cnf = '''
[mysqld] 
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
character-set-server=utf8
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
symbolic-links=0
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid


server-id = 1                                      #用于复制环境钟标识实例,这个在复制环境里唯一
character-set-server = utf8                        #服务端默认字符集,很重要,错误设置会出现乱码
max_connections = 1000                             #允许客户端并发连接的最大数量
max_connect_errors = 6000                          #如果客户端尝试连接的错误数量超过这个参数设置的值，则服务器不再接受新的客户端连接
open_files_limit = 65535                           #操作系统允许MySQL服务打开的文件数量。
table_open_cache = 128                             #所有线程能打开的表的数量
max_allowed_packet = 32M                           #网络传输时单个数据包的大小。
binlog_cache_size = 1M
max_heap_table_size = 1288M
tmp_table_size = 16M
read_buffer_size = 2M
read_rnd_buffer_size = 8M
sort_buffer_size = 16M
join_buffer_size = 16M
key_buffer_size = 4M
thread_cache_size = 8
query_cache_type = 1
query_cache_size = 4096M
query_cache_limit = 4M
ft_min_word_len = 4
log_bin = mysql-bin
binlog_format = mixed
expire_logs_days = 30
slow_query_log = 1
long_query_time = 1
slow_query_log_file = /usr/local/mysql/data/mysql-slow.log      #慢查询日志
performance_schema = 0
explicit_defaults_for_timestamp
lower_case_table_names = 1
skip-external-locking
default_storage_engine = InnoDB
#default-storage-engine = MyISAM
innodb_file_per_table = 1
innodb_open_files = 16350
innodb_buffer_pool_size = 10G
innodb_write_io_threads = 16
innodb_read_io_threads = 16
innodb_thread_concurrency = 32
innodb_purge_threads = 1
innodb_flush_log_at_trx_commit = 2
innodb_log_buffer_size = 128M
innodb_log_file_size = 1G
innodb_log_files_in_group = 3
innodb_max_dirty_pages_pct = 90
innodb_lock_wait_timeout = 120
bulk_insert_buffer_size = 8M
myisam_sort_buffer_size = 8M
myisam_max_sort_file_size = 10G
myisam_repair_threads = 1
interactive_timeout = 512
wait_timeout = 256
#lower_case_table_names = 1
skip-external-locking
default_storage_engine = InnoDB
#default-storage-engine = MyISAM

[client]
default-character-set=utf8

[mysql]
default-character-set=utf8
'''

rsyncConfig = '''
uid = root
gid = root
use chroot = yes
max connections = 500
lock file=/var/run/rsyncd.lock
log file = /var/log/rsyncd.log
exclude = lost+found/
transfer logging = yes
timeout = 900
ignore nonreadable = yes
dont compress   = *.gz *.tgz *.zip *.z *.Z *.rpm *.deb *.bz2

[mp3]
path = /home/mp3
comment = Hostname mp3
read only = yes
list = no
auth users=rsyncuser
secrets file=/etc/rsyncd.passwd
hosts allow=*

[picture]
path = /home/picture
comment = Hostname picture
read only = yes
list = no
auth users=rsyncuser
secrets file=/etc/rsyncd.passwd
hosts allow=*

[videos]
path = /home/videos
comment = Hostname videos
read only = yes
list = no
auth users=rsyncuser
secrets file=/etc/rsyncd.passwd
hosts allow=*
'''

while True:
    print(info)
    n = input('Input your select: ')
    if n.isdigit():  # 判断是否是数字
        n = int(n)  # 如果是就转换成整型，raw_input接收类型默认是字符串型
        if n <= 9 and n >= 1:  # 数字必须在可选范围之内
            if not os.path.isdir('/home/www'):  # 判断是否存在/home/www目录
                os.mkdir('/home/www')  # 不存在就创建
            else:
                if n == 1:  # 如果选的是1,运行shell命令安装nginx
                    print("升级安装Nginx")
                    subprocess.call(["rpm -Uvh http://nginx.org/packages/centos/7/x86_64/RPMS/nginx-1.14.2-1.el7_4.ngx.x86_64.rpm"], shell=True)
                    print("设置开机启动")
                    subprocess.call(["systemctl enable nginx.service"], shell=True)
                    print("启动nginx服务")
                    subprocess.call(["systemctl start nginx.service"], shell=True)
                    print("重新加载nginx")
                    subprocess.call(["nginx -s reload"], shell=True)
                    print("打完收工")

                elif n == 2:  # 编译安装mysql，每个命令都在屏幕上显示；安装包提前放在/root/soft目录下
                    print("remove mariadb")
                    subprocess.call(["yum remove maria* -y"], shell=True)
                    print("Download Mysql5.7 RPM pakeage")
                    subprocess.call(["wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm"], shell=True)
                    print("Install local RPM pakeage")
                    subprocess.call(["yum localinstall mysql57-community-release-el7-11.noarch.rpm"], shell=True)
                    print("Install Mysql5.7")
                    subprocess.call(["yum install -y mysql-community-server"], shell=True)
                    print("Open Start-up and Boot-up")
                    subprocess.call(["systemctl daemon-reload && systemctl start mysqld && systemctl enable mysqld"], shell=True)
                    print("Empty my.cnf")
                    subprocess.call(["echo > /etc/my.cnf"], shell=True)
                    
                    print("创建mysql配置文件")
                    with open("/etc/my.cnf", "a") as f:
                        f.write(my_cnf)
                    f.close()
                    print("打完收工")

                elif n == 3:
                    print("Install dependency packages")
                    subprocess.call(["yum update -y && yum install -y yum-utils && rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm"],shell=True)
                    print("Install PHP 7.2 along with dependencies.")
                    subprocess.call(["yum -y install php72w-fpm php72w-devel php72w-cli php72w-bcmath php72w-bz2 php72w-calendar  php72w-ctype php72w-curl php72w-date php72w-dba php72w-dom php72w-exif php72w-fileinfo php72w-filter php72w-ftp php72w-gd php72w-gettext php72w-gmp php72w-hash php72w-iconv php72w-json php72w-libxml php72w-mbstring php72w-mysqlnd php72w-openssl php72w-pcre   php72w-posix php72w-readline php72w-pecl-redis php72w-session php72w-shmop php72w-soap php72w-sockets php72w-standard php72w-sysvmsg php72w-sysvsem php72w-sysvshm php72w-tokenizer php72w-wddx php72w-xml php72w-xmlreader php72w-xmlrpc php72w-xmlwriter php72w-xsl php72w-zip php72w-zlib"], shell=True)
                    # print("安装redis扩展")
                    # subprocess.call(["yum install php-pecl-redis"], shell=True)
                    # subprocess.call(["cd /usr/local/src && yum install -y git && git clone https://github.com/phpredis/phpredis.git && cd phpredis && \
                    #                   /usr/local/php/bin/phpize && ./configure --with-php-config=/usr/local/php/bin/php-config && make -j24 && make install && \
                    #                   sed -i '%a extension=redis.so' /etc/php.ini"])
                    print("设置开机自启")
                    subprocess.call(["systemctl start php-fpm && systemctl enable php-fpm && php-fpm -v"], shell=True)
                    print("Install PHP composer tools")
                    subprocess.call(["curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/local/bin/composer"], shell=True)
                    print("打完收工")

                elif n == 4:
                    print("Install redis")
                    subprocess.call(["yum install -y http://rpms.famillecollet.com/enterprise/remi-release-7.rpm && yum --enablerepo=remi install -y redis"], shell=True)
                    print("Start-up redis")
                    subprocess.call(["systemctl start redis && systemctl enable redis"], shell=True)
                    print("打完收工")

                elif n == 5:
                    print("Install dependency packages")
                    subprocess.call(["yum install -y glibc && rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org && \
                                          rpm -Uvh https://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm"], shell=True)
                    print("Upgrade the latest stable version of the kernel")
                    subprocess.call(["yum --enablerepo=elrepo-kernel install kernel-ml -y && grub2-set-default 0"], shell=True)
                    print("Start-up BBR")
                    subprocess.call(["echo 'net.core.default_qdisc=fq' | tee -a /etc/sysctl.conf && \
                                    echo 'net.ipv4.tcp_congestion_control=bbr' | tee -a /etc/sysctl.conf && sysctl -p"], shell=True)
                    print("打完收工")

                elif n == 6:
                    print("Install rsync")
                    subprocess.call(["yum -y install rsync && echo 'rsyncuser:jw63$^fwqf8' > /etc/rsyncd.passwd && chmod 600 /etc/rsyncd.passwd"], shell=True)
                    with open("/etc/rsyncd.conf", "a") as f:
                        f.write(rsyncConfig)
                    f.close()
                    print("打完收工")


                elif n == 7:
                    try:
                        print("修改机器八时区和机器名称")
                        subprocess.call(["timedatectl set-local-rtc 1 && timedatectl set-timezone Asia/Shanghai && ntpdate us.pool.ntp.org && hostnamectl set-hostname HOSTNAME"], shell=True)
                        print("安装系统常用命令")
                        subprocess.call(["yum install epel-release -y && yum install wget vim iftop htop iotop curl lrzsz -y && \
                                        systemctl stop firewalld && \
                                        setenforce 0 && \
                                        sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config"], shell=True)
                        print("打完收工")
                    except:
                        print("Error, What the fuck")

                elif n == 9:  # 退出程序
                    print("Program will be quite!")
                    sys.exit()
                    
                else:
                    print('you select is not correct')
        else:
            print('you should input number')













# ./configure后

# 编辑MakeFile

# 找到 开头是 'EXTRA_LIBS' 这一行 在结尾加上 '-llber' 然后执行 make && make install
                    # print("Install dependency packages")
                    # subprocess.call(
                    #         [
                    #             "yum install openldap openldap-devel epel-release gcc gcc-c++ libxml2 libxml2-devel openssl openssl-devel \
                    #                          bzip2 bzip2-devel libcurl libcurl-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel \
                    #                          gmp gmp-devel libmcrypt libmcrypt-devel readline readline-devel libxslt libxslt-devel -y"],
                    #         shell=True)
                    # print("Download install package、 compile install php")
                    # subprocess.call(["cd /usr/local/src && wget https://www.php.net/distributions/php-7.2.17.tar.gz && cp -frp /usr/lib64/libldap* /usr/lib/ && tar -zxvf php-7.2.17.tar.gz && cd php-7.2.17/ && ./configure \
                    #     --prefix=/usr/local/php \
                    #     --with-config-file-path=/etc \
                    #     --enable-fpm \
                    #     --with-fpm-user=nginx \
                    #     --with-fpm-group=nginx \
                    #     --enable-inline-optimization \
                    #     --disable-debug \
                    #     --disable-rpath \
                    #     --enable-shared \
                    #     --enable-soap \
                    #     --with-libxml-dir \
                    #     --with-xmlrpc \
                    #     --with-openssl \
                    #     --with-mcrypt \
                    #     --with-mhash \
                    #     --with-pcre-regex \
                    #     --with-sqlite3 \
                    #     --with-zlib \
                    #     --enable-bcmath \
                    #     --with-iconv \
                    #     --with-bz2 \
                    #     --enable-calendar \
                    #     --with-curl \
                    #     --with-cdb \
                    #     --enable-dom \
                    #     --enable-exif \
                    #     --enable-fileinfo \
                    #     --enable-filter \
                    #     --with-pcre-dir \
                    #     --enable-ftp \
                    #     --with-gd \
                    #     --with-openssl-dir \
                    #     --with-jpeg-dir \
                    #     --with-png-dir \
                    #     --with-zlib-dir \
                    #     --with-freetype-dir \
                    #     --enable-gd-native-ttf \
                    #     --enable-gd-jis-conv \
                    #     --with-gettext \
                    #     --with-gmp \
                    #     --with-mhash \
                    #     --enable-json \
                    #     --enable-mbstring \
                    #     --enable-mbregex \
                    #     --enable-mbregex-backtrack \
                    #     --with-libmbfl \
                    #     --with-onig \
                    #     --enable-pdo \
                    #     --with-mysqli=mysqlnd \
                    #     --with-pdo-mysql=mysqlnd \
                    #     --with-zlib-dir \
                    #     --with-pdo-sqlite \
                    #     --with-readline \
                    #     --enable-session \
                    #     --enable-shmop \
                    #     --enable-simplexml \
                    #     --enable-sockets \
                    #     --enable-sysvmsg \
                    #     --enable-sysvsem \
                    #     --enable-sysvshm \
                    #     --enable-wddx \
                    #     --with-libxml-dir \
                    #     --with-xsl \
                    #     --enable-zip \
                    #     --with-ldap \
                    #     --enable-mysqlnd-compression-support \
                    #     --with-pear \
                    #     --enable-opcache && make -j24 && make install"], shell=True)

                    # print("Configuring environment variables")
                    # subprocess.call(["sed -i '$a export PATH=$PATH:/usr/local/php/bin' /etc/profile && source /etc/profile"], shell=True)
                    # print("Configuration php-fpm")
                    # subprocess.call([
                    #     "cp /usr/local/src/php-7.2.17/php.ini-production /etc/php.ini && cp /usr/local/php/etc/php-fpm.conf.default /usr/local/php/etc/php-fpm.conf"],
                    #         shell=True)
                    # subprocess.call([
                    #     "cp /usr/local/php/etc/php-fpm.d/www.conf.default /usr/local/php/etc/php-fpm.d/www.conf"],
                    #         shell=True)
                    # subprocess.call([
                    #     "cp /usr/local/src/php-7.2.17/sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm"],
                    #         shell=True)
                    # print("给php启动脚本授权")
                    # subprocess.call(["chmod +x /etc/init.d/php-fpm"], shell=True)
                    # print("安装redis扩展")
                    # subprocess.call(["yum install php-pecl-redis"], shell=True)
                    # # subprocess.call(["cd /usr/local/src && yum install -y git && git clone https://github.com/phpredis/phpredis.git && cd phpredis && \
                    # #                   /usr/local/php/bin/phpize && ./configure --with-php-config=/usr/local/php/bin/php-config && make -j24 && make install && \
                    # #                   sed -i '%a extension=redis.so' /etc/php.ini"])
                    # print("启动php")
                    # subprocess.call(["/etc/init.d/php-fpm start"], shell=True)
                    # print("设置开机自启")
                    # subprocess.call(["chkconfig --add php-fpm"], shell=True)
                    # print("Install PHP composer tools")
                    # subprocess.call(["curl -sS https://getcomposer.org/installer | php && mv composer.phar /usr/local/bin/composer"])
                    # print("打完收工")