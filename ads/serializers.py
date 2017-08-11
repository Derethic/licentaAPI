from rest_framework import serializers

from ads.models import User, Ad, Message, Category, Subcategory, MCateg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'location', 'phone_number', 'last_login',
                  'date_joined')
        read_only_fields = ('last_login', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'location', 'phone_number', 'last_login',
                  'date_joined')
        read_only_fields = ('id', 'last_login', 'date_joined')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category_name')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'subcategory_name')


class MapCategorySerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='category_name', read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='subcategory_name', read_only=True)

    class Meta:
        model = MCateg
        fields = ('id', 'category', 'subcategory')


class AdSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    mapcategory = MapCategorySerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'currency', 'condition', 'view_count', 'user', 'mapcategory',
                  'picture1', 'picture2', 'picture3', 'picture4', 'ad_created_at')


class CreateOrUpdateAdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    mapcategory = serializers.PrimaryKeyRelatedField(queryset=MCateg.objects.all())

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'currency', 'condition', 'user', 'mapcategory', 'picture1', 'picture2',
                  'picture3', 'picture4')


class MessageSerializer(serializers.ModelSerializer):
    message_sender = UserSerializer(read_only=True)
    message_receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'message_sender', 'message_receiver', 'content', 'read_time', 'message_created_at')


class CreateMessageSerializer(serializers.ModelSerializer):
    message_sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    message_receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ('message_sender', 'message_receiver', 'content')
