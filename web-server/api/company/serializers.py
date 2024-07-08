from rest_framework import serializers
from api.models import company

"""
序列化模型类
将数据转换为json形式
"""


class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        # 要转化的字段
        # __all__表示所有字段
        fields = '__all__'
        # exclude = ['user']
