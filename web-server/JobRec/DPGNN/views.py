# DPGNN/views.py
from django.http import HttpResponse
from .model.prediction import JobRecommender

# 初始化推荐系统
# recommender = JobRecommender(config_file='zhilian', checkpoint_path='./model/saved/DPGNN-Jun-19-2024_11-51-39.pth')
recommender = JobRecommender(config_file='xdu',
                             checkpoint_path=r'D:\1-work-code\JobRecProject_v1\JobRec\DPGNN\model\saved\xdu-1w.pth')

# def recommend(request):
#     if request.method == "POST":
#         user_id = request.POST.get('user_id')
#         recommendations = recommender.recommend_jobs_for_user(user_id,10)
#         return render(request, 'DPGNN/result.html', {'recommendations': recommendations})
#     else:
#         return render(request, 'DPGNN/index.html')

from django.shortcuts import render
from .forms import RecommendationForm


def recommend(request):
    recommendations = []
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            # 推荐类型
            recommendation_type = form.cleaned_data['recommendation_type']
            # 传入的id
            input_id = form.cleaned_data['input_id']

            if recommendation_type == '1':
                recommendations = recommender.recommend_jobs_for_user(input_id, num_recommendations=5)
            elif recommendation_type == '2':
                recommendations = recommender.recommend_users_for_job(input_id, num_recommendations=5)
    else:
        form = RecommendationForm()

    return render(request, 'DPGNN/result.html', {'form': form, 'recommendations': recommendations})


def index(request):
    return HttpResponse("Hello, world. You're at the DPGNN index.")
