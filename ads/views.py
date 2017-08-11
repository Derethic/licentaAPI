from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models import Q
from rest_framework import  status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ads.models import User, Ad, MCateg, Message

from ads.serializers import UserSerializer, AdSerializer, \
    MapCategorySerializer, RegisterSerializer, MessageSerializer, CreateMessageSerializer, \
    CreateOrUpdateAdSerializer


class UserList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            hashedPassword = make_password(serializer.validated_data['password'])

            serializer.validated_data['password'] = hashedPassword
            serializer.save()

            token = Token.objects.get(user_id=serializer.data["id"])

            return Response(data={
                "id": serializer.data["id"],
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'id': token.user_id, 'token': token.key})


class CategoryView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        categories = MCateg.objects.all()
        serializer = MapCategorySerializer(categories, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class AdView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        ads = Ad.objects.all()
        serializer = AdSerializer(ads, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

    def post(self, request, format=None):
        serializer = CreateOrUpdateAdSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class AdDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Ad.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ad = self.get_object(pk)
        serializer = AdSerializer(ad)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request, pk, format=None):
        ad = self.get_object(pk)
        serializer = CreateOrUpdateAdSerializer(ad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        ad = self.get_object(pk)

        if self.request.user == ad.user_id:
            ad.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAdList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        ads = Ad.objects.filter(user_id=self.request.user)
        serializer = AdSerializer(ads, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class ReceivedMessageList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        messages = Message.objects.filter(message_receiver=self.request.user)
        serializer = MessageSerializer(messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class SentMessageList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        messages = Message.objects.filter(message_sender=self.request.user)
        serializer = MessageSerializer(messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class ConversationList(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        currentMessage = self.get_object(pk)

        messages = Message.objects.order_by('message_created_at').filter(
            (Q(message_sender=currentMessage.message_sender) &
             Q(message_receiver=currentMessage.message_receiver)) |
            (Q(message_sender=currentMessage.message_receiver) &
             Q(message_receiver=currentMessage.message_sender))
        )

        serializer = MessageSerializer(messages, many=True)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)


class CreateMessageView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateMessageSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
