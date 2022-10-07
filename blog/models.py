from config.settings import MAX_TITLE_LEN
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Paper(models.Model):
    class Meta:
        db_table = 'paper'

    user     = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    category = models.ForeignKey('category', null=True, on_delete=models.SET_NULL, db_column='category')
    title    = models.CharField(max_length=MAX_TITLE_LEN, verbose_name='Название статьи')
    paper_text  = models.TextField(verbose_name='Текст сатьи')
    paper_image = models.ImageField(blank=True, verbose_name='Превью статьи')
    pub_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    upd_date = models.DateField(auto_now=True, verbose_name='Дата последнего редактирования')
    likes    = models.IntegerField(default=0,  verbose_name='Лайки')
    dislikes = models.IntegerField(default=0,  verbose_name='Дизлайки')

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name_category = models.CharField(max_length=MAX_TITLE_LEN, verbose_name='Категория',     unique=True)

    def __str__(self):
        return self.name_category
