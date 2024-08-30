from django.contrib.auth.models import User, Group
from django.core.signals import request_started
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.dispatch import Signal

from .models import Post

my_signal = Signal()



@receiver(post_save, sender=User)
def add_user_group(sender, instance,created, **kwargs):
    if created:
        group = Group.objects.get(name='Группа 1')
        instance.groups.add(group)



@receiver(pre_save, sender=Post)
def change_status_df(sender, instance, **kwargs):
    instance.status = 'DF'


@receiver(my_signal)
def show_args(sender, param1, **kwargs):
    print(param1)


@receiver(post_save, sender=User)
def post_save_user(created ,**kwargs):
    instance = kwargs['instance']
    if created:
        print(f'Юзер {instance.username} создан')
    else:
        print(f'Юзер {instance.username} обновлен')



@receiver (request_started)
def log_request(sender, environ, **kwargs):
    method = environ['REQUEST_METHOD']
    host = environ['HTTP_HOST']
    path = environ ['PATH_INFO']
    query = environ['QUERY_STRING']
    query = '?' + query if query else ''
    print('New Request -> {method} {host}{path}{query}'.format(
        method=method,
        host=host,
        path=path,
        query=query,
    ))