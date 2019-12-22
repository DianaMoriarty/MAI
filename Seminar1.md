# Начало работа с github
1) Регистрируетесь на github.com  
2) Заходите на https://github.com/erlong15/otus-linux  
3) Нажимате `Fork` (кнопка сверху справа) - в вашем репозитории появится копия проекта
4) На рабочей машине делаете `git clone <ссылка на ваш репозиторий>` - кнопка "clone or download"  
5) Вносите правки, работаете над проектом, делаете 
```
git add .
git commit -m <comment> -a
```  
6)  По окончании работы делаете `git push`   
7)  В "Чате с преподавателем" отсылаете ссылку на ваш репозиторий  

Полезные ссылки по git:  
https://git-scm.com/book/ru/v1/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5  
https://githowto.com/ru  
https://learngitbranching.js.org/ 

# Начало работы с vagrant
Vagrant - система для создания и управления тестовой инфраструктурой, 
для развертываения виртуальных машин (https://www.vagrantup.com/docs/).
В качества провайдера мы будем использовать Virtualbox (https://www.virtualbox.org).
1) Изучаем полученный Vagrantfile
пример 1
```
Vagrant.configure(2) do |config|
    config.vm.define "vm-1" do |subconfig|
        subconfig.vm.box = "centos/7" subconfig.vm.hostname="vm-1"
        subconfig.vm.network :private_network, ip: "192.168.50.11" 
        subconfig.vm.provider "virtualbox" do |vb|
            vb.memory = "1024"
            vb.cpus = "1" 
         end
    end
    config.vm.define "vm-2" do |subconfig|
        subconfig.vm.box = "centos/7" subconfig.vm.hostname="vm-2"
        subconfig.vm.network :private_network, ip: "192.168.50.12" 
        subconfig.vm.provider "virtualbox" do |vb|
            vb.memory = "1024"
            vb.cpus = "1" 
        end
    end
    config.ssh.insert_key = false
    config.ssh.private_key_path = ['~/.vagrant.d/insecure_private_key', '~/.ssh/id_rsa'] 
    config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/authorized_keys"
end
```
команды для работы с вагрантом
- запуск 
``` vagrant up ```
- запуск с провиженингом
``` vagrant up --provision ```
- запуск провиженинга на запущеном стэнде
``` vagrant provision  ```
- удаление стэнда
``` vagrant desroy -f ```

# Обновить ядро на 5e
```bash
uname -mrs
wget https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
gpg --quiet --with-fingerprint RPM-GPG-KEY-elrepo.org 
rpm --import RPM-GPG-KEY-elrepo.org

wget http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
yum install elrepo-release-7.0-2.el7.elrepo.noarch.rpm
yum list available --disablerepo='*' --enablerepo=elrepo-kernel
yum --disablerepo='*' --enablerepo=elrepo-kernel install kernel-lt
```

# Команды для работы  с модулями ядра и не только
```bash
lsmod
modprobe
rmmod
modinfo module_name
systool -v -m module_name
# директория с конфигами модулей
/etc/modules-load.d/

sysctl -a
cat /etc/sysctl.conf

```
смотрим описание настроек в https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt

# Загрузка и сборка собственнного ядра
```bash
yum update
yum install -y ncurses-devel make gcc bc bison flex elfutils-libelf-devel openssl-devel grub2 bc flex

cd /usr/src/
wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.20.5.tar.xz
tar -xvf linux-4.20.5.tar.xz

cd linux-4.20.5
cp /boot/config-3.10.0-957.1.3.el7.x86_64 .config

make oldconfig
make menuconfig

make -j bzImage

make -j modules
make -j
make -j install
make -j modules_install

dracut --regenerate-all --fstab --force --verbose

grub2-mkconfig | grep 4.20
grub2-set-default 'CentOS Linux (4.20.5) 7 (Core)'
```


# Попасть в систему без пароля
В конце строки, начинающейся с linux16:
1) Можно дописать ``` init=/bin/bash ``` и система загрузится в режиме readonly. 
Перемонтируем систему в режим чтения/записи ``` mount -o remount,rw / ```
2) дописать ``` rw init=/sysroot/bin/sh ``` и загрузиться в режиме чтения/записи.
3) добавить rd.break
```bash

[root@linux ~]# mount -o remount,rw /sysroot 
[root@linux ~]# chroot /sysroot 
[root@linux ~]# passwd root
[root@linux ~]# touch /.autorelabel
```


# Переименуем том LVM и попробуем загрузиться
```bash
# vgrename VolGroup00 MAIRoot

```

# Починим сломанную систему
```bash
sed -i 's/VolGroup00/MAIRoot/g' /etc/fstab
sed -i 's/VolGroup00/MAIRoot/g' /boot/grub2/grub.cfg 
sed -i 's/VolGroup00/MAIRoot/g' /etc/default/grub
dracut -f -v
```