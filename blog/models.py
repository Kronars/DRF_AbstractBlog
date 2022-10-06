from django.db import models
from user.models import MyUser
from django.contrib.auth.models import User
from django.utils.text import slugify
from config.settings import MAX_SLUG_LEN, MAX_TITLE_LEN


# Create your models here.
class Paper(models.Model):
    class Meta:
        db_table = 'paper'

    user     = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    category = models.ForeignKey('category', null=True, on_delete=models.SET_NULL, db_column='category')
    title    = models.CharField(max_length=MAX_TITLE_LEN, verbose_name='Название статьи')
    # slug     = models.SlugField(max_length=MAX_SLUG_LEN, verbose_name='SLUG статьи', unique=True) 
    paper_text  = models.TextField(verbose_name='Текст сатьи')
    paper_image = models.ImageField(blank=True, verbose_name='Превью статьи')
    pub_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    upd_date = models.DateField(auto_now=True, verbose_name='Дата последнего редактирования')
    likes    = models.IntegerField(default=0,  verbose_name='Лайки')
    dislikes = models.IntegerField(default=0,  verbose_name='Дизлайки')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Paper, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name_category = models.CharField(max_length=MAX_TITLE_LEN, verbose_name='Категория',     unique=True)
    # slug_category = models.SlugField(max_length=MAX_SLUG_LEN, verbose_name='URL категории', unique=True) 

    # def save(self, *args, **kwargs):
    #     self.slug_category = slugify(self.name_category)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name_category