# vk2tg_bot
Простой бот, который будет отправлять вам новые записи со стены группы Вконтакте вам в Telegram (в чат или ЛС).
На данный момент бот не умеет отправлять ничего, кроме текста в посте. (Просто автору это не нужно)

## Как это работает? 
0. Бот подключается к ВК, используя ваш логин и пароль.
1. Каждые 10 минут бот проверяет наличие новых записей в группе, которую вы указали в конфиге.
2. Если есть посты, у которых `id` больше, чем в переменной `vk_last_post_id` (в config.yaml), то собирает их.
3. Отправляет новые посты на стене Вконтакте в чат/ЛС в Telegram. 

## В каком формате он отправляет сообщения?
| Простой пост | Репост с комментарием |
|:----|:----|
| Некоторый текст сообщения,<br/>чтобы это было просто видно<br/><br/>*Вася Пупкин*<br/>31-12-2000 09:41 | Некоторый текст сообщения,<br/>чтобы это было просто видно<br/><br/>*reply ->*<br/>**Автор оригинального поста**<br/>Оригинальный текст от автора<br/>оригинального поста<br/><br/>Вася Пупкин<br/>31-12-2000 09:41 |

При этом бот не отправляет ничего, кроме текста.
Дата поста так же является ссылкой на пост Вконтакте.

## Как установить?
0. В удобном для вас месте выполнить `git clone https://github.com/Timofffee/vk2tg_bot.git`

1. `cd vk2tg_bot`

2.1. (Только Linux) Для автоматической установки всех зависимостей и добавления демона в systemd: `sh install.sh`

2.2. (Для любой ОС) Выполнить `pip3 -r requirements.txt` для установки необходимых модулей и воспользоваться командой `python3 vk2tg.py` для запуска бота. 

3. Done!


**ВНИМАНИЕ!!**

Обязательно заполните все поля в `config.yaml` перед запуском! 
Значение `vk_group_id` обязательно должно быть отрицательным.
