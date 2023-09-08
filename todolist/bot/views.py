from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import os
from dotenv import load_dotenv
from bot.models import TgUser
from bot.tg.client import TgClient


class VerificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Get verification code, tie TgUser to the User
        instance.
        """
        try:
            code = request.data["code"]
            tg_user = TgUser.objects.get(verification_code=code)
        except:
            raise serializers.ValidationError("Wrong verification code")
    
        tg_user.user = request.user
        tg_user.verified = True
        tg_user.save()
        
        load_dotenv()
        tg_client = TgClient(os.getenv("TELEGRAM_BOT_TOKEN"))
        tg_client.send_message(chat_id=tg_user.telegram_chat_id,
                               text="Your account has been succesfully verified.")
        
        return Response(status=status.HTTP_200_OK)
            