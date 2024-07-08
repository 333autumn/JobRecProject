from django.urls import path, include
from api.company.companyviews import CompanyViewSet
from rest_framework.routers import DefaultRouter
"""
实现了将 CompanyViewSet 视图集的 URL 映射配置到 Django 项目中。
当 Django 项目收到对 company 资源的 HTTP 请求时，
将会调用 CompanyViewSet 视图集中相应的方法进行处理，并返回相应的数据结果。
"""
router = DefaultRouter()
router.register(r'company', CompanyViewSet)
urlpatterns = [
]
urlpatterns += router.urls
