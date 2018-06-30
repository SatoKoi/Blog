# -*- coding:utf-8 -*-
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVarifyRecord, UserProfile


class UserProfileAdmin(UserAdmin):

    def get_form_layout(self):
        """自定义后台字段顺序"""
        if self.org_obj:
            from xadmin.layout import Main
            from xadmin.layout import Fieldset
            from django.utils.translation import ugettext as _
            from xadmin.layout import Row
            from xadmin.layout import Side
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             'first_name', 'last_name',
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        # 调用UserAdmin中的Mro父集方法
        return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):
    enable_themes = True        # 允许使用xadmin主题
    use_bootswatch = True       # 添加xadmin提供的多种主题


class GlobalSetting(object):
    site_title = "后台管理系统"     # 后台标题
    site_footer = "KoiSato"         # 后台引脚 @ xxx
    menu_style = "accordion"           # 收起每个app下的数据库


class EmailVarifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']  # 后台默认根据这些字段进行展示
    search_fields = ['code', 'email', 'send_type']              # 后台根据这些字段进行搜索
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 后台根据这些字段进行筛选
    model_icon = 'fa fa-address-book-o'                          # 自定义后台管理系统图标icon, 使用的是font-awesome第三方开源库


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVarifyRecord, EmailVarifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)