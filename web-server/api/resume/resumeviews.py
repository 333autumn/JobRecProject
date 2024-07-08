import numpy as np
import pandas as pd
import json
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import user, Logs, UserResume
from .serializers import *
from ..job.jobviews import recommender


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限

        if request.method == 'DELETE':
            return False
        else:
            return True
            # return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
        return obj.user == request.user


class ResumeFilter(filters.FilterSet):
    worktype = filters.CharFilter(field_name='worktype', lookup_expr='icontains')
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = UserResume
        # fields = '__all__'
        fields = ['worktype', 'username', ]


class UserResumeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # 搜索
    # filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    search_fields = ('username',)
    # # 排序
    # ordering_fields = ('create_time', 'last_update')
    # 过滤器
    filterset_class = ResumeFilter
    permission_classes = [CustomPermission]
    queryset = UserResume.objects
    serializer_class = UserResumeSerializer

    def perform_create(self, serializer):
        # Add a log entry for creating an order
        # 获取访问用户的ID
        u = user.objects.get(id=self.request.user.id)
        serializer.validated_data['user'] = u
        instance = serializer.save()

        Logs.objects.create(user=u, active='新增简历', content=instance.to_json())

    def perform_update(self, serializer):
        # Add a log entry for updating an order

        instance = self.get_object()
        serializer.save()
        user = self.request.user
        Logs.objects.create(user=user, active='更新简历', content=instance.to_json())

    @action(detail=False, methods=['POST'])
    def uploadPhoto(self, request):  # 上传图片
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        try:
            serializer = PhotoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)
            else:
                data['code'] = -1
                data['msg'] = '文件为空'
        except Exception as e:
            data['code'] = -1
            data['msg'] = str(e)
        return Response(data)

    @action(detail=False, methods=['POST'])
    def changebaseinfo(self, request):  # 编辑用户信息
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        try:
            serializer = baseinfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.update(request.user, serializer.validated_data)

            else:
                data['code'] = -1
                data['msg'] = f'{serializer.errors}'
        except Exception as e:
            data['code'] = -1
            data['msg'] = str(e)
        return Response(data)

    @action(detail=False, methods=['POST'])
    def changeresumeinfo(self, request):  # 编辑简历信息
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        try:
            serializer = resumeinfoSerializer(data=request.data)
            OBJ = UserResume.objects.filter(user=request.user).first()
            if serializer.is_valid():
                serializer.update(OBJ, serializer.validated_data)

            else:
                data['code'] = -1
                data['msg'] = f'{serializer.errors}'
        except Exception as e:
            data['code'] = -1
            data['msg'] = str(e)
        return Response(data)

    @action(detail=False, methods=['POST'])
    def changereadme(self, request):
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        try:
            serializer = readmeSerializer(data=request.data)
            OBJ = UserResume.objects.filter(user=request.user).first()
            if serializer.is_valid():
                serializer.update(OBJ, serializer.validated_data)

            else:
                data['code'] = -1
                data['msg'] = f'{serializer.errors}'
        except Exception as e:
            data['code'] = -1
            data['msg'] = str(e)
        return Response(data)

    @action(detail=False, methods=['GET'])
    def resumeinfo(self, request):  # 获取简历信息
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        try:
            data['data'] = self.get_queryset().filter(user=request.user).first().to_dict()
        except Exception as e:
            data['code'] = -1
            data['msg'] = str(e)
        return Response(data)

    @action(detail=False, methods=['GET'])
    def resumeList(self, request):  # 获取人才列表
        queryset = UserResume.objects.all()
        serializer = UserResumeSerializer(queryset, many=True)
        data = {
            'code': '200',
            'data': serializer.data,
            'msg': 'ok',
        }
        return Response(data)

    @action(detail=False, methods=['POST'])  # TODO 搜索人才 未实现模糊查询
    def search(self, request):
        key = request.data.get('key')
        eduHighestLevel = request.data.get('eduHighestLevel')
        workingexpCode = request.data.get('workingexpCode')
        # 设置查询字段
        queryset = UserResume.objects.filter(eduHighestLevel=eduHighestLevel, workingexpCode=workingexpCode).all()
        serializer = UserRecommendSerializer(queryset, many=True)
        return Response({'msg': 'OK', 'code': '200', 'data': serializer.data})

    # http://127.0.0.1:8080/api/data/resume/recommend/
    @action(detail=False, methods=['GET'])  # TODO 向职位推荐人才
    def recommend(self, request):

        input_id = "916101316838525277"  # 获取当前的职位id

        # 调用模型进行推荐
        recommendations = recommender.recommend_users_for_job(input_id, num_recommendations=5)
        user_ids = []
        for recommendation in recommendations:
            userid = recommendation[0]
            user_ids.append(int(userid))

        # CSV文件路径
        csv_file_path = r'D:\1-work-code\Employment_referral\web-server\xdu_dataset\xdu_dataset_user.csv'

        # 读取CSV文件
        df = pd.read_csv(csv_file_path)

        # 定义一个用来保存工作对象的列表
        users_list = []

        if len(user_ids) == 0:  # 调用冷启动模型
            # 读取 xdu_dataset_user.xlsx
            job_df = pd.read_excel('data/xdu/xdu_dataset_job.xlsx')

            # 根据 SID 获取 MAJOR 字段值
            job_row = job_df[job_df['DWZZJGDM'] == input_id]

            DWHYMC = job_row['DWHYMC'].values[0]

            # 读取 major_trans.txt
            with open('data/xdu/DWHYMC_trans.txt', 'r', encoding='utf-8') as f:
                DWHYMC_trans = dict(line.strip().split(' ') for line in f)

            # 获取映射后的 MAJOR 值
            mapped_DWHYMC = DWHYMC_trans.get(DWHYMC)

            # 读取 recommend_result 文件
            with open('data/xdu/recommend_result_com', 'r') as f:
                recommend_result = json.load(f)

            # 获取推荐列表
            recommend_list = recommend_result.get(mapped_DWHYMC)

            # 取推荐列表长度和10的较小值
            top_n = min(len(recommend_list), 10)
            top_recommendations = recommend_list[:top_n]

            # 读取 xdu_dataset_job.xlsx
            user_df = pd.read_excel('data/xdu/xdu_dataset_user.xlsx')

            # 打印推荐结果
            for rec in top_recommendations:

                user_dict = user_df[user_df['SID'] == int(rec)]
                # 这里可以根据需要创建自定义对象或直接使用字典
                obj = {
                    'sid': user_dict['SID'],
                    'realname': user_dict['REALNAME'],
                    'age': user_dict['GRADE'],
                    'department': user_dict['DEPARTMENT'],
                    'major': user_dict['MAJOR'],
                    'zyfx': user_dict['ZYFX'],
                    'sex': user_dict['XBMC'],
                    'zxwyyzmc': user_dict['ZXWYYZMC'],
                    'birthday': user_dict['BIRTHDAY'],
                    'xlmc': user_dict['XLMC'],
                    'xxxsmc': user_dict['XXXSMC'],
                    'address': user_dict['JTDZ'],
                    'gzzwlbmc': user_dict['GZZWLBMC'],
                }
                users_list.append(obj)

        else:  # 调用推荐模型
            # 遍历ID列表，找到对应的行，并保存为对象
            for user_id in user_ids:
                # print(user_id)
                # 假设CSV文件中有名为'user_id'的列
                user_row = df[df['SID'] == user_id]

                # 检查是否找到了对应的行
                if not user_row.empty:
                    # 将DataFrame的行转换为字典
                    user_dict = user_row.to_dict(orient='records')[0]
                    # 这里可以根据需要创建自定义对象或直接使用字典
                    obj = {
                        'sid': user_dict['SID'],
                        'realname': user_dict['REALNAME'],
                        'age': user_dict['GRADE'],
                        'department': user_dict['DEPARTMENT'],
                        'major': user_dict['MAJOR'],
                        'zyfx': user_dict['ZYFX'],
                        'sex': user_dict['XBMC'],
                        'zxwyyzmc': user_dict['ZXWYYZMC'],
                        'birthday': user_dict['BIRTHDAY'],
                        'xlmc': user_dict['XLMC'],
                        'xxxsmc': user_dict['XXXSMC'],
                        'address': user_dict['JTDZ'],
                        'gzzwlbmc': user_dict['GZZWLBMC'],
                    }
                    users_list.append(obj)
                else:
                    print(f"No user found with ID: {user_id}")

        data = {
            'code': '200',
            'data': users_list,
            'msg': 'ok',
            'count': 200
        }

        return Response(data)
