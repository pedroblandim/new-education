from blog.models import Arvore, Tela, Usuario
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve
from django.http import HttpResponseForbidden

from django.contrib.auth import logout

# ajudar a debugar
def mostrarSession(request):
    print('Sessão:')
    for key, value in request.session.items():
        if key[0] != '_':
            print('{} => {}'.format(key, value))
    print('\n')

def MostrarSessionMiddleware(get_response):

    def middleware(request):
        response = get_response(request)
        # mostrarSession(request)
        return response
    return middleware

#=======================

def apagarSessao(request):
    keyArray = []
    # apaga dados da sessão mas sem logout
    for key, value in request.session.items():
        # não deletar keys que indicam login
        if key[0] != '_':
            keyArray.append(key)

    for key in keyArray:
        del request.session[key]


# middleware que impede atualização de árvores que já foram submetidas
def BloqueioDeAtualizacao(get_response):

    def middleware(request):
        if request.method == 'POST':
            requestedUrl = request.path
            requestedUrl = requestedUrl.split('/')
            if 'change' in requestedUrl and 'arvore' in requestedUrl:
                arv = Arvore.objects.get(pk=requestedUrl[-3])
                if arv.submetida:
                    messages.error(request, f'Não foi possível modificar a árvore {arv.id} pois esta já foi submetida a resposta.')
                    return redirect('/admin/blog/arvore')

        response = get_response(request)

        return response
    return middleware



def PermissaoTelas(get_response):

    def middleware(request):

        user = request.user

        # filtrar usuários sem tela_num, desautenticados ou superusuários
        try:
            tela_id = request.session['tela_num']
        except:
            response = get_response(request)
            return response

        if not(user.is_authenticated) or user.is_superuser:
            response = get_response(request)
            return response

        usuario = user.usuario
        arvore = Arvore.objects.get(pk=request.session['arvore'])
        response = get_response(request)

        if response.status_code == 304: # 304: nada mudou. Não saiu do questionário
            return response

        # os usuários que chegam até essa parte devem estar respondendo a um questionário
        view_requisitada = resolve(request.path).view_name

        if view_requisitada != 'blog:arvore' and view_requisitada != 'blog:resposta' :
            # requisitou url fora do questionário, portanto saiu
            usuario.arvores.add(arvore)   
            usuario.save()
            apagarSessao(request)
        return response

    return middleware

