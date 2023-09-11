from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from bot.models import TgUser


class VerificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Get verification code, tie TgUser to the User
        instance.
        """
        try:
            code = request.data["verification_code"]
        except:
            raise serializers.ValidationError("Please insert a correct verification code")
        
        tg_user = TgUser.objects.get(verification_code=code)
        tg_user.user = request.user
        tg_user.verified = True
        tg_user.save()
        return Response(status=status.HTTP_200_OK)
            