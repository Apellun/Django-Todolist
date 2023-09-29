<i>Ридми на русском — внизу.</i>

# Todolist API

This was a final project from the Python course. It is a Django API that allows users to create goals, and also categories and boards for goals. Users can invite other users to their boards and give them one of two roles: reader or editor.
Users also can view their goals and create new goals with a Telegram bot.

<p><b>Technologies:</b> Django, Telegram Bot API, Docker. </p>

<i>Note: The requirements.txt file is so extensive because while recently updating Django I encountered an error while launching the API. So just in case I have updated all of the packages and put them all into requirements, to make sure that the API runs correctly.</i>

<p><b>To launch:</b>

Download the repository to your computer, fill in the example.env file and rename it into .env.
In the terminal, from the root folder of the repository run the following commands:

`pip install -r requirements.txt`
`python3 todolist/manage.py migrate`
`python3 todolist/manage.py runserver`

To run the telegram bot (run the API first), in the separate terminal, from the root folder of the repository run:

`python3 todolist/manage.py runbot`

## Main endpoints

You can see all of the API's viewpoints documented in the Swagger UI at host:port/schema/swagger-ui/ when the API is running in the development mode (Debug=True in .env).

### User Authentication

For token authentication:

<b>api/token/</b> — POST, returns a pair of tokens, requires a username and a password.
<b>api/token/refresh/</b> - POST, returns a new pair of tokens, requires a refresh token from the previously issued pair.

The CRUD for the user is under the api/core/ path:

<b>core/register</b> - POST, creates a user, requires a username and a password.

<i>The creation of a goal requires an existing category and the creation of the category requires an existing board, so the API automatically creates a board named "My board" and a category named "My goals" for every new user.</i>

<b>core/update/uid/</b> PUT/PATCH
<b>core/profile/uid/</b> GET
<b>core/delete/uid/</b> DELETE

Users can only view/change/delete their own account.

### Goals functionality

All viewpoints for the functionality considering goals are under the api/goals/ path (can be viewed by authenticated users only):

<b>board/ endpoints:</b>

<b>board/create/</b> POST, use to create a new board, requires a title ("title").
<b>board/id/</b> GET, PUT, PATCH, DELETE — use to view/edit/delete an existing board. The queryset is limited by the boards you have access to as a board participant (for viewing) or as the owner (for editing/deleting).

Only the board's owner can change or delete it. With the PUT method, they can add and delete board participants for the boards you own, as well as change their roles on the board. To do that, along with the board title, they should send the "boardparticipants" field with a list of dictionaries like this: {"user": id, "role": int}.

The board participants can have one of two roles:

- <b>Owner</b>.
- <b>Editor</b> — can create new categories and goals as well as comment on the goals on the board.
- <b>Reader</b> — can view categories, goals and comments on the board.

If the board is deleted, it remains in the database with the "deleted" status (with the "True" value in the "is_deleted" field). All categories on the board are marked as deleted as well, and all goals in those categories are marked as archived.

<b>goal_category/</b> endpoints:

<b>goal_category/create/</b> POST, creates a new category, requires a title for the new category ("title") and the id of the board ("board") to host the category on.
<b>goal_category/id/</b> GET, PUT, PATCH, DELETE, use to view/edit/delete an existing category, only the owner can change/delete categories.

If the category is deleted, it remains in the database with the "deleted" status (with the "True" value in the "is_deleted" field). All goals in that category are marked as archived.

<b>goal/</b> endpoints:

<b>goal/create/</b> POST, creates a goal, requires a title for the new goal ("title") and the id of the category to put the goal in ("category").
<b>goal/id/</b> GET, PUT, PATCH, DELETE use to view/edit/delete an existing goal, only the owner can change/delete goals.

Goals can have four statuses: "To Do", "In progress", "Done" and "Archived". Users can also set the priority for the goals: "Low", "Medium", "High" or "Critical".

When deleted, goals remain in the database with the "Archived" status.

<b>goal_comment/</b> viewpoints:

<b>goal_comment/create/</b> POST, creates a comment, requires the text of the comment ("text") and the id of the goal ("goal").
<b>goal_comment/id/</b> GET, PUT, PATCH, DELETE, use to view/edit/delete an existing comment, only the owner can change/delete comments.

### Telegram bot functionality

