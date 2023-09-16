# Todolist API

This was a final project from the Python course. 

<p><b>Technologies:</b> Django, Telegram Bot API, Docker. </p>

<p><b>To launch:</b>

Download the folder onto your computer, fill in the .env file.
From the root folder run following commands:

`pip install -r requirements.txt`
`python3 todolist/manage.py migrate`
`python3 todolist/manage.py runserver`

To run the telegram bot, while running the app, run:

`python3 todolist/manage.py runbot`

## Main viewpoints

You can see all of the app's viewpoints documented in the Swagger ui at host:port/schema/swagger-ui/

###User Authentication

For token authentication:

<b>api/token/</b> — POST, use to get a pair of tokens, requires a username and a password.
<b>api/token/refresh/</b> - POST, use to get a new token, requi refresh token from the previously issued pair.

The rest are under the api/core/ path:

<b>core/register</b> - POST, use to create a user. Requires a username and a password.

The creation of a goal requires an existing category and the creation of the category requires an existing board, so the API automatically creates a board named "My board" and a category named "My goals" for every new user.

The rest are the standart views for the authenticated users:

<b>core/update/uid/</b> PUT/PATCH
<b>core/profile/uid/</b> GET
<b>core/delete/uid/</b> DELETE

Users can only view/change/delete their own account.

###Goals functionality

All under the api/goals/ path (can be viewed by authenticated users only):

<b>board/ viewpoints:</b>

<b>board/create/</b> POST, use to create a new board.
<b>board/id/</b> GET, PUT, PATCH, DELETE — use to edit an existing board, the queryset is limited by the boards you have access to as a board participant. Through the put method you can add and delte board participants for the boards you own, as well as change their roles on the board. To do that, along with the board title send a "boardparticipants" field with a list of dictionaries like this: {"user": id, "role": int}.

Only the board's owner can change or delete it. But boards hawe two more roles:

- An <b>Editor</b> can create new categories and goals and comment the goals on the board.
- A <b>Reader</b> can view categories, goals and comments on the board.

<b>goal_category/</b> viewpoints:

<b>goal_category/create/</b> POST, requires a title for the new category and the id of the board to host the category on.
<b>goal_category/id/</b> GET, PUT, PATCH, DELETE, only the owner can change/delete categories.

<b>goal/</b> viewpoints:

<b>goal/create/</b> POST, requires a title for the new goal and the id of the category to put the goal in.
<b>goal/id/</b> GET, PUT, PATCH, DELETE, only the owner can change/delete goals.

<b>goal_comment/</b> viewpoints:

<b>goal_comment/create/</b> POST, requires a text of the comment and the id of the goal.
<b>goal_comment/id/</b> GET, PUT, PATCH, DELETE, only the owner can change/delete comments.

###Telegram bot functionality

To use the Telegram bot, you have to be registered in the main api and exist in the database. When you text the bot for the first time, it gives you a code to send to the <b>bot/verify/</b> endpoint. After you've done that, the api ties the tguser to the user in the database and you can get a list of your active goals with <b>/goals</b> command or create new goals with <b>/create_goal</b> command.

##Challenges

###Permissions

It was difficult at first to keep track of varying permissions for different roles on the board, but it got much easier to handle with the inheritance structure. I decided to leave each type of object create permission as their own class so they would be easy to change in the future. Main object permissions still have a lot of same code, I didn't manage to organize them better yet.

###/create_goal status handling via the Telegram bot

I was stuck with the question of how do I recognize if the user have initiated a goal creation process, because I needed to take their responses to pick a board and a category for the new goal. I also had to store this data somehow, while the process of creation goes. The best decision I managed to come up with so far was to store the info on the process in the database (as a separate TgUser field "goal_creating_status" with 5 possible statuses) as well as the info for the new goal (as an instance of a separate model tied to TgUser, TgUserGoal). After the process of creation of the new goal has been completed or stopped, the TgUserGoal instance is deleted from the database, and TgUser's goal_creating_status is set back to 0.
The code I came up is rather cumbersome, but it's still the best implementation I could come up with.