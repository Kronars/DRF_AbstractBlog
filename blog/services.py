from datetime import datetime
from django.db.models import QuerySet
from django.http import Http404
from .models import Paper
from config.settings import MAX_TITLE_LEN

def validate_search_params( title:str=False, name_cat:str=False, pub_date:str=False, 
                            order:str=False, desc=False) -> dict:
    '''Параметр order указывает по какому одному параметру отсортировать результат'''
    validated = {'order':'title'}
    if not any((title, name_cat, pub_date)): # Если не указан ни один параметр
        raise Http404('Для поиска необходимо указать параметр')

    if title:
        if len(title) > MAX_TITLE_LEN: raise Http404(f'Слишком длинное название, максимум {MAX_TITLE_LEN} символа')
        else: validated['title__icontains'] = title

    if name_cat:    
        if len(name_cat) > MAX_TITLE_LEN: raise Http404(f'Слишком длинное название, максимум {MAX_TITLE_LEN} символа')
        else: validated['category__name_category'] = name_cat

    if pub_date:
        try:
            pub_datetime = datetime.strptime(pub_date, r'%Y-%m-%d') # r'%d-%m-%Y'
            # pub_datetime = datetime.strftime(pub_date, r'%Y-%m-%d')
        except ValueError:
            raise Http404(f'Полученная дата - {pub_date}, не соответствует формату YYYY-MM-DD')
        
        if pub_datetime > datetime.now(): raise Http404(f'Я дико извиняюсь, а ты как в будущем статьи искать собрался?')
        else: validated['pub_date'] = pub_date

    if order in ['title', 'category', 'pub_date']: 
        validated['order'] = order

    if desc:
        if order:   # Если выбрана сортировка по столбцу, 
                    # символ - меняет порядок сортировки на возрастающий
            validated['order'] = '-' + validated['order']
    
    return validated


def find_paper(validated_params: dict) -> QuerySet:
    
    order = validated_params.pop('order')

    return Paper.objects.filter(**validated_params).order_by(order)
    

def validate_slice(offset: str, limit: str):
    '''Проверка корректности среза'''
    if offset.isdigit() and limit.isdigit():
        offset, limit = int(offset), int(limit)
    else: Http404('offset и limit должны быть числом')

    if offset >= limit or offset < 0 or limit < 0:
        # return HttpResponseBadRequest('offset должен быть меньше limit')
        raise Http404('offset должен быть меньше limit')

    return offset, limit
