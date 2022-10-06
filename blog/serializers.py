from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Category, Paper


class AuthorList(serializers.ModelSerializer):
    '''Сериализатор автора поста'''
    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name']

class CatList(serializers.ModelSerializer):
    '''Сериализатор каегории, только для чтения и отображения в списке'''
    class Meta:
        model  = Category
        fields = ['id', 'name_category']

class CatCreate(serializers.ModelSerializer):
    '''Сериализатор категории для создания постов. 
    Нужен для отключения проверок блокирующих запись'''
    class Meta:
        model = Category
        fields = ['name_category']
        extra_kwargs = {
            'name_category': {'validators': []}
        }

class MetaPaperList(serializers.ModelSerializer):
    '''Сериализатор информации о статье, без самой статьи'''
    author   = AuthorList(source='user')
    category = CatList()    # Если назвать атрибут именем отличным от названия класса, 
                            # и не указать сурс, всплывёт ошибка лол 

    class Meta:
        model   = Paper
        exclude = ('paper_text', 'paper_image', 'user')

class PaperDetailSerializer(serializers.ModelSerializer):
    '''Сериализатор всей информации о статье, только для чтения'''
    author = AuthorList(source='user')
    category = CatList()

    class Meta:
        model = Paper
        exclude = ['user']

class PaperCreateSerializer(serializers.ModelSerializer):
    '''Публикация статьи, отличие от PaperList в сериализаторе категории, 
    его поле "название категории" имеет тип ChoiceField
    POST paper_create/'''
    category = CatCreate()

    class Meta:
        model   = Paper
        exclude = ('likes', 'dislikes',)

    def create(self, validated_data):
        cat_to_post = validated_data.pop('category')['name_category']
    
        try:
            cat_to_post = Category.objects.get(
                name_category__contains=cat_to_post
                )
        except Exception as e:
            raise NotFound(f'Категории статьи {cat_to_post} не существует, укажите существующее в списке /api/v1/category название')
        
        pape = Paper.objects.create(category_id=cat_to_post.pk, **validated_data)
        return pape
