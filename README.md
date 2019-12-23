## Посмотрим какие дисковые устройства и партиции есть в системе

```bash
lsblk
blkid
fdisk -l 
parted -l

```
* Какой размер дисков?
* Есть ли неразмеченное место на дисках?
* Какой размер партиций?
* Какая таблица партционирования используется?
* Какой диск, партция или лвм том смонтированы в /

![screenshot1](https://i.postimg.cc/mZ5vqW88/Capture.png)

![screenshot2](https://i.postimg.cc/hPFXB6G1/Capture.png)

![screenshot3](https://i.postimg.cc/L58N65DG/Capture.png)

**Один диск на 10 ГБ**  
Есть ли неразмеченное место на дисках? **Нет**  
Какой размер партиций? **part 10 GB**  
Какая таблица партционирования используется? **msdos**  
Какой диск, партция или лвм том смонтированы в /? **/dev/sda1**  

---

## Создадим сжатую файловую систему для чтения squashfs
```bash
git clone https://gitlab.com/erlong15/mai.git
mksquashfs mai/* mai.sqsh
sudo mkdir /mnt/mai
sudo mount mai.sqsh /mnt/mai -t squashfs -o loop
```

![screenshot4](https://i.postimg.cc/6q97RGG5/Capture.png)

---

## Посмотрим информацию по файловым системам смонтированным в системе

```bash
df -h
df -i
mount
```
* Какая файловая система примонтирована в /?  **/dev/sda1**
* С какими опциями примонтирована файловая система в /? **rw,relatime,errors=remount-ro**
* Какой размер файловой системы приментированной в /mnt/mai?  **128 KB**

![screenshot5](https://i.postimg.cc/vZ6m4vSt/Capture.png)

![screenshot6](https://i.postimg.cc/k5vqSYNK/Capture.png)

![screenshot7](https://i.postimg.cc/ZRNg3Wzg/Capture.png)

---

## Попробуем создать файлик в каталоге /dev/shm

```bash
dd if=/dev/zero of=/dev/shm/mai bs=1M count=100
free -h
rm -f /dev/shm/mai
free -h
```
![screenshot8](https://i.postimg.cc/MK3D6zhj/Capture.png)

* Что такое tmpfs? **временное файловое хранилище**
* какая часть памяти изменялась? **free - размер свободной памяти**

---

## Изучим процессы запущенные в системе

```bash
ps -eF
ps rx 
ps -e --forest
ps -efL
```

![screenshot9](https://i.postimg.cc/jjBqtnhk/Capture.png)

![screenshot10](https://i.postimg.cc/VNnp0S8h/Capture.png)

![screenshot11](https://i.postimg.cc/SsmTXDVX/Capture.png)

![screenshot12](https://i.postimg.cc/jSVhwMSs/Capture.png)

* Какие процессы в системе порождают дочерние процессы через fork? **gdm3, systemd, firefox**
* Какие процессы в системе являются мультитредовыми? **gdm3, gnome, firefox**

---

## Разберитесь что делает команда

```bash
ps axo rss | tail -n +2|paste -sd+ | bc
```

* Что подсчитывается этой командой
* Почему цифра такая странная

![screenshot13](https://i.postimg.cc/y8y73Yzv/Capture.png)

Команда подсчитывает количество занятой и не находящейся в swap оперативной памяти, использованное процессами всех пользователей.
Цифра странная, потому что она в килобайтах.

---

## Уставновим утилиту smem и проанализируем параметр PSS в ней
```bash
apt-get install smem -y
smem
```
![screenshot14](https://i.postimg.cc/5tXkdnpL/Capture.png)

* утилита работает какое то время, можно оставить ее в другом терминале

---

## Запустим приложеннный скрипт и понаблюдаем за процессами
```bash
python myfork.py
```
* в другом терминале  отследите порождение процессов
* отследите какие состояния вы видите у процессов. **Z - зомби процессы**
* почему появляются процессы со статусам Z. **потому что эти дочерние процессы завершаются раньше родительского**
* какой PID у основного процесса? **27671**
* убейте основной процесс ```kill -9 <pid>```
* какой PPID стал у первого чайлда **27672**
* насколько вы разобрались в скрипте и втом что он делает? **скрипт создает форки и некоторых отправляет в сон**

![screenshot14](https://i.postimg.cc/28pq46PD/Capture.png)

![screenshot14](https://i.postimg.cc/2jTk55rG/Capture.png)

---

## Научимся корректно завершать зомби процессы
* запустим еще раз наш процесс
* убьем процесс первого чайлда
* проверим его состояние  и убедимся что он зомби
* остановим основной процесс

![screenshot15](https://i.postimg.cc/4yrPbgp3/Capture.png)

![screenshot16](https://i.postimg.cc/6qGLQmFx/Capture.png)

* расскоментируем строки в скрипте
```python
      pid, status = os.waitpid(pid, 0)
      print("wait returned, pid = %d, status = %d" % (pid, status))
```

* поторим все еще раз
* отследим корректное завершение чайлда

![screenshot17](https://i.postimg.cc/yxBcV8hc/Capture.png)

---
## Научимся убивать зомби процессы
* запускаем процессс еще раз
```bash
gdb
> attach <parent_PID>
> call waitpid(zombie_PID, 0, 0) wait
> detach
> quit
```

![screenshot18](https://i.postimg.cc/8khxwXj0/Capture.png)

---
## Проблемы при отмонтировании директории
```bash
cd /mnt/mai
# в другом терминале
sudo umount /mnt/mai
fuser -v /mnt/dir
```
* Напишите какие процессы мешают размонтировать директорию? **Мешает bush**
* посмотрите ```lsof -p <pid>``` этих процессов
* убейте мешаюший процесс и размонтируйте директорию

![screenshot19](https://i.postimg.cc/Gh6Y2Kjb/Capture.png)

**Убираем этот процесс и размонтируем директорию.**

---

## Решаем загадку исчезновения места на диске
* создадим директорию ~/myfiles
* запустим файл test_write.py из ранее созданной директории
* проверим в другом терминале что в этой директории создался файл и он увеличивается в размере
* в первом терминали нажмем Ctrl+Z
* проверим статус файла


![screenshot19](https://i.postimg.cc/JhHRh3PC/Capture.png)

* выполним команды
```bash
jobs -l
fg
```
* eще раз остановим  процесс черерз CTRL+Z
* выполним команду ```bg```
* проверим размер файловой системы и каталога
```bash
df 
du -sh  ~/myfiles
```

![screenshot20](https://i.postimg.cc/R0dLNfFG/Capture.png)


* удалим файл
* повторно проверим размеры кталога и файловой системы

![screenshot21](https://i.postimg.cc/hvdmb7Sk/Capture.png)

* Какую систуацию вы видите, как вы это объясните
* Подключитесь к процессу через ```strace -p <pid>``` и назовите дескриптор файла, куда пишет процесс
* проверим какие файлы открыты у нашего процесса через команду lsof -p <pid>
* убьем процесс
* еще раз прорим размер файловой системы и каталога
* Напишите свое объяснение, что произошло. **Файл удалился только после закрытия файлового дескриптора**

---

## Утилиты наблюдения
* C помощью утилит мониторинга 
* проверьте текущий LA 

![screenshot24](https://i.postimg.cc/6564PbfQ/Capture.png)


* запишите top 3 процессов загружающих CPU

![screenshot22](https://i.postimg.cc/rFTNw9C6/Capture.png)

* запишите top 3 процессов загружающих память 

![screenshot23](https://i.postimg.cc/yN2F4hYb/Capture.png)

* запустите dd на генерацию файла размер в 3 гигабайта. 

**dd if=/dev/zero of=test.txt bs=1M count=3072**

![screenshot27](https://i.postimg.cc/y6r8y9yJ/Capture.png)

* удалите сгенеренный файл
* через atop скажите какой  pid был у процесса? **PID процесса 3489**
* Проанализируйте нагрузку на диск через утилиты  iotop и iostat

![screenshot25](https://i.postimg.cc/hGGBWx3T/Capture.png)

![screenshot26](https://i.postimg.cc/MKwgJVnH/Capture.png)
