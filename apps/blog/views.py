import json
import random

<<<<<<< HEAD
from blog.forms import PublishForm
from django.db.models import Q
from django.http import HttpResponse
=======
from django.db.models import Q
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
from django.shortcuts import render
from django.views import View
from utils.common import get_date, split_tags, paginate, get_bread_dict
from utils.mixin_utils import GetDateMixin, LoginRequiredMixin
from utils.page_exception import page_not_found

from .models import SiteInfo, Tags, PageDetail, Archiving, ArticleCategory, UserProfile, TagsMap


class IndexView(View):
    """主页视图"""
    def get(self, request):
        host = request.get_host()
        site_info = SiteInfo.objects.get(id=1)      # 网站信息

        category = ArticleCategory.objects.all()
<<<<<<< HEAD
        tags = Tags.objects.all()[:20]
        for tag in tags:
            tag.nums = TagsMap.objects.filter(tag=tag).count()
        tags = sorted(tags, key=lambda x: x.nums)
        pages = PageDetail.objects.all()
        lunbo_pages = pages.filter(is_lunbo=True)[:5]
        archiving = Archiving.objects.all()
=======
        tags = Tags.objects.all()
        tags = tags.order_by('-nums')[:20]          # 获取前20个标签
        pages = PageDetail.objects.all()
        lunbo_pages = pages.filter(is_lunbo=True)[:5]
        archiving = Archiving.objects.all()

>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        single_pages = paginate(request, pages[::-1], 5)

        return render(request, 'index.html', {'site_info': site_info,
                                              'tags': tags,
<<<<<<< HEAD
                                              'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                              'lunbo_pages': lunbo_pages,
                                              'single_pages': single_pages,
                                              'archiving': archiving,
                                              'category': category,
                                              'host': host})


class PageView(GetDateMixin, View):
    """页面详情视图"""
    def get(self, request, page_id):
        host = request.get_host()
        pages = PageDetail.objects.filter(id=page_id)
        if not pages:
            return page_not_found(request)
        next_page = PageDetail.objects.filter(id__gt=page_id)
        if next_page:
            next_page = next_page.order_by('add_time')[0]
        previous_page = PageDetail.objects.filter(id__lt=page_id)
        if previous_page:
            previous_page = previous_page.order_by('-add_time')[0]
<<<<<<< HEAD
=======

>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()
        for page in pages:
            if page:
                tag_maps = []
