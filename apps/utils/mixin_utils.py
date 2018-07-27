# apps/utils/mixin_utils.py
import datetime

from blog.models import PageDetail, TraceCount, ArticleCategory, Tags, TagsMap
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """若未登录, 跳转到登录界面"""
    @method_decorator(login_required(login_url='/user/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class GetDateMixin(object):
    """所有需要自动获取文章日期的接口mixin"""
    today = datetime.date.today()
    all_page_dates = PageDetail.objects.filter(add_time__year=today.year, add_time__month=today.month).values('add_time')
    date_set = set()
    for page in all_page_dates:
        year = page['add_time'].year
        month = page['add_time'].month
        day = page['add_time'].day
        date_set.add("-".join([str(year), "{:0>2}".format(month), "{:0>2}".format(day)]))
    del all_page_dates
    date_array = [ele for ele in date_set]      # 可供使用的变量


class TraceRouterMixin(object):
    """网站访问统计"""

    def get_trace(self, request):
        remote_addr = request.META.get("REMOTE_ADDR")
        router = request.path
        trace_count = TraceCount.objects.create(remote_addr=remote_addr, router=router, method=request.method)
        return trace_count


class CategoryMixin(object):

    @property
    def category(self):
        category = ArticleCategory.objects.all()
        for sub_cat in category:
            sub_cat.nums = PageDetail.objects.filter(category__name=sub_cat.name).count()
        category = sorted(category, key=lambda x: x.nums)
        return category[::-1]


class TagMixin(object):

    @property
    def tags(self):
        tags = Tags.objects.all()[:20]
        for tag in tags:
            tag.nums = TagsMap.objects.filter(tag=tag).count()
        tags = sorted(tags, key=lambda x: x.nums)
        return tags[::-1]
