from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Paper
from .serializers import (CatList, MetaPaperList, PaperCreateSerializer,
                          PaperDetailSerializer)
from .services import find_paper, validate_search_params, validate_slice


class CategoryList(generics.ListAPIView,
                   viewsets.GenericViewSet):
    '''Получение списка доступных категорий'''
    queryset = Category.objects.all()
    serializer_class = CatList

class PaperList(generics.ListAPIView, 
                viewsets.GenericViewSet):
    '''Получение мета информации о срезе статьей, от offset до limit
    GET paper/'''
    queryset = Paper.objects.all()
    serializer_class = MetaPaperList

    def get_queryset(self):
        offset: str = self.request.query_params.get('offset', '0')
        limit:  str = self.request.query_params.get('limit', '40')
        cat_filter_value = self.request.query_params.get('filter', None)

        offset, limit = validate_slice(offset, limit)

        if cat_filter_value:
            query = Paper.objects.filter(
                Q(category__name_category=cat_filter_value) | Q(category__slug_category=cat_filter_value)
                )[offset:limit]
        else:
            query = Paper.objects.all()[offset:limit]

        return query


class PaperDetail(generics.RetrieveAPIView,
                  viewsets.GenericViewSet):
    '''Получение полной статьи по id
    GET paper/1'''
    queryset = Paper.objects.all()
    serializer_class = PaperDetailSerializer


class PaperCreate(generics.CreateAPIView,
                  viewsets.GenericViewSet):
    '''Публикация статьи
    POST paper_create/'''
    queryset = Paper.objects.all()
    serializer_class = PaperCreateSerializer


class PaperFind(APIView):
    '''Обработка поискового запроса списка статьей
    GET paper/find'''
    queryset = Paper.objects.all()
    serializer_class = MetaPaperList
    
    def get(self, req):
        '''Получение параметров -> валидация парамметров -> поиск в БД -> сериализация'''
        title:    str | bool = req.query_params.get('title', False)   # Получение параметров
        name_cat: str | bool = req.query_params.get('category', False)
        pub_date: str | bool = req.query_params.get('pub_date', False)
        order: str['title', 'name_cat', 'pub_date'] = req.query_params.get('order_by', False)
        desc: bool = req.query_params.get('desc', False)

        validated_params = validate_search_params(title, name_cat, pub_date, order, desc)
        paper = find_paper(validated_params)
        serializer = self.serializer_class(paper, many=True)

        return Response(serializer.data)