If a user wants to use the Telegram bot, they have to be registered in the main API and exist in the database.
When the user texts the bot for the first time, the bot sends them a code that they should send to the <b>bot/verify/</b> endpoint via a POST method (in the "verification_code" field).
After the user has sent the code, the API ties their tguser object with the Telegram chat details to the user object in the database. After that, the user can use the bot to get a list of their active goals with the <b>/goals</b> command or create new goals with the <b>/create_goal</b> command (the goal creation process can be stopped with the <b>/stop</b> command).
The <b>/start</b> command returns a hint with the possible commands for the bot. If the user has not sent the verification code to the API, the bot will not accept commands, it will continue to ask the user to send the code to the API.

## Challenges

### Permissions

It was difficult at first to keep track of varying permissions for different roles for the boards, but it got much easier to handle with inheritance. I decided to leave each type of permission for creating objects as their own class so it would be easy to change them in the future. Permissions for viewing/editing objects still have a lot of the same code, I haven't managed to organize them in a better way yet.

### The preservation of the user's status while creating the goal with the bot

I had to figure out how to recognize that the Telegram user had initiated a goal-creation process because I needed to get the board and the category and also the title for the goal from their following responses in the chat. I also had to store this data somewhere, while the process of creation was not finished.
The best decision I found so far is to store the info on the process in the database (as a separate TgUser field "goal_creating_status" with 5 possible statuses), as well as the info for the new goal (as an object of a separate model tied to the TgUser object, TgUserGoal). When the process of creating the goal has been completed or stopped, the TgUserGoal object is deleted from the database, and the TgUser object's goal_creating_status is set back to 0.
The code I came up with is rather cumbersome, but it's still the best solution I managed to come up with. I know that there are other solutions in the pre-maid libraries for bots, and I am planning to use one of them in another project. But in this one, the task was to write all of the bot logic by myself.

<i>Here starts the Readme in Russian.</i>

# API для списка дел

Это был финальный проект курса по Python. Это API на Django для сервиса, в котором пользователи могут создавать цели, а также доски и категории для целей. Пользователи могут приглашать других пользователей на свои доски с одной из двух ролей: читатель или редактор.
Также пользователи могут смотреть свой список целей и создавать новые цели через Telegram бота.

<p><b>Технологии:</b> Django, Telegram Bot API, Docker. </p>

<i>Замечание: requirements.txt такой длинный, потому что недавно я обновляла Django и столкнулась с ошибкой при запуске API (несовместимость с каким-то другим пакетом, каким конкретно — я не выяснила). На всякий случай, я обновила все пакеты и сложила их в requirements, чтобы API точно везде запускался.</i>

<p><b>Как запустить:</b>

Скопируйте репозиторий на компьютер, заполните файл example.env и переименуйте его в .env.
В терминале, из корневой папки проекта, введите команды:

`pip install -r requirements.txt`
`python3 todolist/manage.py migrate`
`python3 todolist/manage.py runserver`

Чтобы запустить бота, после того, как запустите API, в новом окне терминала введите:

`python3 todolist/manage.py runbot`

## Главные адреса

Когда приложение работает в режиме разработки (Debug=True в .env), документация по всем адресам API доступна в Swagger UI по адресу host:port/schema/swagger-ui/.

### Аутентификация пользователей

Для аутентификации с помощью токена:

<b>api/token/</b> — POST, возвращает пару токенов, нужно отправить логин и пароль (поля "username", "password").
<b>api/token/refresh/</b> - POST, возвращает новую пару токенов, нужно отправить refresh токен из ранее выданной пары.

CRUD для пользователей — по адресу api/core/:

<b>core/register</b> - POST, создает пользователя. Нужно отправить логин и пароль (поля "username" и "password").

Для создания цели нужно, чтобы уже существовала категория, а для создания категории нужно, чтобы у пользователя уже была доска. Поэтому API автоматически создает для каждого нового пользователя доску "My board", а на ней — категорию "My goals".

<b>core/update/uid/</b> PUT/PATCH
<b>core/profile/uid/</b> GET
<b>core/delete/uid/</b> DELETE

Пользователи могут просматривать/изменять/удалять только свой аккаунт.

### Функциональность целей

Все адреса для работы с целями находятся по пути api/goals/ (могут просматривать только аутентифицированные пользователи):

Адреса <b>board/:</b>

<b>board/create/</b> POST, создает доску, нужно отправить название ("title").
<b>board/id/</b> GET, PUT, PATCH, DELETE — просмотр/редактирование/удаление доски, выдача объектов из базы ограничена досками, с которыми пользователь связан как участник(просмотр) или как владелец(изменение/удаление).
Только хозяин доски может изменять или удалять ее. Через метод put хозяин может изменять список участников на своих досках и менять их роли. Для этого вместе с новыйм названием (поле "title") нужно отправить поле "boardparticipants" со списком словарей по образцу: {"user": id, "role": int}.

