Telegram bot for tagging all persons in chat

How to set up the bot?
1) Create virtual environment with python -m venv .venv command (write command in the terminal);
2) Execute command .venv/Scripts/activate (on Windows) or .venv/bin/activate (on Linux);
3) Install libraries with pip install -r requirement.txt command;
4) Create settings.json file in settings directory;
5) Register on site https://my.telegram.org/auth. Get the API ID and API HASH values;
6) Get the Bot token from t.me/botfather;
7) Copy this in your settings.json file. Replace words in quotation marks with your values:
{
   "API_HASH": "your api_hash value here",
   "API_ID": your api_id value here,
   "TOKEN": "your bot token here"
}
8) Add your bot to the group;
9) Run bot.py file


At the forst launch you will be asked for ypur number. It is necessary to start your user bot.
Don't forget to give admin rights to bot

To tag users use command /all ot just tag the bot

Bot was created on Python 3.12.4 but I guess it should work on lower versions either.

-----------------------------------------------
Телеграм бот для тега всех пользователей чата (аналог команды @all во ВКонтакте)

Для работы необходимо создать собственного бота через @BotFather

Как поставить бота?
1) Создайте виртуальную среду при помощи команды python -m venv .venv (команду пишем в командной строке);
2) Выполните команду .venv/Scripts/activate (на Windows) или .venv/bin/activate (на Linux);
3) Установите необходимые библиотеки при помощи команды pip install -r requirement.txt;
4) Создайте файл settings.json в папке settings;
5) Зарегистрируйтесь на сайте https://my.telegram.org/auth. Сохраните API ID и API HASH;
6) Получите токен вашего бота у BotFather;
7) Скопируйте слудующие строчки в файл settings.json. Замените значения в кавычках на ваши значения (значение API_ID не должно быть в кавычках!!!):
{
   "API_HASH": "ваш  API HASH",
   "API_ID": ваш APi ID,
   "TOKEN": "токен вашего бота"
}
8) Добавьте бота в ваш чат;
9) Запустите файл bot.py.

При первом запуске попросят ввести ваш номер телефона. Это нормально, это нужно для регистрации юзер бота от вашего имени (иначе нельзя получить список пользователей в чате)
Не забудьте выдать боту права администратора.

Чтобы отметить всех пользователей используйте команду /all или просто отметьте вашего бота

Написан на Python 3.12.4, но на ранних версиях, наверное, тоже будет работать.
