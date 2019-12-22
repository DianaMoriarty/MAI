 # BASH - bourne again shell
 ## Shells
 * sh
 * bash
 * zsh
    * https://github.com/robbyrussell/oh-my-zsh
 * fish
    * https://github.com/robbyrussell/oh-my-zsh
 
 ## Базовые команды
 - работа с файлами
    - ls, touch, vi, cat, less, more, find, rm
 - работа с диреториями
    - mkdir, pwd, cd
 - работа с правами
    - chmod, chown, id, chgrp
 - работа с процессами
    - ps, top
 - получение прав суперпользователя
   -  sudo, su
    
 ## Скрипты выполняющиеся при запуске
 *  login shell
    * /etc/profile
    * /etc/profile.d/[files]
    * ~/.bash_profile
 * non-login shell
    * ~/.bashrc
 
 ## Встроенная документация и помощь
 * help - помощь по встроенным командам
 * man - установленная документация по программам
 * apropos - поиск нужной документации
 * info - встроенная документация 
 * type - информация о введенной команде
 
 ## She-bang
```
#!/usr/bin/env VAR=VALUE bash ● #!/bin/bash
#!/bin/python
#!/bin/perl 
 ```
 
 ## Варианты запуска скриптов и программ
 - ./script.sh (необходим chmod +x) 
 - bash script.sh
 - source script.sh
 
 ## Return code
 * возвращается во внутреннюю переменную ```$?```
 * 0 - success
 * 1-255  - Fail
 
 ## Операторы списка
 - ```command1; command2``` - в􏰄ыполн􏰀ет перву􏰁ю, затем втору􏰁 команд􏰄
 - ```command1 & command2``` - в􏰄ыполн􏰀ет перву􏰁ю в фоновом режиме и
одновременно в􏰄полн􏰀ет втору􏰁
 - ```command1 && command2``` - в􏰄ыполн􏰀ет перву􏰁ю 􏰁, и затем в􏰄полн􏰀ет втору􏰁,
тол􏰃ко в случае если 1-а􏰀 вернула статус 0(завершилас􏰃 успешно)
 - ```command1 || command2``` - в􏰄ыполн􏰀ет перву􏰁ю , и затем в􏰄полн􏰀ет втору􏰁
тол􏰃ко в случае если 1-а􏰀 вернула не 0 статус (завершилас􏰃 неудачно)

## Переменные и параметры
 - export var=value
 - var=value
 - var1= val
 - declare var=value
 - var=`ls`
 - var=$(uname -r)
 - var=$((2+3))
 - var=$(expr 3 + 7)
 - var1="${var1:-default value}"
 
```
echo $var
echo ${var}
echo “$var”
echo ‘$var’
echo `$var`
echo $($var)
echo var
```

## Environment
```bash
env
printenv
export 
declare
```
## Встроенные переменные

- ```$@``` — параметр􏰄 скрипта (столбик)
- ```$*``` - все параметр􏰄 скрипта (строка)
- ```$0``` — им􏰀я скрипта
- ```$1 , $2 , $3 , ...``` — параметр􏰄 скрипта, по одному
- ```$#``` — количество параметров
- ```$?```-  статус завершения последеней команды
- ```$$``` — PID оболочки
- ```$!``` PID последней в􏰄полненной в фоновом режиме команд􏰄

## Массивы
```bash
files = $(ls) - счит􏰄ваетс􏰀 строка
array=('first element' 'second element' 'third element')
array=([3]='fourth element' [4]='fifth element')
array[0]='first element'
array[1]='second element'
echo ${array[2]}
IFS=$'\n'; echo "${array[*]}"
declare -A array
array[first]='First element'
array[second]='Second element'
array=(0 1 2)
```

## Условния
- if EXPR ; then команд􏰄 ; fi
- if EXPR ; then команд􏰄 ; else другие команд􏰄 ; fi
- if EXPR ; then команд􏰄; elif EXPR ; then команд􏰄; else другие команд􏰄 ; fi
```
test
if [ "$answer" = y -o "$answer" = yes ] 
if [[ $answer =~ ^y(es)?$ ]]
```

