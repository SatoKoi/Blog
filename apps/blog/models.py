from django.db import models, connection
from users.models import UserProfile
from DjangoUeditor.models import UEditorField
from datetime import datetime, date


class SiteInfo(models.Model):
    """网站信息详情"""
    site_name = models.CharField(max_length=20, verbose_name="网站名称")
    upload_time = models.DateTimeField(default=datetime.now, verbose_name="创建日期")

    class Meta:
        verbose_name_plural = verbose_name = "网站详情"

    def __str__(self):
        return self.site_name

    def get_lasting_time(self):
        """获取运行天数"""
        return (datetime.today() - self.upload_time).days + 1
    get_lasting_time.short_description = "运行时间(天)"

    def get_category_nums(self):
        """获取分类个数"""
        return ArticleCategory.objects.all().count()
    get_category_nums.short_description = "分类个数"

    def get_article_nums(self):
        """文章个数"""
        return PageDetail.objects.all().count()
    get_article_nums.short_description = "文章个数"

    def get_comments_nums(self):
        """"""
        # TODO: 获取评论个数
        return 0
    get_comments_nums.short_description = "评论条数"

    def get_tag_nums(self):
        """获取标签个数"""
        return Tags.objects.all().count()
    get_tag_nums.short_description = "标签个数"

    def get_total_views(self):
        """网站访问量"""
        # 此处为方便使用sql内置函数使用原生sql
        cursor = connection.cursor()
        cursor.execute("select count(DISTINCT router, remote_addr, date(visited_time)) from blog_tracecount;")
        res = cursor.fetchone()
        return res[0]
    get_total_views.short_description = "网站访问量"


class ArticleCategory(models.Model):
    """分类集"""
    name = models.CharField(max_length=20, default='', verbose_name="分类名称")

    class Meta:
        verbose_name_plural = verbose_name = "分类集"

    def __str__(self):
        return self.name

    def get_counts(self):
        """获取当前分类的数量"""
        return PageDetail.objects.filter(category__name=self.name).count()


class PageDetail(models.Model):
    """页面详情"""
    title = models.CharField(max_length=20, verbose_name="标题")
    category = models.ForeignKey(ArticleCategory, verbose_name="分类", on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, verbose_name="文章作者", on_delete=models.CASCADE)
    comments = models.IntegerField(default=0, verbose_name="评论数")
    views = models.IntegerField(default=0, verbose_name="访问数")
    detail = UEditorField(verbose_name="文章详情", width=600, height=300, imagePath="page/ueditor/",
                          filePath="page/ueditor", default='')
    image = models.ImageField(verbose_name="封面图", upload_to="posts/%Y/%m", max_length=100)
    is_lunbo = models.BooleanField(verbose_name="是否轮播", default=False)
    tags = models.CharField(default='', verbose_name="标签", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发布日期")

    class Meta:
        verbose_name_plural = verbose_name = "文章"

    def __str__(self):
        return self.title

    def get_tag_ids(self):
        tag_maps = TagsMap.objects.filter(article=self.id)
        self.tag_ids = [tag_map.tag.id for tag_map in tag_maps]
        return self.tag_ids


class Tags(models.Model):
    """标签表"""
    tag_name = models.CharField(max_length=12, verbose_name="标签")

    class Meta:
        verbose_name_plural = verbose_name = "标签集"

    def get_nums(self):
        """获取标签个数"""
        return TagsMap.objects.filter(tag__tag_name=self.tag_name).count()
    get_nums.short_description = "引用个数"

    def __str__(self):
        return self.tag_name


class TagsMap(models.Model):
    """标签映射表"""
    tag = models.ForeignKey(Tags, verbose_name="标签", on_delete=models.CASCADE)
    article = models.ForeignKey(PageDetail, verbose_name="文章", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = verbose_name = "标签映射集"

    def __str__(self):
        return "[{}]:[{}]".format(self.tag, self.article)


class Archiving(models.Model):
    """文章归档"""
    year = models.IntegerField(default=date.today().year, verbose_name="归档年份")
    month = models.IntegerField(default=date.today().month, verbose_name="归档月份")

    class Meta:
        verbose_name_plural = verbose_name = "文章归档"

    def __str__(self):
        return "{}:{}".format(self.year, self.month)

    def get_nums(self):
        return PageDetail.objects.filter(add_time__year=self.year, add_time__month=self.month).count()
    get_nums.short_description = "文章数量"


class Message(models.Model):
    """留言板"""
    message = models.CharField(max_length=500, verbose_name="留言", default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="留言时间")

    class Meta:
        verbose_name_plural = verbose_name = "留言"

    def __str__(self):
        return self.message[:6]


class TraceCount(models.Model):
    """网站访问统计"""
    method = models.CharField(max_length=8, verbose_name="访问方式", default="GET")
    router = models.CharField(max_length=50, verbose_name="访问路由")
    remote_addr = models.CharField(max_length=20, verbose_name="ip地址")
    visited_time = models.DateTimeField(default=datetime.now, verbose_name="访问时间")

    class Meta:
        verbose_name_plural = verbose_name = "网站访问统计"

    def __str__(self):
        return "{remote_addr}:{router}".format(remote_addr=self.remote_addr, router=self.router)
