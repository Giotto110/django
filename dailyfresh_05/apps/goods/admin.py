from django.contrib import admin
from goods.models import GoodsCategory,Goods,IndexPromotionBanner
from celery_tasks.tasks import generate_static_index_html
from django.core.cache import cache


# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()

        generate_static_index_html.delay()

        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        obj.delete()

        generate_static_index_html.delay()

        cache.delete('index_page_data')

class IndexPromotionBannerAdmin(BaseAdmin):

    pass

class GoodsAdmin(BaseAdmin):

    pass

admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)
admin.site.register(GoodsCategory)
admin.site.register(Goods,GoodsAdmin)
