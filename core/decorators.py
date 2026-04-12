from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def eh_aluno(user):
    return hasattr(user, 'aluno')


def eh_personal(user):
    return not hasattr(user, 'aluno')

def apenas_aluno(view_func):
    return user_passes_test(
        eh_aluno,
        login_url ='core:login'
    )(view_func)

def apenas_personal(view_func):
    return user_passes_test(
        eh_personal,
        login_url='core:login'
    )(view_func)