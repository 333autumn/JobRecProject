
from pathlib import Path
import os,datetime
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w8%uz78aq9r&jcq8pg8o#q8^9vjl507y94v=bhk0fqjta1gg(o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG==False:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobfree',  #recruit_info
        'USER': 'root',  # os.environ.get('DJANGO_MYSQL_USER')
        'PASSWORD': 'root',  # os.environ.get('DJANGO_MYSQL_PASSWORD')
        'HOST': '127.0.0.1',  # os.environ.get('DJANGO_MYSQL_HOST')
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'},
    },

    }
    EMAIL_PORT = 587 # SMTP端口号
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # 自动重定向到安全连接
    # SECURE_SSL_REDIRECT = True

    # 避免浏览器自作聪明推断内容类型（避免跨站脚本攻击风险）
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # 避免跨站脚本攻击(XSS)
    SECURE_BROWSER_XSS_FILTER = True

    # COOKIE只能通过HTTPS进行传输
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # 防止点击劫持攻击手段（不允许使用<iframe>标签进行加载）
    X_FRAME_OPTIONS = 'DENY'
    CORS_ALLOW_ALL_ORIGINS = False
else:
    CORS_ALLOW_ALL_ORIGINS = True
    EMAIL_PORT =25
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobfree',  #recruit_info
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4'},
    },

}
SIMPLEUI_HOME_PAGE = '/'
SIMPLEUI_LOGO ='/favicon.ico'
ALLOWED_HOSTS = ['*']
# APPEND_SLASH=False
# # Application definition
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS=True

# Application definition
SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['用户管理', '数据管理'],
    'menus': [
        # {
        #     'name': '其他工具',
        #     'icon': 'fas fa-wrench',
        #     'models': [
        #         {
        #             'name': '目录编排',
        #             'icon': 'fas fa-folder-open',
        #             'url': '/home/#/directory/'
        #         }
        #     ]
        # },

        {
            'name':'用户管理',
            'models': [
                {
                    'name': '用户信息',
                    'url':'/adminapi/user/'
                    
                },
                {
                    'name': '用户画像信息',
                    'url':'/adminapi/userresume/'
                    
                },
                {
                    'name': '用户推荐',
                    'url':'/adminapi/recommendforallusers/'
                    
                },
                {
                    'name': '收藏',
                    'url':'/adminapi/starjobs/'
                    
                },
                {
                    'name': '评论',
                    'url':'/adminapi/commentjobs/'
                    
                },
                {
                    'name': '浏览',
                    'url':'/adminapi/clickjobs/'
                    
                },
            ]
        },
        {
            'name':'数据管理',
            'models':[
                {
                    'name': '热门岗位',
                    'url':'/adminapi/hotjobs_top20/'
                },
                {
                    'name': '岗位列表',
                    'url':'/adminapi/jobs/'
                },
                {
                    'name': '企业列表',
                    'url':'/adminapi/company/'
                }
            ]
        }
    ]
}
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'corsheaders',
    'api'
]
AUTH_USER_MODEL='api.user'
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 白名单域名列表：即前端网址在以下列表中，均可向此后端drf发送请求；
# 全允许：CORS_ALLOW_ALL_ORIGINS = True，仅开发环境用
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

# 最后面添加白名单请求头字段，非以下请求头字段均被过滤掉
# 自己家的请求头字段都必须加，否则均丢失，下面是默认的，
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Authorization",
    'Cookie'
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

 
REST_FRAMEWORK = {
 
    # 权限认证
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    # 身份验证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/m',  # 匿名用户每分20次请求
        'user': '10000/m',  # 用户每分50次请求
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # 指定每页的数据数量
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    
}
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_LIFETIME': datetime.timedelta(minutes=10),  # 设置令牌有效期
    'TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=7),  # 设置刷新令牌有效期
}



APPEND_SLASH=False
ROOT_URLCONF = 'DRF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DRF.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases



# SMTP邮箱设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''  # 邮箱SMTP服务器地址
EMAIL_HOST_USER = ''  # 邮箱用户名
EMAIL_HOST_PASSWORD = ''  # 邮箱密码
# EMAIL_USE_TLS = True  # 使用TLS加密
DEFAULT_FROM_EMAIL = ''  # 默认发件人邮箱
#redis
REDIS_HOST='redis'
REDIS_PORT=6379
REDIS_PSW=''
REDIS_DB=1
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'


TIME_ZONE = 'Asia/Shanghai'
 
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if DEBUG==False:
    STATIC_URL = '/assets/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static') ## 新增行
    # STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, '/static/'), ##修改地方
    # ]
else:
    STATIC_URL = '/assets/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR,'static'),
    )
# 配置 MEDIA_ROOT 作为你上传文件在服务器中的基本路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload') # 注意此处不要写成列表或元组的形式
# 配置 MEDIA_URL 作为公用 URL，指向上传文件的基本路径
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
