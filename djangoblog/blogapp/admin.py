from django.contrib import admin
from .models import author, category, article, comment, tegory, gory, commentqq


# Register your models here.

class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]

    class Meta:
        Model = author


admin.site.register(author, authorModel)


class articleModel(admin.ModelAdmin):
    list_display = ["__str__", "posted_on"]
    search_fields = ["__str__", "details"]
    list_per_page = 10
    list_filter = ["posted_on", "category"]

    class Meta:
        Model = article


admin.site.register(article, articleModel)


class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = category


admin.site.register(category, categoryModel)


class commentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = comment


admin.site.register(comment, commentModel)

admin.site.register(tegory)

class goryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = gory


admin.site.register(gory, categoryModel)

admin.site.register(commentqq, categoryModel)
