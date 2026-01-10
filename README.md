# Telegram bot for tagging all persons in chat

## How to set up the bot?
1) Create virtual environment with `python -m venv .venv` command (write command in the terminal);
2) Execute command `.venv/Scripts/activate` (on Windows) or `.venv/bin/activate`* (on Linux);
3) Install libraries with `pip install -r requirements.txt` command;
4) Create settings.json file in settings directory;
5) Register on site https://my.telegram.org/auth. Get the **API ID** and **API HASH** values;
6) Get the Bot token from [@BotFather](https://t.me/botfather);
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

## How to Add Resources?
### String Resources
1) Open the file `resources/strings/strings.json` (or the file `resources/strings/logger_strings.json` 
if the string is intended for the logger);
2) Add your string resource to the file in the format `"key": "value"`. 
Any value can be used as the key, but it is advisable for it to reflect what is written in the string resource. 
Copy the key;
3) Open the file `models/pydantic_models/strings_model.py`;
4) Add a new field to the class `StringsModel` (or to the class `LoggerStringsModel` if the resource is intended for 
the logger) in the following format:
```python
field_name: str = Field(alias='paste_the_copied_key_here', frozen=True)
```
5) Now the string resource can be used in the code :)  
P.S. To get the model with string resources, use the method `ResourceHandler.get_strings_resources` 
(for logger resources, use the method `ResourceHandler.get_logger_strings_resources()`)

### Images
1) Add an image to the `resources/images` directory. Copy the image file name;
2) Open the file `resources/resource_handler.py`;
3) Find the class `Images` in the file. Add a field with the image file name to it;
4) Now the image can be used in the code :)  
P.S. To get the file for sending in a message, use the method `ResourceHandler.get_image_file()`

### Stickers
1) Open the file `resources/stickers.json`;
2) Add a sticker to the file in the format `"key": "value"`. The value is the sticker ID in Telegram. 
You can find out the sticker ID using special bots in Telegram itself, for example [@idstickerbot](https://t.me/idstickerbot). 
Use any key, but preferably one that reflects what is depicted on the sticker. Copy the key;
3) Open the file `models/pydantic_models/stickers_model.py`;
4) Add a new field to the class `StickersModel` in the following format:
```python
field_name: str = Field(alias='paste_the_copied_key_here', frozen=True)
```
5) Now the sticker can be used in the code :)  
P.S. To get the model with sticker data, use the method `ResourceHandler.get_stickers_resources()`

Bot was created on `Python 3.12.4` but I guess it should work on lower versions either.

---

# Телеграм бот для тега всех пользователей чата (аналог команды @all во ВКонтакте)

Для работы необходимо создать собственного бота через [@BotFather](https://t.me/BotFather)

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

## Как добавлять ресурсы?
### Строковые ресурсы
1) Откройте файл `resources/strings/strings.json` (или файл `resources/strings/logger_strings.json`, если строковый
предназначен для логгера);
2) Добавьте в файл ваш строковый ресурс в формате `"ключ": "значение"`. В качестве ключа можно использовать 
любое значение, но желательно, чтобы он отображал то, что написано в строковом ресурсе. Скопируйте ключ;
3) Откройте файл `models/pydantic_models/strings_model.py`;
4) Добавьте в класс `StringsModel` (или в класс `LoggerStringsModel`, если ресурс предназначен для логгера) новое поле
в следующем формате: 
```python
имя_поля: str = Field(alias='сюда_скопированный_ключ', frozen=True)
```
5) Теперь строковым ресурсом можно пользоваться в коде :)  
P.S. Для получения модели со строковыми ресурсами используйте метод ResourceHandler.get_strings_resources
   (для ресурсов логгера используйте метод ResourceHandler.get_logger_strings_resources())

### Изображения
1) Добавьте в директорию `resources/images` изображение. Скопируйте имя файла изображения;
2) Откройте файл `resources/resource_handler.py`;
3) Найдите в файле класс Images. Добавьте в него поле с названием файла изображения;
4) Теперь изображение можно использовать в коде :)  
P.S. Для получения файла для отправки в сообщении используйте метод ResourceHandler.get_image_file()


### Стикеры
1) Откройте файл `resources/stickers.json`;
2) Добавьте в файл стикер в формате `"ключ": "значение"`. В качестве значения используется ID стикера в телеграмм.
Узнать ID стикера можно при помощи специальных ботов в самом Телеграмме, например 
[@idstickerbot](https://t.me/idstickerbot). Ключ используйте любой, но желательно, чтобы он отображал, что изображено
на стикере. Скопируйте ключ;
3) Откройте файл `models/pydantic_models/stickers_model.py`;
4) Добавьте в класс `StickersModel` новое поле в следующем формате:
```python
имя_поля: str = Field(alias='сюда_скопированный ключ', frozen=True)
```
5) Теперь стикером можно пользваться в коде :)  
P.S. Для получения модели с данными по стикерам используйте метод ResourceHandler.get_stickers_resources()

Написан на `Python 3.12.4`, но на ранних версиях, наверное, тоже будет работать.
