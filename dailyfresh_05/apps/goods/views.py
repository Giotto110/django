from django.shortcuts import render
from django.views.generic import View
from django_redis import get_redis_connection
from goods.models import GoodsCategory,Goods,GoodsSKU,GoodsImage,IndexGoodsBanner,IndexPromotionBanner,IndexCategoryGoodsBanner
from django.core.cache import cache
# Create your views here.


class IndexView(View):

    def get(self,request):

        context = cache.get('index_page_data')
        if context is None:
            categorys = GoodsCategory.objects.all()

            index_banners = IndexGoodsBanner.objects.all().order_by('index')

            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            for category in categorys:
                title_banners = IndexCategoryGoodsBanner.objects.filter(category=category,display_type=0).order_by('index')
                category.title_banners = title_banners

                image_banners = IndexCategoryGoodsBanner.objects.filter(category=category,display_type=1).order_by('index')
                category.image_banners = image_banners


            context = {
                'categorys':categorys,
                'index_banners':index_banners,
                'promotion_banners':promotion_banners,
            }

            cache.set('index_page_data',context,3600)

        cart_num = 0

        if request.user.is_authenticated():
            redis_conn = get_redis_connection('default')

            user_id = request.user.id

            cart_dict = redis_conn.hgetall('cart_%s'%user_id)

            for val in cart_dict.values():
                cart_num += int(val)

        cart_num = 10


        context.update(cart_num=cart_num)

        return render(request,'index.html',context)