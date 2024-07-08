import random
import pandas as pd
import json

from django.db.models import *
from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import *
from .serializers import *
from JobRec.DPGNN.model.prediction import JobRecommender

# 初始化模型
# recommender = JobRecommender(config_file='xdu',
#                              checkpoint_path=r'D:\1-work-code\JobRecProject_v1\JobRec\DPGNN\model\saved\xdu-1w.pth')
recommender = JobRecommender(config_file='xdu',
                             checkpoint_path=r'JobRec\DPGNN\model\saved\xdu-1w.pth')


class SimilarJobsList(generics.ListAPIView):
    serializer_class = JobsSerializer

    def get_queryset(self):
        number = self.kwargs.get('number')
        job = Jobs.objects.get(number=number)

        query = (
                Q(industryname=job.industryname) &
                Q(education=job.education) &
                Q(worktype=job.worktype) &
                Q(workcity=job.workcity) &
                Q(educationcode__gte=job.educationcode) &
                Q(salary_min__lte=job.salary_min) &
                Q(salary_max__gte=job.salary_max)
        )

        similar_jobs = Jobs.objects.filter(query).exclude(number=number)
        return similar_jobs


def get_random_objects(queryset, num_objects):
    random_objects = []
    total_objects = queryset.count()
    if num_objects >= total_objects:
        return list(queryset)
    while len(random_objects) < num_objects:
        random_index = random.randint(0, total_objects - 1)
        random_object = queryset[random_index]
        if random_object not in random_objects:
            random_objects.append(random_object)
    return random_objects


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 在这里编写权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
        if request.method == 'GET' or (request.method == 'POST'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # 在这里编写对象级别的权限逻辑，返回 True 表示有权限，返回 False 表示没有权限
        return True


class JobsFilter(filters.FilterSet):
    # jobid = filters.CharFilter(lookup_expr='exact')
    number = filters.CharFilter(lookup_expr='exact')
    # 职位名模糊查询
    name = filters.CharFilter(lookup_expr='icontains')
    educationcode = filters.CharFilter(lookup_expr='exact')
    # industrycompanytags = filters.CharFilter(lookup_expr='exact')
    # industryname = filters.CharFilter(lookup_expr='icontains')
    # jobsummary = filters.CharFilter(lookup_expr='exact')
    # positionurl = filters.CharFilter(lookup_expr='exact')
    # positionsourcetypeurl = filters.CharFilter(lookup_expr='exact')
    # property = filters.CharFilter(lookup_expr='exact')
    propertycode = filters.CharFilter(lookup_expr='exact')
    # recruitnumber = filters.CharFilter(lookup_expr='exact')
    # salary60 = filters.CharFilter(lookup_expr='exact')
    # salaryreal = filters.CharFilter(lookup_expr='exact')
    # salarytype = filters.CharFilter(lookup_expr='exact')
    # salarycounte = filters.CharFilter(lookup_expr='exact')
    salary = filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary2 = filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    # skilllabel = filters.CharFilter(lookup_expr='icontains')
    publishtime = filters.DateFromToRangeFilter()
    cityid = filters.CharFilter(lookup_expr='icontains')
    citydistrict = filters.CharFilter(lookup_expr='exact')
    # streetid = filters.CharFilter(lookup_expr='icontains')
    # streetname = filters.CharFilter(lookup_expr='exact')
    subjobtypelevel = filters.CharFilter(lookup_expr='exact')
    # subjobtypelevelname = filters.CharFilter(lookup_expr='icontains')
    # 待遇
    # welfaretaglist = filters.CharFilter(lookup_expr='icontains')
    # workcity = filters.CharFilter(lookup_expr='exact')
    # 兼职全职..
    worktypecode = filters.NumberFilter(lookup_expr='exact')
    # 工作经验
    workingexpcode = filters.NumberFilter(lookup_expr='exact')

    # companyid = filters.CharFilter(lookup_expr='exact')
    # companynumber = filters.CharFilter(lookup_expr='exact')
    # 	# companyscaletypetagsnew = filters.CharFilter(lookup_expr='exact')
    # companyname = filters.CharFilter(lookup_expr='exact')
    # rootcompanynumber = filters.CharFilter(lookup_expr='exact')
    # companylogo = filters.CharFilter(lookup_expr='exact')
    # companysize = filters.CharFilter(lookup_expr='exact')
    # companyurl = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Jobs
        fields = '__all__'


# job模型类
class JobsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # 搜索
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('name',)
    # 排序
    ordering_fields = ('publishtime',)
    # 过滤器
    filterset_class = JobsFilter
    permission_classes = [CustomPermission]
    queryset = Jobs.objects
    serializer_class = JobsSerializer
    lookup_field = 'number'

    # detail=False表示处理整个资源集合
    # detail=True表示处理单个资源，需要传入资源的主键
    @action(detail=False, methods=['POST'])
    def comment(self, request):  # 新增评论
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = CollectSerializer(data=request.data)
                content = request.data.get('content')
                if serializer.is_valid() and content:
                    number = serializer.validated_data.get('number')
                    job = Jobs.objects.filter(number=number).first()
                    # 新增到数据库
                    Comment = CommentJobs.objects
                    Comment.create(user=request.user, job=job, content=content)

                    data['data'] = 'ok'
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['GET'])
    def commentJobs(self, request):  # 获取对应职位的评论列表
        data = {
            'code': '200',
            'data': [],
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = RecommendSerializer(data=request.GET)
                number = request.GET.get('number')
                if serializer.is_valid() and number:
                    page = serializer.validated_data.get('page')
                    pagesize = serializer.validated_data.get('pagesize')
                    t = Jobs.objects.get(number=number)
                    job_list = [
                        {'id': i.cid, 'username': i.user.username, 'content': i.content, 'create_time': i.create_time}
                        for i in CommentJobs.objects.filter(job=t).order_by('-create_time')[
                                 (page - 1) * pagesize:page * pagesize]]
                    data['count'] = CommentJobs.objects.filter(job=t).count()
                    data['data'] = job_list
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['POST'])
    def click(self, request):  # 用户浏览工作
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = ClickSerializer(data=request.data)
                if serializer.is_valid():
                    number = serializer.validated_data.get('number')
                    job = Jobs.objects.filter(number=number).first()
                    cli = ClickJobs.objects
                    c = cli.filter(user=request.user, job=job)
                    if not c.exists():
                        cli.create(user=request.user, job=job)
                    c.update(count=F('count') + 1)
                    data['data'] = cli.filter(job=job).aggregate(sum=Sum('count'))
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            serializer = ClickSerializer(data=request.data)
            if serializer.is_valid():
                number = serializer.validated_data.get('number')
                cli = ClickJobs.objects
                job = Jobs.objects.filter(number=number).first()
                data['data'] = cli.filter(job=job).aggregate(sum=Sum('count'))
            else:
                data['code'] = '-1'
                data['msg'] = serializer.errors

        return Response(data)

    @action(detail=False, methods=['POST'])
    def clickTalents(self, request):  # TODO 公司浏览人才信息
        return Response()

    @action(detail=False, methods=['POST'])
    def collect(self, request):  # 收藏工作
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = CollectSerializer(data=request.data)
                if serializer.is_valid():
                    number = serializer.validated_data.get('number')
                    job = Jobs.objects.filter(number=number).first()
                    star = StarJobs.objects
                    if star.filter(user=request.user, job=job).exists():
                        data['code'] = '-1'
                        data['msg'] = '已收藏'
                        return Response(data)
                    # 新增到数据库
                    star.create(user=request.user, job=job)
                    data['data'] = job.to_dict('收藏')
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['GET'])
    def collectjobs(self, request):  # 收藏多个工作
        data = {
            'code': '200',
            'data': [],
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = RecommendSerializer(data=request.GET)
                if serializer.is_valid():
                    page = serializer.validated_data.get('page')
                    pagesize = serializer.validated_data.get('pagesize')
                    res = StarJobs.objects.filter(user=request.user)
                    job_list = [i.job.to_dict(None) for i in res[(page - 1) * pagesize:page * pagesize]]
                    data['count'] = res.count()
                    data['data'] = job_list
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['GET'])
    def clickjobs(self, request):  # 点击多个工作
        data = {
            'code': '200',
            'data': [],
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = RecommendSerializer(data=request.GET)
                if serializer.is_valid():
                    page = serializer.validated_data.get('page')
                    pagesize = serializer.validated_data.get('pagesize')
                    res = ClickJobs.objects.filter(user=request.user)
                    job_list = [i.job.to_dict(None) for i in res[(page - 1) * pagesize:page * pagesize]]
                    data['count'] = res.count()
                    data['data'] = job_list
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['POST'])
    def iscollected(self, request):  # 判断是否收藏
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = CollectSerializer(data=request.data)
                if serializer.is_valid():
                    number = serializer.validated_data.get('number')
                    job = Jobs.objects.filter(number=number).first()
                    star = StarJobs.objects
                    if star.filter(user=request.user, job=job).exists():
                        data['data'] = True
                        data['msg'] = '已收藏'
                        return Response(data)
                    data['data'] = False
                    data['msg'] = '未收藏'
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['POST'])
    def removecollect(self, request):  # 取消收藏
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        if request.user.is_authenticated:
            try:
                serializer = CollectSerializer(data=request.data)
                if serializer.is_valid():
                    number = serializer.validated_data.get('number')
                    job = Jobs.objects.filter(number=number).first()

                    star = StarJobs.objects
                    if not star.filter(user=request.user, job=job).exists():
                        data['code'] = '-1'
                        data['msg'] = '未收藏'
                        return Response(data)
                    star.filter(user=request.user, job=job).delete()
                    data['data'] = job.to_dict('取消收藏')
                else:
                    # 参数有误
                    data['code'] = '-1'
                    data['msg'] = serializer.errors
            except Exception as e:
                data['code'] = '-1'
                data['data'] = str(e)
                data['msg'] = '系统错误'
        else:
            data['code'] = -1
            data['msg'] = '请登录'
        return Response(data)

    @action(detail=False, methods=['GET'])
    def bigdata_info(self, request):  # 获取图表数据
        queryset = self.filter_queryset(self.get_queryset())
        data = {}
        # 不同公司的数量
        data['count'] = company.objects.aggregate(sum=Count('companyid')).values()
        # 总的公司数量
        data['total'] = queryset.aggregate(sum=Count('id')).values()
        return Response({'msg': 'OK', 'code': '200', 'data': data})

    @action(detail=False, methods=['GET'])
    def education_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(sum=Avg('salary_min')).values()
        data = queryset.filter(salary_min__gt=0).values('education').annotate(name=F('education'),
                                                                              sum=Avg('salary_min')).order_by('-sum')[
               :5]
        return Response({'msg': 'OK', 'code': '200', 'data': data, 'total': total})

    @action(detail=False, methods=['GET'])
    def worktype_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values('worktype').annotate(name=F('worktype'), value=Count('id')).order_by('-value')[:10]
        return Response({'msg': 'OK', 'code': '200', 'data': data})

    @action(detail=False, methods=['GET'])
    def property_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(sum=Avg('salary_min')).values()
        data = queryset.filter(salary_min__gt=0).values('property').annotate(name=F('property'),
                                                                             sum=Avg('salary_min')).order_by('-sum')[
               :10]
        return Response({'msg': 'OK', 'code': '200', 'data': data, 'total': total})

    @action(detail=False, methods=['GET'])
    def workcity_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.filter(salary_min__gt=0).values('workcity').annotate(name=F('workcity'),
                                                                             value=Sum('salary_min')).order_by(
            '-value')[:10]
        return Response({'msg': 'OK', 'code': '200', 'data': data})

    @action(detail=False, methods=['GET'])
    def test(self, request):  # 测试方法
        num = 10
        queryset = Jobs.objects.all()[:num]
        serializer = JobsSerializer(queryset, many=True)
        return Response({'msg': 'OK', 'code': '200', 'data': serializer.data})

    @action(detail=False, methods=['GET'])
    def companyJobs(self, request):  # TODO 获取企业发布的职位列表
        num = 10
        queryset = Jobs.objects.all()[:num]
        serializer = JobsSerializer(queryset, many=True)
        return Response({'msg': 'OK', 'code': '200', 'data': serializer.data})

    @action(detail=False, methods=['POST'])  # TODO 搜索职位 模糊搜索未实现
    def search(self, request):
        key = request.data.get('key')
        queryset = Jobs.objects.filter(name=key).all()[:10]
        serializer = JobsSerializer(queryset, many=True)
        return Response({'msg': 'OK', 'code': '200', 'data': serializer.data})

    @action(detail=False, methods=['POST'])
    def removeJob(self, request):  # 删除职位
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        id = request.data.get('id')
        Jobs.objects.filter(id=id).delete()
        return Response(data)

    @action(detail=False, methods=['POST'])
    def editJob(self, request):  # 编辑职位
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        job = Jobs.objects.get(id=request.data.get('id'))
        serializer = JobsSerializer(instance=job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data)

    @action(detail=False, methods=['POST'])
    def addJob(self, request):  # TODO 新增职位 和企业账户建立联系
        data = {
            'code': '200',
            'data': None,
            'msg': 'ok',
        }
        Jobs.objects.create(name=request.data.get('name'),
                            job_id=request.data.get('job_id'),
                            number=request.data.get('number'))
        return Response(data)

    # http://127.0.0.1:8080/api/data/jobs/recommend/
    @action(detail=False, methods=['GET'])
    def recommend(self, request):  # TODO 向用户推荐职位

        input_id = "20051212160"  # 获取当前登录的学生id

        # 调用模型进行推荐
        recommendations = recommender.recommend_jobs_for_user(input_id, num_recommendations=5)
        job_ids = []
        for recommendation in recommendations:
            jobid = recommendation[0]
            job_ids.append(jobid)

        # 定义一个用来保存工作对象的列表
        jobs_list = []

        if len(job_ids) == 0:  # 调用冷启动模型
            # 读取 xdu_dataset_user.xlsx
            user_df = pd.read_excel('data/xdu/xdu_dataset_user.xlsx')

            # 根据 SID 获取 MAJOR 字段值
            user_row = user_df[user_df['SID'] == input_id]

            major = user_row['MAJOR'].values[0]

            # 读取 major_trans.txt
            with open('data/xdu/major_trans.txt', 'r', encoding='utf-8') as f:
                major_trans = dict(line.strip().split(' ') for line in f)

            # 获取映射后的 MAJOR 值
            mapped_major = major_trans.get(major)

            # 读取 recommend_result 文件
            with open('data/xdu/recommend_job_result', 'r') as f:
                recommend_result = json.load(f)

            # 获取推荐列表
            recommend_list = recommend_result.get(mapped_major)

            # 取推荐列表长度和10的较小值
            top_n = min(len(recommend_list), 5)
            top_recommendations = recommend_list[:top_n]

            # 读取 xdu_dataset_job.xlsx
            job_df = pd.read_excel('data/xdu/xdu_dataset_job.xlsx')

            # 打印推荐结果
            for rec in top_recommendations:
                job_dict = job_df[job_df['DWZZJGDM'] == rec]
                job = {
                    'jobid': job_dict['DWZZJGDM'],
                    'companyname': job_dict['SJDWMC'],
                    'property': job_dict['DWXZMC'],
                    'industryname': job_dict['DWHYMC'],
                    'name': job_dict['GZZWLBMC'],
                    'workcity': job_dict['DWSZDDM'],
                }
                jobs_list.append(job)

        else:
            # CSV文件路径
            csv_file_path = r'D:\1-work-code\Employment_referral\web-server\xdu_dataset\xdu_dataset_job.csv'

            # 读取CSV文件
            df = pd.read_csv(csv_file_path)

            # 遍历ID列表，找到对应的行，并保存为对象
            for job_id in job_ids:
                # 假设CSV文件中有名为'job_id'的列
                job_row = df[df['DWZZJGDM'] == job_id]

                # 检查是否找到了对应的行
                if not job_row.empty:
                    # 将DataFrame的行转换为字典
                    job_dict = job_row.to_dict(orient='records')[0]

                    # 这里可以根据需要创建自定义对象或直接使用字典
                    job = {
                        'jobid': job_dict['DWZZJGDM'],
                        'companyname': job_dict['SJDWMC'],
                        'property': job_dict['DWXZMC'],
                        'industryname': job_dict['DWHYMC'],
                        'name': job_dict['GZZWLBMC'],
                        'workcity': job_dict['DWSZDDM'],
                    }
                    jobs_list.append(job)
                else:
                    print(f"No job found with ID: {job_id}")

        data = {
            'code': '200',
            'data': jobs_list,
            'msg': 'ok',
            'count': 200
        }

        return Response(data)
