import os
import random
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv
from typing import Dict
from django.db.models import Q
from bot.tg.client import TgClient
from bot.models import TgUser, TgUserNewGoal
from goals.models import Goal, Board, GoalCategory


class Command(BaseCommand):
    help = "Starts the Telegram bot"
    
    def get_code(self) -> str:
        """
        Creates a random user confirmation code.
        """
        randomlist = []
        for i in range(0,10):
            n = random.randint(1,10)
            randomlist.append(n)
            
        code = "".join(map(str, randomlist))
        return code
    
    def get_goals(self, chat_id: int) -> str:
        """
        Returns a string with a list of user's goals.
        """
        user = TgUser.objects.get(telegram_chat_id=chat_id)
        goals = Goal.objects.all().filter(Q(status=1)|Q(status=2), user=user.user)
        if goals:
            if len(goals) > 1:
                goals = "\n".join(goal.title for goal in goals)
            else:
                goals = goals[0].title
        return goals if goals else "You have no active goals."
    
    def get_boards(self, user_id: int) -> str:
        """
        Returns a string with a list of user's boards.
        """
        boards = Board.objects.filter(boardparticipants__user=user_id, is_deleted=False)
        if len(boards) > 1:
            boards = "\n".join(board.title for board in boards)  
        else:
            boards = boards[0].title
        return boards
    
    def get_goal_categories(self, user_id: int, board: Board) -> str:
        """
        Returns a string with a list of user's categories.
        """
        categories = GoalCategory.objects.filter(user=user_id, board=board)
        if len(categories) > 1:
            categories = "\n".join(category.title for category in categories)  
        else:
            categories = categories[0].title
        return categories
    
    def finish_goal_creation(self, user: TgUser) -> None:
        """
        Finishes goal creation by changing user's goal
        creating status and deleting the new goal data from database.
        """
        try:
            goal = TgUserNewGoal.objects.get(user=user)
            goal.delete()
        except:
            pass
        user.goal_creating_status = 0
        user.save()
        
    def create_goal(self, user: TgUser, client: TgClient, message: Dict) -> None:
        """
        Goes through each of the goal creation steps
        depending on the user's goal creation status.
        """
        if message.text == "/stop":
            self.finish_goal_creation(user)
            client.send_message(chat_id=message.chat.id,
                                    text="The goal creation process has been stoppped.")
            
        elif user.goal_creating_status == 1:
            client.send_message(chat_id=message.chat.id,
                                    text="Please select a board:")
            
            boards = self.get_boards(user.user_id)
            client.send_message(chat_id=message.chat.id,
                                text=boards)
            user.goal_creating_status = 2
            user.save()
        
        elif user.goal_creating_status == 2:
            board_title = message.text
            try:
                board = Board.objects.get(title=board_title,
                                    boardparticipants__user=user.user_id)
                goal = TgUserNewGoal()
                goal.user = user
                goal.board = board
                goal.save()
            except:
                client.send_message(chat_id=message.chat.id,
                                    text="Incorrect board title, please try again.")
                return
            
            user.goal_creating_status = 3
            user.save()
            client.send_message(chat_id=message.chat.id,
                                    text="Please select a category:")
            categories = self.get_goal_categories(user_id=user.user_id,
                                                board=board)
            client.send_message(chat_id=message.chat.id,
                                    text=categories)
            
        elif user.goal_creating_status == 3:
            category_title = message.text
            try:
                category = GoalCategory.objects.get(title=category_title,
                                    user=user.user_id)
                goal = TgUserNewGoal.objects.get(user=user)
                goal.category = category
                goal.save()
            except:
                client.send_message(chat_id=message.chat.id,
                                    text="Incorrect category title, please try again.")
                return
            
            user.goal_creating_status = 4
            user.save()
            client.send_message(chat_id=message.chat.id,
                                    text="Please enter the title of the goal:")
            
        elif user.goal_creating_status == 4:
            goal_title = message.text
            goal = TgUserNewGoal.objects.get(user=user)
            new_goal = Goal(category=goal.category, title=goal_title, user_id=user.user.id)
            new_goal.save()

            self.finish_goal_creation(user)
            client.send_message(chat_id=message.chat.id,
                                    text="Goal has been succesfully created.")
        
    def handle(self, *args, **options):     
        try:
            load_dotenv()
            offset = 0
            tg_client = TgClient(os.getenv("TELEGRAM_BOT_TOKEN"))
            self.stdout.write(self.style.SUCCESS('Successfully started the bot'))
            
            while True:
                res = tg_client.get_updates(offset=offset)
                for item in res.result:
                    offset = item.update_id + 1
                    try:
                        user = TgUser.objects.get(telegram_chat_id=item.message.chat.id)
                    except:
                            code = self.get_code()
                            tg_client.send_message(chat_id=item.message.chat.id,
                                                    text=f"Hello! Please verify your account. Your verification code is {code}. Enter the verification code into the app while logged in.")

                            TgUser.objects.create(telegram_chat_id=item.message.chat.id, telegram_user_ud=item.message.from_.id, verification_code=code)
                            break
                    if not user.verified:
                            tg_client.send_message(chat_id=item.message.chat.id, text=f"Please verify your account to start. Your verification code is {user.verification_code}. Enter the verification code into the app while logged in.")
                    
                    elif item.message.text == "/start":
                        tg_client.send_message(chat_id=item.message.chat.id, text=f"Hello! Please input one of the following commands:\n/goals to view your active goals,\n/create_goal to create a new goal.")
                    
                    elif item.message.text == "/goals":
                        goals = self.get_goals(item.message.chat.id)
                        tg_client.send_message(chat_id=item.message.chat.id,
                                                text=goals)
                    
                    elif item.message.text == '/create_goal':
                        user.goal_creating_status = 1
                        user.save()
                        tg_client.send_message(chat_id=item.message.chat.id, text="Input /stop to cancel the goal creation process.")
                        self.create_goal(user=user, client=tg_client, message=item.message)
                        
                    elif user.goal_creating_status:
                        self.create_goal(user=user, client=tg_client, message=item.message)
                    
                    else:
                        tg_client.send_message(chat_id=item.message.chat.id,
                                                text=f"Unknown command\nInput /start to begin")
                        
        except Exception as e:
            raise CommandError(e)
        