from fabric.api import task
from fabric.api import cd
from fabric.api import env
from fabric.api import prefix
from fabric.api import sudo
from fabric.api import run

env.user = 'esvdev'
env.hosts = ['24.199.124.168']


def deploy():
    with cd('/home/esvdev/projects/blog_wagtail/esvdev_blog_wagtail/esvdev_blog'):
        run('git pull')
        run('pipenv shell')

        with cd('/home/esvdev/projects/blog_wagtail/esvdev_blog_wagtail/esvdev_blog'):
            run('pip install -r requirements.txt')
            run('python manage.py migrate')

        sudo('systemctl restart blog')
        sudo('systemctl restart nginx')