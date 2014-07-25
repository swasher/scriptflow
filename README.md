### Scriptflow

Скрипт для автоматической отправки PDF файлов на фотовывод.

### inotify и incrontab

Список пользователей, которые могут запускать incrontab, находится в `/etc/incron.allow`. Добавляем туда юзера, 
от которого работаем.

Запуск скрипта осуществляется через inotify, с применением incrontab:

    $ incrontab -e
    add string
    /home/<user>/scriptflow/input IN_CLOSE_WRITE /home/<user>/scriptflow/flow.sh $#   
    
incrontab следит за директорией input, и в случае изиенений в ней запускает скрипт flow.sh.
Последний является оберткой для flow.py. Обертка предназначена для возможности наблюдения за работой
фонового скрипта через терминал /dev/tty1 (удобно например для vmware viewer).



    
    