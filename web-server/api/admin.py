from django.contrib import admin
from api.models import *
from django.contrib.admin import DateFieldListFilter

"""
后台管理模块
"""
# 注册模型
admin.site.site_header = '后台管理'
admin.site.site_title = '后台管理'


# 在后台管理中注册模型
@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    # 展示的列表
    list_display = ('username', 'email', 'last_login')  # list
    # 搜素字段
    search_fields = ('username',)
    # 排序字段
    ordering = ['-date_joined']
    # 筛选字段
    list_filter = [('date_joined', DateFieldListFilter)]


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('user', 'active', 'content', 'create_time')  # list
    search_fields = ('user__username',)
    ordering = ['-create_time']
    list_filter = [('create_time', DateFieldListFilter), 'active']


@admin.register(ClickJobs)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cid', 'user', 'job', 'count', 'create_time', 'last_update')  # list
    search_fields = ('user', 'job')
    ordering = ['-create_time', '-last_update']
    list_filter = ['user']


@admin.register(StarJobs)
class UserAdmin(admin.ModelAdmin):
    list_display = ('sid', 'user', 'job', 'create_time')  # list
    search_fields = ('user', 'job')
    ordering = ['-create_time']
    list_filter = ['user']


@admin.register(CommentJobs)
class UserAdmin(admin.ModelAdmin):
    list_display = ('cid', 'user', 'job', 'create_time')  # list
    search_fields = ('user', 'job')
    ordering = ['-create_time']
    list_filter = ['user']


@admin.register(Recommendforallusers)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'recommendations')  # list
    search_fields = ('user_id',)
    list_filter = ['user_id']


# 公司
@admin.register(company)
class UserAdmin(admin.ModelAdmin):
    list_display = ('companynumber', 'job_num', 'companyurl', 'property', 'job_num')  # list
    search_fields = ('companynumber',)
    list_filter = ['property']


@admin.register(UserResume)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'eduHighestLevelTranslation', 'workingexp', 'worktype', 'workcityTranslation',
        'workcity2Translation',
        'workcity3Translation', 'subjobtypelevel', 'skilllabel', 'property', 'preferredSalaryMin',
        'preferredSalaryMax')  # list
    search_fields = ('user__username',)
    ordering = ['-created_time', '-last_update']
    list_filter = ['user', 'eduHighestLevelTranslation', 'workingexp', 'worktype', 'workcityTranslation',
                   'workcity2Translation', 'workcity3Translation', 'subjobtypelevel', 'skilllabel', 'property']


@admin.register(hotjobs_TOP20)
class UserAdmin(admin.ModelAdmin):
    list_display = ('job_id',)  # list


@admin.register(Jobs)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'number', 'name', 'education', 'workingexp', 'worktype', 'workcity', 'subjobtypelevel', 'skilllabel',
        'property', 'salary_min', 'salary_max')  # list
    search_fields = ('name',)
    ordering = ['-publishtime']
