# -*- coding:utf-8 -*-
import xadmin
from utils.common import split_tags

from .models import PageDetail, Tags, ArticleCategory, SiteInfo, TagsMap, Archiving, Message


class PageDetailAdmin(object):
    list_display = ['title', 'author', 'category', 'comments', 'views', 'detail', 'image', 'tags', 'add_time']
    search_fields = ['title', 'author', 'category', 'tags']
    list_filter = ['title', 'author', 'category', 'tags', 'add_time']
    ordering = ['-views']
    readonly_fields = ['views', 'comments']
    style_fields = {"detail": "ueditor"}

    def save_models(self):
        """保存文章响应更新网站信息"""
        obj = self.new_obj
        obj.save()
        archiving, _ = Archiving.objects.get_or_create(year=obj.add_time.year, month=obj.add_time.month)
        for tag in split_tags(obj.tags):
            tag_obj, status = Tags.objects.get_or_create(tag_name=tag)
            if tag_obj:
                TagsMap.objects.get_or_create(tag=tag_obj, article=obj)     # 映射关系建立

    def delete_model(self):
        """删除文章时进行的数据更新"""
        obj = self.obj
        archiving = Archiving.objects.get(year=obj.add_time.year, month=obj.add_time.month)
        for tag in split_tags(obj.tags):
            tag_obj = Tags.objects.get(tag_name=tag)
            if tag_obj:
                tag_map_obj = TagsMap.objects.get(tag=tag_obj, article=obj)
                tag_map_obj.delete()
        obj.delete()


class TagAdmin(object):
    list_display = ['tag_name', 'get_nums']
    search_fields = ['tag_name']
    list_filter = ['tag_name']
    ordering = ['tag_name']


class TagMapAdmin(object):
    list_display = ['tag', 'article']
    search_fields = ['tag', 'article']
    list_filter = ['tag', 'article']

    def save_models(self):
        """tag引用计数的更新"""
        obj = self.new_obj
        obj.save()
        tag_obj = Tags.objects.get(id=obj.tag.id)
        article_obj = PageDetail.objects.get(id=obj.article.id)
        if article_obj:
            article_obj.tags += "," + tag_obj.tag_name
            article_obj.save()

    def delete_model(self):
        """删除Tag映射"""
        obj = self.obj
        tag_obj = Tags.objects.get(id=obj.tag.id)
        article_obj = PageDetail.objects.get(id=obj.article.id)
        if article_obj:
            import re
            # 对文章的标签进行修改
            subtract_res = re.split(tag_obj.tag_name, article_obj.tags)
            tags_array = [split_tags(res) for res in subtract_res if res]
            new_tag = ','.join([tag for tags in tags_array for tag in tags])
            article_obj.tags = new_tag
            article_obj.save()
        # 最后删除该项数据
        self.obj.delete()


class CategoryAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


class ArchivingAdmin(object):
    list_display = ['year', 'month', 'get_nums']
    search_fields = ['year', 'month']
    list_filter = ['year', 'month']
    ordering = ['-year', '-month']


class SiteInfoAdmin(object):
    list_display = ['site_name', 'get_category_nums', 'get_tag_nums', 'get_article_nums', 'get_comments_nums', 'get_total_views', 'get_lasting_time']
    search_fields = ['site_name']
    list_filter = ['site_name']


class MessageAdmin(object):
    list_display = ['message', 'add_time']
    search_fields = ['message']
    list_filter = ['message']
    readonly_fields = ['message']


xadmin.site.register(SiteInfo, SiteInfoAdmin)
xadmin.site.register(PageDetail, PageDetailAdmin)
xadmin.site.register(Tags, TagAdmin)
xadmin.site.register(TagsMap, TagMapAdmin)
xadmin.site.register(ArticleCategory, CategoryAdmin)
xadmin.site.register(Archiving, ArchivingAdmin)
xadmin.site.register(Message, MessageAdmin)
