# Telegram bot for tagging all persons in chat

## How to set up the bot?
1) Create virtual environment with `python -m venv .venv` command (write command in the terminal);
2) Execute command `.venv/Scripts/activate` (on Windows) or `.venv/bin/activate`* (on Linux);
3) Install libraries with `pip install -r requirements.txt` command;
4) Create settings.json file in settings directory;
5) Register on site https://my.telegram.org/auth. Get the **API ID** and **API HASH** values;
6) Get the Bot token from [@BotFather](t.me/botfather);
7) Copy this in your settings.json file. Replace values in file with yours:
```json
{
   "API_HASH": "your API HASH value here",
   "API_ID": "your API ID here (delete quotes in this line)",
   "TOKEN": "your bot token here"
}
```
8) Add your bot to the group;
9) Run `start_bot.py` file

> [!IMPORTANT]
> Don't forget to give admin rights to bot

\* - In some situations on Linux this command may do nothing. If so, write path to pip for installing libraries on
step 3 (`.venv/bin/pip install -r requirements.txt`)

## Available commands
1) `/all` (or @prostoTagAllBot) - mention all users in chat;
2) `/spam <amount> <message>` - repeat \<message\> \<amount\> times. Command will split text into several messages if  
final text is too big. Don't use too often, your friends won't be happy :)
3) `/react <emoji>` - set reaction on a message with \<emoji\>. \<emoji\> must be allowed to use. For use reply 
the message with this command. 

Bot was created on `Python 3.12.4` but I guess it should work on lower versions either.

---

# Телеграм бот для тега всех пользователей чата (аналог команды @all во ВКонтакте)

Для работы необходимо создать собственного бота через [@BotFather](t.me/BotFather)

## Как настроить бота?
1) Создайте виртуальную среду при помощи команды `python -m venv .venv` (команду пишем в командной строке);
2) Выполните команду `.venv/Scripts/activate` (на Windows) или `.venv/bin/activate`* (на Linux);
3) Установите необходимые библиотеки при помощи команды `pip install -r requirements.txt`;
4) Создайте файл settings.json в папке settings;
5) Зарегистрируйтесь на сайте https://my.telegram.org/auth. Сохраните **API ID** и **API HASH**;
6) Получите токен вашего бота у [@BotFather](t.me/BotFather);
7) Скопируйте следующие строчки в файл settings.json. Замените значения из файла на ваши значения:
```json
{
   "API_HASH": "ваш  API HASH",
   "API_ID": "ваш API ID (удалите кавычки)",
   "TOKEN": "токен вашего бота"
}
```
8) Добавьте бота в ваш чат;
9) Запустите файл `start_bot.py`.

> [!IMPORTANT]
> Не забудьте выдать боту права администратора.

\* - На Linux может быть такое, что использование команды ничего не даст. Тогда при установке библиотек (на шаге 3) надо
прописать путь до pip целиком (`.venv/bin/pip install -r requirements.txt`)

## Доступные команды
1) `/all` (или @prostoTagAllBot) - отметить всех пользователей в чате;
2) `/spam <amount> <message>` - повторить фразу \<message\> \<amount\> раз. Если итоговый текст получится слишком 
большим, он будет разделён на несколько сообщений. Не используйте слишком часто, друзья рады не будут :)
3) `/react <emoji>` - поставить реакцию на сообщение. Реакция должна быть разрешена в чате. Чтобы поставить реакцию,
ответьте на сообщение этой командой

Написан на `Python 3.12.4`, но на ранних версиях, наверное, тоже будет работать.
