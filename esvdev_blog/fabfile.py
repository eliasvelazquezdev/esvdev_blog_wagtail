from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import sudo
from fabric.api import run
from fabric.api import get

env.user = 'esvdev'
env.hosts = ['24.199.124.168']


def deploy():
    with cd('/home/esvdev/projects/blog_wagtail/esvdev_blog_wagtail/esvdev_blog'):
        run('git pull')
        run('pipenv run pip install -r requirements.txt')
        run('pipenv run python manage.py migrate')

    sudo('systemctl restart blog')
    sudo('systemctl restart nginx')

@task(alias='get-log')
def download_error_log():
    sudo ('tail -n 20 /var/log/nginx/error.log.1 > tmp.log')

    get(
        local_path="/home/esvdev/Programacion/Python/Proyectos/Blog/blog_wagtail/error_log.log",
        remote_path="/home/esvdev/tmp.log"
    )

    sudo ('rm tmp.log')