<<<<<<< HEAD
                tag_map_objs = None
                for tag in split_tags(page.tags):
                    tag_obj = Tags.objects.get(tag_name=tag)
                    temp_tag_map_objs = TagsMap.objects.filter(tag=tag_obj.id).exclude(article=page_id)     # 包括tag范围内但不包括自己的相关文章
                    if tag_map_objs:
                        temp_tag_map_objs = (tag_map_objs | temp_tag_map_objs).distinct()
                    tag_map_objs = temp_tag_map_objs
                tag_maps.extend(tag_map_objs)
                random.shuffle(tag_maps)

                return render(request, 'page_detail.html', {'page': page,
                                                            'user': request.user,
=======
                for tag in split_tags(page.tags):
                    tag_obj = Tags.objects.get(tag_name=tag)
                    tag_map_objs = TagsMap.objects.filter(tag=tag_obj.id).all()
                    for tag_map_obj in tag_map_objs:
                        tag_maps.append(tag_map_obj)
                random.shuffle(tag_maps)

                return render(request, 'page_detail.html', {'page': page,
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                            'category': category,
                                                            'archiving': archiving,
                                                            'host': host,
                                                            'date_msg': json.dumps(self.date_array),
                                                            'tag_maps': tag_maps[:8],
                                                            'next_page': next_page,
                                                            'previous_page': previous_page})


class CategoryView(GetDateMixin, View):
    """分类页面视图"""
    def get(self, request, category_id):
        host = request.get_host()
        pages = PageDetail.objects.filter(category=category_id).order_by('-add_time')
        if not pages:
            return page_not_found(request)
        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()
        bread_dict = get_bread_dict(category_id, pages[0].category.name)
        pages = paginate(request, pages, 8)
        return render(request, 'category.html', {'pages': pages,
<<<<<<< HEAD
                                                 'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                 'category': category,
                                                 'archiving': archiving,
                                                 'host': host,
                                                 'bread_dict': bread_dict,
                                                 'date_msg': json.dumps(self.date_array)})


class AuthorArticleView(GetDateMixin, View):
    """作者文章详情"""
    def get(self, request, author_id):
        host = request.get_host()
        pages = PageDetail.objects.filter(author=author_id).order_by('-add_time')
        if not pages:
            return page_not_found(request)
        author = UserProfile.objects.get(id=author_id)
        bread_dict = get_bread_dict(author_id, pages[0].author.username)
        count = pages.count()
        pages = paginate(request, pages, 8)
        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()
        return render(request, 'author_article.html', {'pages': pages,
<<<<<<< HEAD
                                                       'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                       'category': category,
                                                       'archiving': archiving,
                                                       'host': host,
                                                       'author': author,
                                                       'count': count,
                                                       'bread_dict': bread_dict,
                                                       'date_msg': json.dumps(self.date_array)})


class DateHistoryView(View):
    """通过日期搜索文章"""
    def get(self, request, date):
        host = request.get_host()
        date = get_date(date)
        day = date.get('day')
        month = date.get("month")
        year = date.get('year')
        all_pages = PageDetail.objects.filter(add_time__year=year, add_time__month=month).order_by('-add_time')
        if day:
            pages = PageDetail.objects.filter(add_time__year=year, add_time__month=month, add_time__day=day).order_by('-add_time')
        else:
            pages = all_pages
        date_set = set()
        for page in all_pages:
            _year = page.add_time.year
            _month = page.add_time.month
            _day = page.add_time.day
            date_set.add("-".join([str(_year), "{:0>2}".format(_month), "{:0>2}".format(_day)]))
        date_array = [ele for ele in date_set]
        del all_pages
<<<<<<< HEAD
=======

>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        pages = paginate(request, pages, 8)

        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()
        return render(request, 'date_article.html', {'pages': pages,
<<<<<<< HEAD
                                                     'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                     'category': category,
                                                     'archiving': archiving,
                                                     'host': host,
                                                     'date': '-'.join([str(year), "{:0>2}".format(month), "{:0>2}".format(day)]),
                                                     'date_msg': json.dumps(date_array)})


class SearchView(GetDateMixin, View):
    """通过关键字进行搜索"""
    def get(self, request):
<<<<<<< HEAD
        keyword = request.GET.get('keyword')        # 获取关键字
        host = request.get_host()
        pages = PageDetail.objects.filter(Q(title__contains=keyword) | Q(category__name=keyword))   # 获取文章中标题含有关键字或分类为关键字的set
        tag_pages = TagsMap.objects.filter(tag__tag_name=keyword).values('article')                 # 从tag映射集中获取名字为关键字的文章
=======
        keyword = request.GET.get('keyword')
        host = request.get_host()
        pages = PageDetail.objects.filter(Q(title__contains=keyword) | Q(category__name=keyword))
        tag_pages = TagsMap.objects.filter(tag__tag_name=keyword).values('article')

>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        article_pages = None
        for tag_page in tag_pages:
            temp_page = PageDetail.objects.filter(id=tag_page['article'])
            if article_pages:
                temp_page = temp_page | article_pages
            article_pages = temp_page
<<<<<<< HEAD
        if pages and article_pages:
            pages = (pages | article_pages).distinct().order_by('-add_time')
=======
        pages = (pages | article_pages).distinct().order_by('-add_time')
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
        count = pages.count()

        pages = paginate(request, pages, 20)

        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()
        return render(request, 'search_article.html', {'pages': pages,
<<<<<<< HEAD
                                                       'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                       'category': category,
                                                       'archiving': archiving,
                                                       'host': host,
                                                       'count': count,
                                                       'date_msg': json.dumps(self.date_array)})


class TagView(GetDateMixin, View):
    """获取tag相关的视图页面"""
    def get(self, request, tag_name):
        host = request.get_host()
        tag = Tags.objects.filter(tag_name=tag_name)
        if not tag:
            return page_not_found(request)
        tag_maps = TagsMap.objects.filter(tag__tag_name=tag_name)
        count = tag_maps.count()
        bread_dict = get_bread_dict(tag[0].id, tag_name)
        tag_maps = paginate(request, tag_maps[::-1], 8)
        category = ArticleCategory.objects.all()
        archiving = Archiving.objects.all()

        return render(request, 'tags_article.html', {'tag_maps': tag_maps,
<<<<<<< HEAD
                                                     'user': request.user,
=======
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                     'category': category,
                                                     'archiving': archiving,
                                                     'host': host,
                                                     'count': count,
                                                     'bread_dict': bread_dict,
                                                     'date_msg': json.dumps(self.date_array)})


class MessageBoardView(View):
    """留言板视图页面"""
    def get(self, request):
        host = request.get_host()
        site_info = SiteInfo.objects.get(id=1)  # 网站信息
<<<<<<< HEAD
        login_required = not request.user.is_authenticated
        category = ArticleCategory.objects.all()
        tags = Tags.objects.all()[:20]
        for tag in tags:
            tag.nums = TagsMap.objects.filter(tag=tag).count()
        tags = sorted(tags, key=lambda x: x.nums)
        # pages = PageDetail.objects.all()
        archiving = Archiving.objects.all()
        return render(request, 'message_board.html',  {'site_info': site_info,
                                                       'login_required': login_required,
                                                       'user': request.user,
                                                       'tags': tags,
=======
        category = ArticleCategory.objects.all()
        tags = Tags.objects.all()
        tags = tags.order_by('-nums')[:20]  # 获取前20个标签
        pages = PageDetail.objects.all()
        archiving = Archiving.objects.all()

        single_pages = paginate(request, pages[::-1], 5)
        return render(request, 'message_board.html',  {'site_info': site_info,
                                                       'tags': tags,
                                                       'single_pages': single_pages,
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
                                                       'archiving': archiving,
                                                       'category': category,
                                                       'host': host})


<<<<<<< HEAD
class PublishView(View):
    """发表文章页面"""
    def get(self, request):
        host = request.get_host()
        site_info = SiteInfo.objects.get(id=1)  # 网站信息
        archiving = Archiving.objects.all()
        category = ArticleCategory.objects.all()
        tags = Tags.objects.all()[:20]
        for tag in tags:
            tag.nums = TagsMap.objects.filter(tag=tag).count()
        tags = sorted(tags, key=lambda x: x.nums)
        login_required = not request.user.is_authenticated
        return render(request, 'publish_article.html', {"login_required": login_required,
                                                        "site_info": site_info,
                                                        'user': request.user,
                                                        'tags': tags,
                                                        'category': category,
                                                        'archiving': archiving,
                                                        'host': host})

    def post(self, request):
        category = ArticleCategory.objects.get(name=request.POST.get("category"))
        author = UserProfile.objects.get(username=request.user)
        local_post = request.POST.copy()            # 浅拷贝表单提交的信息
        local_post.update({"category": category.id, "author": author.id})
        tags = local_post.get("tags", "")
        publish_form = PublishForm(local_post, request.FILES)       # 使用更改过的本地的POST信息
        if publish_form.is_valid():
            article = publish_form.save()
            for tag in split_tags(tags):
                tag_obj, status = Tags.objects.get_or_create(tag_name=tag)
                if tag_obj:
                    tag_obj.nums += 1
                    tag_obj.save()
                    TagsMap.objects.get_or_create(tag=tag_obj, article=article)  # 映射关系建立
            return HttpResponse(json.dumps({"msg": "文章提交成功", "status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"msg": "文章提交失败，请验证表单是否正确填写", "status": "failure"}), content_type="application/json")
=======
class PublishView(LoginRequiredMixin, View):
    """发表文章页面"""
    def get(self, request):
        return render(request, 'publish_article.html', {})
>>>>>>> 099e5c25ae68b192044e849abac312193b08b4b9