## CASE
```bash
 case EXPR in
CASE1) команд􏰄
;& # отработат􏰃 следу􏰁щие команд􏰄 без проверки CASE2) команд􏰄
;;& # в􏰄полнит􏰃 следу􏰁щу􏰁 проверку
...
CASEN) команд􏰄
;; # закончит􏰃 на 􏰂том
esac
```

## Сравнения
```bash
-z # строка пуста
-n # строка не пуста
=, (==) # строки равн􏰄
!= # строки не равн􏰄
-eq # равно
-ne # не равно
-lt,(< ) # мен􏰃ше
-le,(<=) # мен􏰃ше или равно
-gt,(>) # бол􏰃ше
-ge,(>=) # бол􏰃ше или равно
! # отрицание логического в􏰄ражени􏰀 ● -a,(&&) # логическое «И»
-o,(||) # логическое «ИЛИ»
``` 

##  Файловые проверки
```bash
[ -e FILE ] — файл существует
[ -d FILE ] — 􏰂это директори􏰀
[ -f FILE ] — 􏰂обычный файл
[ -s FILE ] — ненулевой размер
[ -r FILE ] — доступен для􏰀 чтени􏰀я
[ -w FILE ] — доступен дл􏰀я записи 
[ -x FILE ] — исполняемый
```

##  Циклы
смотримы примеры loop[X].sh

# Перенаправления
```bash
$ ls -l /dev/std*
lrwxrwxrwx. 1 root root 15 май 10 15:01 /dev/stderr -> /proc/self/fd/2 
lrwxrwxrwx. 1 root root 15 май 10 15:01 /dev/stdin -> /proc/self/fd/0
lrwxrwxrwx. 1 root root 15 май 10 15:01 /dev/stdout -> /proc/self/fd/1
$ echo 'hello' > /dev/null 2>&1
$ echo 'hello' &> /dev/null (сокращенна􏰀 форма с версии >= 4.0) 
$ ls -l | grep ".log"
$ mkfifo myPipe
$ ls -l > myPipe
$grep ".log" < myPipe
```

```bash
exec 3</dev/tcp/www.google.com/80 printf ‘GET /HTTP/1.0\r\n\r\n’ >&3
cat <&3
err(){
echo "E: $*" >>/dev/stderr
}
err "My error message"
{
echo "contents of home directory" ls ~ }
> output.txt
```

<< - HERE TEXT
```bash
wc -l << EOF Ssss
Sdsd
Sdsd
EOF
```

<<< - HERE STRING
```bash
$ read first second <<< "hello world" 
$ echo $second $first
```

<<< - HERE DOC
```bash
cat << EOF > myscript.sh #!/bin/bash
echo “Hello Linux!!!”
exit 0
EOF
```

## Traps
```bash
if ( set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null; 
then
  trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT KILL 
  while true
  do
    ls -ld ${lockfile}
    sleep 1 
  done
  rm -f "$lockfile"
  trap - INT TERM EXIT 
else
  echo "Failed to acquire lockfile: $lockfile."
 echo "Held by $(cat $lockfile)" 
fi
```

##  Регулярные выражения
```
 ^([a-zA-Z0-9_\-\.\+]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$
```
BRE
- ^ - начало строки
- $ - конец строки
- . - любой символ
- \ - 􏰂экранирование символа
- [A-Z] - диапазон􏰄 перечислени􏰀 
- [xyz] - любой из перечисленных
- [^xyz] - исключение символов из поиска
- ```*``` - любое кол-во

ERE (perl/egrep/awk)

- {m,n} - скол􏰃ко раз может встретитс􏰀 символ от - до 
- {m} - точное кол-во встречаемости символа
- ? - символ может встретитс􏰀 0 или 1 раз
- \+ - л􏰁бое кол-во символов, но хот􏰀 б􏰄 1
- () - группировка символов 
- | - какой либо из символов
