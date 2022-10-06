from django.contrib import admin
from .models import Paper, Category

# class PaperAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
#     pass

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug_category': ('name_category',)}
#     pass

# admin.site.register(Paper, PaperAdmin)
# admin.site.register(Category, CategoryAdmin)

admin.site.register(Paper)
admin.site.register(Category)
