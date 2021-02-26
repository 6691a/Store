

from pathlib import Path
import config.__setting__ as setting
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = setting.SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'storages',
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.naver',
    'django_summernote',
    'six',


    'user',
    'store',
    'cart',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # CORS 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



DATABASES = setting.DATABASES


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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False




# CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000' ,'http://localhost:3000']
# CORS_ALLOW_CREDENTIALS = True

# user custom
AUTH_USER_MODEL = 'user.User'

# AWS S3
AWS_ACCESS_KEY_ID = setting.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = setting.AWS_SECRET_ACCESS_KEY
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'store-static-server'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION
)

# f's3.{AWS_REGION}.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'


# 파일 캐시 유지 시간
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# 같은 파일이 들어오면 덮어 쓰지 말라는 의미
AWS_S3_FILE_OVERWRITE = False

# 외부 접근 허용
AWS_DEFAULT_ACL = 'public-read'

AWS_LOCATION = ''

# AWS S3 사용을 위해 수정
STATIC_URL = 'http://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# 스토리지 기법
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 개발용
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]




#Media file 설정

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#static을 제외한 파일을 어디에 저장할 것 인가
DEFAULT_FILE_STORAGE = 'config.s3media.MediaStorage'


#소셜 로그인

#로그인을 누가 관리 할 건지
# AUTHENTICATION_BACKENDS = [
#     #기본 장고
#     'django.contrib.auth.backends.ModelBackend',
#     #소셜 로그인
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

SITE_ID = 1

#로그인 이후 이동  페이지
LOGIN_URL = 'user:login'



# gmail
EMAIL_HOST = 'smtp.gmail.com' 		     
EMAIL_PORT = '587'                     
EMAIL_HOST_USER = setting.EMAIL_HOST_USER 	 
EMAIL_HOST_PASSWORD = setting.EMAIL_HOST_PASSWORD		 
EMAIL_USE_TLS = True			    
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
	