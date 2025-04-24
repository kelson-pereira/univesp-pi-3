# univesp-pi-3

## UNIVESP, 2025

Projeto Integrador em Computação III - Grupo 4

### Comandos de instalação do python3:

`brew upgrade && brew update && brew install python3 && brew cleanup phyton3 && python3 --version`

### Comandos de instalação do django e demais componentes:

### Comandos de inicialização do projeto:

`pip3 freeze`

`django-admin startproject univesp_pi_3`

`mv univesp_pi_3 univesp-pi-3 && cd univesp-pi-3`

`django-admin startapp plantio`

### Comandos para execução do projeto localmente:

`cd univesp-pi-3`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py collectstatic --noinput --clear`

`python3 manage.py runserver 0.0.0.0:8000`

### Comandos para recriar o banco:

`cd univesp-pi-3`

`find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`

`find . -path "*/migrations/*.pyc" -delete`

`find . -path "*/db.sqlite3" -delete`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

### Comandos para criar banco de dados na plataforma Heroku:

`heroku login`

`heroku run python manage.py makemigrations --app plantio`

`heroku run python manage.py migrate --app plantio`

### Comandos de debug na Heroku:

`heroku logs --tail --app plantio`

### Comandos de teste:
