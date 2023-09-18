<i>Ридми на русском — внизу.</i>

# Todolist API

This was a final project from the Python course. 

<p><b>Technologies:</b> Django, Telegram Bot API, Docker. </p>

<p><b>To launch:</b>

Download the folder to your computer, fill in the example.env file and rename it into .env.
In the terminal, from the root folder run the following commands:

`pip install -r requirements.txt`
`python3 todolist/manage.py migrate`
`python3 todolist/manage.py runserver`

To run the telegram bot, while running the app, run:

`python3 todolist/manage.py runbot`

## Main viewpoints

You can see all of the app's viewpoints documented in the Swagger ui at host:port/schema/swagger-ui/ when the app runs in the development mode (Debug=True in .env).

### User Authentication

For token authentication:

<b>api/token/</b> — POST, use to get a pair of tokens, requires a username and a password.
<b>api/token/refresh/</b> - POST, use to get a new token, requires a refresh token from the previously issued pair.

The rest are under the api/core/ path:

<b>core/register</b> - POST, use to create a user. Requires a username and a password.

The creation of a goal requires an existing category and the creation of the category requires an existing board, so the api automatically creates a board named "My board" and a category named "My goals" for every new user.

The rest are the standart CRUD views for the authenticated users:

<b>core/update/uid/</b> PUT/PATCH
<b>core/profile/uid/</b> GET
<b>core/delete/uid/</b> DELETE

Users can only view/change/delete their own account.

### Goals functionality

All viewpoints under the api/goals/ path (can be viewed by authenticated users only):

<b>board/ viewpoints:</b>

<b>board/create/</b> POST, use to create a new board.
<b>board/id/</b> GET, PUT, PATCH, DELETE — use to edit an existing board, the queryset is limited by the boards you have access to as a board participant (for viewing) or as an owner (for editing/deleting). Through the put method you can add and delte board participants for the boards you own, as well as change their roles on the board. To do that, along with the board title send a "boardparticipants" field with a list of dictionaries like this: {"user": id, "role": int}.

Only the board's owner can change or delete it. But the other board participnts can hawe one of two roles:

- An <b>Editor</b> can create new categories and goals and comment the goals on the board.
- A <b>Reader</b> can view categories, goals and comments on the board.

If the board is deleted, it remains in the database with the deleted status. All categories on the board are marked as delted as well, and all goals in those categories are marked as archived.

<b>goal_category/</b> viewpoints:

<b>goal_category/create/</b> POST, creates a new category, requires a title for the new category ("title") and the id of the board ("board") to host the category on.
<b>goal_category/id/</b> GET, PUT, PATCH, DELETE for the category by id, only the owner can change/delete categories.

If the category is deleted, it remains in the database with the deleted status. All goals in that category are marked as archived.

<b>goal/</b> viewpoints:

<b>goal/create/</b> POST, creates a goal, requires a title for the new goal ("title") and the id of the category to put the goal in ("category").
<b>goal/id/</b> GET, PUT, PATCH, DELETE for the goal by id, only the owner can change/delete goals.

Goals can have four statuses: "To Do", "In progress", "Done" and "Archived". User can also set the priority for the goal: "Low", "Medium", "High" or "Critical".

When deleted, goals remain in the database with the "Archived" status.

<b>goal_comment/</b> viewpoints:

<b>goal_comment/create/</b> POST, creates a comment, requires a text of the comment ("text") and the id of the goal ("goal").
<b>goal_comment/id/</b> GET, PUT, PATCH, DELETE for the comment by id, only the owner can change/delete comments.

### Telegram bot functionality

If user wants to use the Telegram bot, they have to be registered in the main api and exist in the database. When the user texts the bot for the first time, the bot sends them a code to then send to the <b>bot/verify/</b> endpoint with a POST method (in the "verification_code" field). After they have done that, the api ties the tguser to the user in the database and the user can get a list of their active goals with <b>/goals</b> command, or create new goals with <b>/create_goal</b> command (the goal creation process can be stopped with the <b>/stop</b> command).
The <b>/start</b> command returns a hint with the possible commands for the bot. If the user did not send the verification code to the api, the bot will not accept commands, it will continue to ask the user to send thecode to the api.

## Challenges

### Permissions

It was difficult at first to keep track of varying permissions for different roles on the board, but it got much easier to handle with the inheritance structure. I decided to leave each type of object create permission as their own class so they would be easy to change in the future. Main object permissions still have a lot of same code, I didn't manage to organize them better yet.

### The preservation of the user's status while creating the goal via the bot

I had to figure out how can I recognize that the telegram user have initiated a goal creation process, because I needed to take their responses to pick a board and a category for the new goal. I also had to store this data somehow, while the process of creation goes. The best decision I managed to come up with so far was to store the info on the process in the database (as a separate TgUser field "goal_creating_status" with 5 possible statuses) as well as the info for the new goal (as an instance of a separate model tied to TgUser, TgUserGoal). After the process of creation of the new goal has been completed or stopped, the TgUserGoal instance is deleted from the database, and TgUser's goal_creating_status is set back to 0.
The code I came up is rather cumbersome, but it's still the best implementation I could come up with.

<i>Here starts the Readme in Russian.</i>

# API для списка дел

Это был финальный проект курса по Python.

<p><b>Технологии:</b> Django, Telegram Bot API, Docker. </p>

<p><b>Чтобы запустить:</b>

Скопируйте репозиторий на компьютер, заполните файл example.env и переименуйте его в .env.
В терминале, из корневой папки проекта введите команды:

`pip install -r requirements.txt`
`python3 todolist/manage.py migrate`
`python3 todolist/manage.py runserver`

Чтобы запустить бота, когда приложение запущено, в новом окне терминала введите:

