from blog.models import Category, Paper
from blog.services import find_paper, validate_search_params
from config.settings import MAX_TITLE_LEN
from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


class BlogTestCase(TestCase):
    '''Модульные тесты'''
    invalid_inputs = [
        {'title': ''},
        {'title': 'A' * (MAX_TITLE_LEN + 1)},
        {'pub_date': '1-1_2047'},
        {'pub_date': '01-01-2047'},
        {'order': 'no'}
    ]

    def setUp(self):
        user_ivan = User.objects.create(username='ИИИ', first_name='Иван', last_name='Иванов')
        user_lev  = User.objects.create(username='Лев', first_name='Лёёёвик)')
        user_lev.myuser.description = 'Чел, лёвик типо'
        user_lev.save()

        cat_1 = Category.objects.create(name_category='Категория 1')
        cat_2 = Category.objects.create(name_category='Категория 2')

        Paper.objects.create(user=user_lev,  category=cat_1, title='Название 1', paper_text='Вставить текст')
        Paper.objects.create(user=user_ivan, category=cat_2, title='Название 2', paper_text='Вставить текст')

    def test_model(self):
        user_ivan = User.objects.get(first_name='Иван')
        user_lev  = User.objects.get(username='Лев')

        self.assertEqual(user_ivan.username, 'ИИИ')
        self.assertEqual(user_lev.myuser.description, 'Чел, лёвик типо')

    def test_validate_search_params_valid(self):
        val = {
            'title': 'Название', 'name_cat': 'Категория 1',
            'pub_date': '2001-01-01', 'order': 'title', 'desc': True}
        answer = {
            'title__icontains': 'Название', 'category__name_category': 'Категория 1',
            'pub_date': '2001-01-01', 'order': '-title'}
        self.assertEqual(validate_search_params(**val), answer)

    def test_validate_search_params_invalid(self):
        for invalid_dict in self.invalid_inputs:
            with self.subTest(f'Проверка валидации параметров поиска, упал из за - {invalid_dict} '):
                with self.assertRaises(Http404):
                    validate_search_params(**invalid_dict)

    def test_find_paper(self):
        val = validate_search_params('Название', 'Категория 1', order='title')
        res = find_paper(val)[0]   # может ведь упасть с ошибкой, хорошо бы придумать что получше
        self.assertEqual(res.title, 'Название 1')


class BlogApiTestCase(APITestCase):
    '''Интеграционные тесты'''
    def setUp(self) -> None:
        user_ivan = User.objects.create(username='ИИИ', first_name='Иван', last_name='Иванов')
        user_lev  = User.objects.create(username='Лев', first_name='Лёёёвик)')
        user_lev.myuser.description = 'Чел, лёвик типо'
        user_lev.save()

        cat_1 = Category.objects.create(name_category='Категория 1')
        cat_2 = Category.objects.create(name_category='Категория 2')

        Paper.objects.create(user=user_lev,  category=cat_1, title='Название 1', paper_text='Вставить текст')
        Paper.objects.create(user=user_ivan, category=cat_2, title='Название 2', paper_text='Вставить текст')

        self.token = self.client.get('')

    def test_paper_find(self):
        '''Что то типо параметризированного теста'''
        core_url = reverse('paper-find')
        params = (
            ('?title=Название', 'Название 1'),
            ('?category=Категория 2', 'Название 2'),
            ('?title=Название&category=Категория 2&desc=True', 'Название 2'),
            ('?title=Название&category=Категория 2&order_by=category', 'Название 2'))
        for param in params:
            with self.subTest():
                url = core_url + param[0]
                res = self.client.get(url)
                self.assertEqual(res.data[0]['title'], param[1])

    def test_post_paper(self):
        url = reverse('paper-create')
        data = (
            {
                "category": {
                    "name_category": "приколы"},
                "title": "1234",
                "paper_text": "1234",
                "paper_image": None,
                "user": 2
                },)

        for payload in data:
            with self.subTest():
                print(url)
                repl = self.client.post(url, payload, 'json')
                print(repl)
                print(repl.status_code)
