from rest_framework import routers
from rest_framework.urls import path

from blog.views import (CategoryList, PaperCreate, PaperDetail, 
                        PaperFind, PaperList)

router = routers.SimpleRouter()
router.register('paper', PaperList)
router.register('paper', PaperDetail)
router.register('paper_create', PaperCreate, basename='paper-post')
router.register('category', CategoryList)

urlpatterns = [
    path('paper/find/', PaperFind.as_view(), name='paper-find')
    ]

urlpatterns += router.urls
