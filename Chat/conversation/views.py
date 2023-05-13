from rest_framework import generics, permissions ,status
from rest_framework.views import APIView
from .models import Message , Conversation
from .serializers import ConversationSerializer
from rest_framework.response import Response 
from core.models import User
from django.shortcuts import render

class ListMessages(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request , username):
        try:
            user2= User.objects.get(username=username)
        except User.DoesNotExist :
            return Response({'detail':f'No such user have username {username}'})
        try:
            query = Conversation.objects.filter(
                user1 = user2 , user2 = request.user).union(Conversation.objects.filter(
                user2 = user2 , user1 = request.user) )[0]
        except IndexError :
            query = Conversation.objects.create(user1=request.user , user2= user2 , room_name=str(request.user.username+'_'+user2.username))
        print(query)
        serializer = ConversationSerializer(query)
        # serializer.is_valid(raise_exception=False) 
        return Response(serializer.data , status=status.HTTP_200_OK)


# class MessageListCreateView(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # Set the sender of the message to the authenticated user
#         serializer.save(sender=self.request.user)

#     def get_queryset(self):
#         # Return only messages between the authenticated user and the other user in the private chat
#         room_name = self.kwargs.get('room_name')
#         other_user = self.kwargs.get('other_user')
#         return Message.objects.filter(sender=self.request.user, receiver=other_user).union(
#             Message.objects.filter(sender=other_user, receiver=self.request.user)
#         )