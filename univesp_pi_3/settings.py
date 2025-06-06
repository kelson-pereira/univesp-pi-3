"""
Configurações do Django para o projeto univesp_pi_3.

Gerado por 'django-admin startproject' usando Django 5.1.7.

Para obter mais informações sobre este arquivo, consulte
https://docs.djangoproject.com/en/5.1/topics/settings/

Para obter a lista completa de configurações e seus valores, consulte
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import secrets

from pathlib import Path

import dj_database_url
import django_heroku
from celery.schedules import crontab

# Cria caminhos dentro do projeto como: BASE_DIR/'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Os arquivos de mídia enviados pelo usuário dependem de duas configurações:
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Configurações de desenvolvimento de início rápido – inadequadas para produção
# Consulte https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha em segredo a chave secreta usada na produção!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", default=secrets.token_urlsafe(nbytes=64)
)

# A variável de ambiente `DYNO` está definida na Heroku CI, mas não é um aplicativo Heroku real,
# então também temos que excluir explicitamente o CI:
# https://devcenter.heroku.com/articles/heroku-ci#immutable-environment-variables
IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

# AVISO DE SEGURANÇA: não execute com o debug ativado na produção!
if not IS_HEROKU_APP:
    DEBUG = True

# Na Heroku, é seguro usar um curinga para `ALLOWED_HOSTS`, pois o roteador Heroku realiza
# a validação do cabeçalho Host na solicitação HTTP recebida. Em outras plataformas,
# você pode precisar listar explicitamente os nomes de host esperados para evitar ataques
# de cabeçalho de host HTTP. Veja:
# https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-ALLOWED_HOSTS
if IS_HEROKU_APP:
    ALLOWED_HOSTS = ["*"]
    SECURE_SSL_REDIRECT = False
else:
    ALLOWED_HOSTS = ["127.0.0.1"]

# Definição da aplicação

INSTALLED_APPS = [
    # Use a implementação runserver do WhiteNoise em vez do padrão do Django, para paridade dev-prod.
    "whitenoise.runserver_nostatic",
    # Remova o comentário e a entrada em `urls.py` se desejar usar o recurso de administração do Django:
    # https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "plantio",
    "channels",
    'django_celery_beat',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # O Django não suporta servir ativos estáticos de maneira pronta para produção, então
    # usamos o excelente pacote WhiteNoise para fazer isso. O middleware WhiteNoise deve ser
    # listado após o `SecurityMiddleware` do Django para que os redirecionamentos de segurança
    # ainda sejam executados.
    # Veja: https://whitenoise.readthedocs.io
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "univesp_pi_3.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "univesp_pi_3.wsgi.application"
ASGI_APPLICATION = "univesp_pi_3.asgi.application"

REDIS_URL = os.environ.get("REDISCLOUD_URL", "redis://localhost:6379")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
    },
}

# Scheduler controls com Celery
CELERY_BROKER_URL = os.environ.get("REDISCLOUD_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.environ.get("REDISCLOUD_URL", "redis://localhost:6379")
CELERY_TIMEZONE = 'America/Sao_Paulo'

# Banco de dados
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if IS_HEROKU_APP:
    # Na produção na Heroku, a configuração do banco de dados é derivada da variável de ambiente
    # `DATABASE_URL` pelo pacote dj-database-url. `DATABASE_URL` será definido automaticamente
    # pela Heroku quando um complemento de banco de dados for anexado ao seu aplicativo Heroku. Veja:
    # https://devcenter.heroku.com/articles/provisioning-heroku-postgres
    # https://github.com/jazzband/dj-database-url
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        ),
    }
else:
    # Ao executar localmente em desenvolvimento ou em CI, um arquivo de banco de dados sqlite
    # será usado para simplificar a configuração inicial. A longo prazo, é recomendado usar o
    # Postgres localmente também.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Validação de senha
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internacionalização
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

# Utiliza cookies de sessão do usuário
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Arquivos estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Não armazene a versão original (nome de arquivo sem hash) de arquivos estáticos, para reduzir o tamanho do slug:
# https://whitenoise.readthedocs.io/en/latest/django.html#WHITENOISE_KEEP_ONLY_HASHED_FILES

WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Tipo de campo de chave primária padrão
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

django_heroku.settings(locals(), staticfiles=False)

AUTHENTICATION_BACKENDS = [
    'plantio.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
]

CSRF_TRUSTED_ORIGINS = [
    'https://plantio-74e808a068fc.herokuapp.com',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True