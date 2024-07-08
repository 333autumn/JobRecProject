from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import *
from .serializers import *


# 定义权限逻辑
class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
        if request.method == 'GET':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
        return True


# 定义了一些字段过滤器，用于过滤查询结果
class CompanyFilter(filters.FilterSet):
    # jobid = filters.CharFilter(lookup_expr='exact')
    companynumber = filters.CharFilter(lookup_expr='exact')
    industryCompanyTags = filters.CharFilter(lookup_expr='exact')
    job_num = filters.NumberFilter(field_name='job_num', lookup_expr='gte')
    # 公司名模糊查询
    companyname = filters.CharFilter(lookup_expr='icontains')
    propertycode = filters.CharFilter(lookup_expr='exact')
    property = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = company
        fields = '__all__'


"""
定义视图集类
通过这个视图集类，可以实现对公司模型的增删改查等操作，
并且根据定义的权限逻辑和过滤器对数据进行权限控制和过滤。
这样的视图集类可以作为 Django REST framework 中的一个 API 视图，用于处理前端发送的 HTTP 请求，并返回相应的数据结果。
"""


# 通过ModelViewSet自动实现增删改查操作
class CompanyViewSet(viewsets.ModelViewSet):
    # 认证
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # 搜索字段
    search_fields = ('companyname',)
    # 排序字段
    ordering_fields = ('job_num',)
    # 过滤器
    filterset_class = CompanyFilter
    # 权限
    permission_classes = [CustomPermission]
    # 从数据库查询数据
    queryset = company.objects
    # 序列化类
    serializer_class = companySerializer

    @action(detail=False, methods=['GET'])
    def test(self, request):
        queryset = company.objects.filter(companyname="搜狐公司")
        serializer = companySerializer(queryset, many=True)

        # for e in queryset:
        #     name = e.companyname
        #     c = queryset.filter(companyname=name)
        #     if len(c) >= 2:
        #         for temp in c[:-1]:
        #             queryset.filter(companyname=name).delete()

        return Response({'msg': 'OK', 'code': '200', 'data': serializer.data})