У участников досок могут быть три роли:

- <b>Хозяин (Owner)</b>.
- <b>Редактор (Editor)</b> — может создавать новые категории и цели, а также комментировать цели на доске.
- <b>Читатель (Reader)</b> — может просматривать категории, цели и комментарии на доске.

Удаленная доска остается в базе со статусом "удалена" (со значением "True" в поле "is_deleted"). Все категории на доске так же помечаются как удаленные, а целям в этих категориях присваевается статус "в архиве".

Адреса <b>goal_category/</b>:

<b>goal_category/create/</b> POST, создает категорию, требует название ("title") и id доски ("board"), на которой следует разместить категорию.
<b>goal_category/id/</b> GET, PUT, PATCH, DELETE — просмотр/редактирование/удаление категории, только владелец может изменять/удалять категории.

Удаленные категории остаются в базе данных и помечаются как удаленные (значением "True" в поле "is_deleted"), а целям в этих категориях присваетвается статус "в архиве".

Адреса <b>goal/</b>:

<b>goal/create/</b> POST, создает цель, требует название ("title") и id категории, в которую отправить цель ("category").
<b>goal/id/</b> GET, PUT, PATCH, DELETE — просмотр/редактирование/удаление цели, только владелец может изменять/удалять цели.

У целей могут быть четыре статуса: "Сделать" ("To Do"), "В процессе" ("In progress"), "Готово" ("Done") и "В архиве" ("Archived"). Также пользователь может выставить цели приоритет: "Низкий" ("Low"), "Средний" ("Medium"), "Высокий" ("High") или "Критический" ("Critical").

Удаленные цели остаются в базе данных со статусом "В архиве".

Адреса <b>goal_comment/</b>:

<b>goal_comment/create/</b> POST, создает комментарий, требует текст комментария ("text") и id цели, к которой прикрепить комментарий ("goal").
<b>goal_comment/id/</b> GET, PUT, PATCH, DELETE  — просмотр/редактирование/удаление комментария, только владелец может изменять/удалять комментарии.

### Функциональность Telegram-бота

Пользователю, который хочет воспользоваться ботом, нужно быть зарегистрирвоанным в api и присутствовать в базе данных. Когда пользователь пишет первое сообщение боту, он получает код, который нужно отправить методом POST на адре api <b>bot/verify/</b> (в поле "verification_code"). После того, как пользователь это сделал, api привязывает его объект tguser к объекту user в базе данных, и пользователь может получить список активных целей с помощью команды <b>/goals</b> или создать новые цели с помощью команды <b>/create_goal</b> (остановить создание цели можно командой <b>/stop</b>). Команда <b>/start</b> выдает подсказку с возможными командами для бота. Если пользователь не отправил код подтверждения в api, бот не будет принимать команды, он будет продолжать просить отправить код в api.

## Трудности

### Разрешения

Поначалу было трудно уследить за разрешениями для ролей на досках, но с наследованием их получилось более-менее упорядочить. Я решила оставить отдельный класс для каждого разрешения для создания объекта, чтобы в будущем их было легко изменять. Разрешения для просмотра/редактирования/удаления объектов все еще содержат повторяющийся код, мне пока не удалось организовать их лучше.

### Хранение прогресса пользователя во время создания цели через бота

Мне нужно было понять, как регистрировать, что пользователь начал создавать новую цель через чат, потому что из его последующих ответов мне нужно было получать имя доски и категории для новой цели, а еще название новой цели. Также эти ответы надо было как-то хранить весь процесс создания цели.
Лучшее решение, которое я придумала на нынешний момент — хранить все в базе данных. Я создала отдельное поле для модели TgUser, "goal_creating_status", с пятью возможными значениями: 0 по умолчанию и от 1 до 4 для каждого шага создания цели. А также новую модель TgUserGoal, объекты которой привязываются к TgUser и содержат информацию о доске/категории/названии для новой цели.
Когда новая цель создана или процесс создания остановлен пользователем, объект TgUserGoal удаляется из базы, а значение goal_creating_status для TgUser снова принимает значение 0.
Решение получилось громоздким, но лучше я пока не придумала. Я знаю, что в готовых библиотеках для ботов есть другие решения и планирую использовать одну из них в другом проекте, но в этой работе задача была написать всю логику бота самостоятельно.
