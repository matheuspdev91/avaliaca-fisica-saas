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
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'aluno'):
            return redirect('core:painel_aluno', aluno_id=request.user.aluno.id)
        return view_func(request, *args, **kwargs)
    return wrapper