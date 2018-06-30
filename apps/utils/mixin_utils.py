# apps/utils/mixin_utils.py
import datetime

from blog.models import PageDetail
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