`python3 todolist/manage.py runbot`

## Главные адреса

Документация по всем адресам api доступна в Swagger ui по адресу host:port/schema/swagger-ui/, когда приложение запущено в режиме разработки (Debug=True в .env).

### Аутентификация пользователей

Для аутентификации с помощью токена:

<b>api/token/</b> — POST, возвращает пару токенов в ответ на логин и пароль (поля "username", "password").
<b>api/token/refresh/</b> - POST, возвращает новую пару токенов взамен на refresh токен из ранее выданной пары.

Остальное — по адресу api/core/:

<b>core/register</b> - POST, создает пользователя. Требует логин и пароль (поля "username" и "password").

Для создания цели нужно, чтобы уже существовала категория, а для создания категории нужно, чтобы у пользователя уже была доска для целей. Поэтому api автоматически создает каждому новосу пользователю доску "My board", а на ней — категорию "My goals".

Остальные адреса — стандартный CRUD пользователей:

<b>core/update/uid/</b> PUT/PATCH
<b>core/profile/uid/</b> GET
<b>core/delete/uid/</b> DELETE

Пользователи могут просматривать/изменять/удалять только свой аккаунт.

### Функуиональность целей

Все адреса по пути api/goals/ (могут просматривать только аутентифицированные пользователи):

Адреса <b>board/:</b>

<b>board/create/</b> POST, создает доску.
<b>board/id/</b> GET, PUT, PATCH, DELETE — редактирвоание/удаление доски, выдача объектов из базы ограничена досками, с которыми пользователь связан как участник(просмотр) или как владелец(изменение/удаление). Через метод put можно изменять список участников на своих досках и менять их роли. Для этого вместе с новыйм названием (поле "title") нужно отправить поле "boardparticipants" со списком словарей по образцу: {"user": id, "role": int}.

Только хозяин доски может изменять или удалять ее. Но у участников досок могут быть еще две роли:

- <b>Редактор (Editor)</b> может создавать новые категории и цели, а также комментировать цели на доске.
- <b>Читатель (Reader)</b> может просматривать категории, цели и комментарии на доске.

Удаленная доска остается в базе со статусом "удалена". Все категории на доске также помечаются как удаленные, а целям в этих категориях присваетвается статус "в архиве".

Адреса <b>goal_category/</b>:

<b>goal_category/create/</b> POST, создает категорию, требует название ("title") и id доски ("board"), на которой следует разместить категорию.
<b>goal_category/id/</b> GET, PUT, PATCH, DELETE для категории по id, только владелец может изменять/удалять категории.

Удаленные категории остаеются в базе данных и помечаются как удаленные, а целям в этих категориях присваетвается статус "в архиве".

Адреса <b>goal/</b>:

<b>goal/create/</b> POST, создает цель, требует название ("title") и id категории, в котороую отпарвить цель ("category").
<b>goal/id/</b> GET, PUT, PATCH, DELETE для цели по id, только владелец может изменять/удалять цели.

У целий могут быть четыре статуса: "Сделать" ("To Do"), "В процессе" ("In progress"), "Готово" ("Done") и "В архиве" ("Archived"). Также пользователь может выставить цели приоритет: "Низкий" ("Low"), "Средний" ("Medium"), "Высокий" ("High") или "Критический" ("Critical").

Удаленный цели остаются в базе данных со статусом "В архиве".

Адреса <b>goal_comment/</b>:

<b>goal_comment/create/</b> POST, создает комментарий, требует текст комментария ("text") и id цели, к которой прикрепить комментарий ("goal").
<b>goal_comment/id/</b> GET, PUT, PATCH, DELETE для комментария по id, только владелец может изменять/удалять комментарии.

### Функциональность Telegram-бота

Пользователю, который хочет воспользоваться ботом, нужно быть зарегистрирвоанным в api и присутствовать в базе данных. Когда пользователь пишет первое сообщение боту, он получает код, который нужно отправить методом POST на адре api <b>bot/verify/</b> (в поле "verification_code"). После того, как пользователь это сделал, api привязывает его объект tguser к объекту user в базе данных, и пользователь может получить список активных целей с помощью команды <b>/goals</b> или создать новые цели с помощью команды <b>/create_goal</b> (остановить создание цели можно командой <b>/stop</b>). Команда <b>/start</b> выдает подсказку с возможными командами для бота. Если пользователь не отправил код подтверждения в api, бот не будет принимать команды, он будет продолжать просить отправить код в api.

## Трудности

### Разрешения

Поначалу было трудно уследить за разрешениями для ролей на досках, но со структурой наследования и классами разрешений их получилось более-менее упорядочить. Я решила оставить отдельный класс для каждого разрешения для создания объекта, чтобы в будущем их было легко изменять. Основные разрешения для объектов все еще содержат повторяющийся когд, мне пока не удалось организовать их лучше.

### Хранение статуса пользователя в процессе создания цели через бота

Мне нужно было разобраться, как я могу знать 6что пользователь бота начал создавать новую цель, потому что из его ответов мне нужно было получать имя доски и категории для новой цели, и название новой цели. Также эти ответы надо было как-то хранить, пока процесс создания цели продолжается. Лучшее решение, которое я придумала на нынешний момент — хранить информацию о процессе в базе данных (как отдельное поле модели TgUser, "goal_creating_status", с пятью возможными значениями, 0 по умолчанию и от 1 до 4 для каждого шага создания цели), и о новой цели тоже (как об объекте модели TgUserGoal, привязанной к TgUser). Когда процесс создания новой цели завершается или остановлен пользователем, объект TgUserGoal удаляется из базы, а значение goal_creating_status для TgUser снова принимает значение 0.
Решение получилось громоздким, но лучше я пока не придумала.