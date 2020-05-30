from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Usuario, Resposta
from .models import Arvore, Question, Escolha, Raiz, Tela

from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required            # Limita o acesso de uma url apenas para usuários logados

def apagarSessao(request):
    keyArray = []
    # apaga dados da sessão mas sem fazer logout
    for key, value in request.session.items():
        # não deletar keys que indicam login
        if key[0] != '_':
            keyArray.append(key)

    for key in keyArray:
        del request.session[key]

def about(request):
	return render(request, 'blog/about_us.html')

def home(request):
    return render(request, 'blog/home.html')


@login_required
def arvore(request):

    usuario = request.user.usuario

    try:
        tela_atual = Tela.objects.get(pk=request.session['tela_atual']) 
    except:
        return redirect('/')

    escolhas = tela_atual.question.escolha_set.all()
    if tela_atual.video:
        url = tela_atual.video + '?autoplay=1&controls=0&disablekb=1&modestbranding=1&rel=0&showinfo=0'
    else:
        url = None
    context= {
        'tela':tela_atual,
        'escolhas': escolhas,
        'url_tela':url,
        'tela_num': request.session['tela_num']
    }

    # # Atualizar arvore para submetida
    # if tela_atual.arvore.submetida == False:
    #     tela_atual.arvore_do_dia.submetida = True
    #     tela_atual.arvore_do_dia.save()

    return render(request, 'blog/tela.html', context)

def arvoreConcluida(request):
    return render(request, 'blog/arvoreConcluida.html',{})

@login_required
def resposta(request):
    if request.method == 'GET':
        return redirect('/')

    usuario = request.user.usuario
    # verificar se está respondendo algum questionário
    try:
        tela = Tela.objects.get(pk=request.session['tela_atual'])
    except:
        messages.warning(request,'Você saiu do questionário.')
        return redirect('/')


    arvore      = tela.arvore
    question    = tela.question

    # ver se já existe um tempo inicial para a pergunta
    ini_tempo_num = 'ini_tempo' + str(request.session['tela_num'])

    try:
        request.session[ini_tempo_num]
    except:
        request.session[ini_tempo_num] = request.POST['ini_tempo']

    # verificar timeout
    if arvore.timeout and ((int(request.POST['fim_tempo']) - int(request.session['ini_tempo0'])) > arvore.timeout * 60 *1000):
        messages.error(request, 'Tempo esgotado.')
        return redirect('/')

    # validar resposta
    try:
        escolha_id = request.POST['escolha']
    except (KeyError, Escolha.DoesNotExist):

        if tela.video:
            url = tela.video + '?autoplay=1&controls=0&disablekb=1&modestbranding=1&rel=0&showinfo=0'
        else:
            url = None

        return render(request, 'blog/tela.html', {
            'tela':tela,
            'escolhas': question.escolha_set.all(),
            'error_message': "Você não escolheu uma alternativa.",
            'url_tela': url,
            'tela_num': request.session['tela_num']
        })
    escolha = Escolha.objects.get(pk=escolha_id)


    # verificando duplicata
    for i in range(1, request.session['tela_num']):    
        if question.id == request.session['question' + str(i)]:
            prox_tela = Tela.objects.get(pk=request.session['question' + str(i)])
            request.session['tela_atual'] = prox_tela.id
            url = '/arvore/'
            
            return redirect(url)

    # atualizar fim_tempo
    fim_tempo_num = 'fim_tempo' + str(request.session['tela_num'])
    request.session[fim_tempo_num] = request.POST['fim_tempo']

    request.session['tela_num'] += 1
    # adicionando respostas a sessão
    question_num = 'question' + str(request.session['tela_num'])
    request.session[question_num] = question.pk
    escolha_num = 'escolha' + str(request.session['tela_num'])
    request.session[escolha_num] = escolha.pk
    tempo_num = 'tempo' + str(request.session['tela_num'])
    request.session[tempo_num] = (int(request.session[fim_tempo_num]) - int(request.session[ini_tempo_num]))

    usuario.tela_num = request.session['tela_num']

    if tela.ultimo:

        usuario.arvores.add(arvore)
        usuario.save()

        # Salvar repostas já que ele chegou no final
        pub_data    = timezone.now().date()
        for i in range(1, request.session['tela_num'] + 1):
            question = get_object_or_404(Question, pk=int(request.session['question' + str(i)]))
            escolha = get_object_or_404(Escolha, pk=int(request.session['escolha' + str(i)]))
            tempo = request.session['tempo' + str(i)]
            Resposta.objects.create(usuario=usuario, arvore=arvore, question=question, escolha=escolha, tempo=tempo, pub_data=pub_data)
        apagarSessao(request)
        url = '/arvore/concluida/'
    else:
        request.session['tela_atual'] = escolha.tela.id
        url = '/arvore/'

    return redirect(url)


@login_required
def iniciar(request, flag=None):
    
    usuario = request.user.usuario
    if not flag:
        # se não tiver flag, renderizar iniciar normalmente
        try:
            # pegar árvore disponível
            arvore_do_dia = Raiz.objects.all()[0].arvore
            if arvore_do_dia in usuario.arvores.all(): # arvore já respondida 
                return render(request, 'blog/arvoreConcluida.html',{})
        except:
            arvore_do_dia = None

        context = {
            'arvore':arvore_do_dia,
        }

        return render(request, 'blog/iniciar.html', context)

    # se tiver flag, iniciar questionário
    arvore_do_dia = Raiz.objects.all()[0].arvore
    primeira_tela = arvore_do_dia.prim_tela.id


    try:
        usuario.tela_atual
        # saiu do questionario
        # invalidar questionario
        tela = Tela.objects.get(pk=request.session['tela_atual'])
        usuario.arvores.add(tela.arvore)
        del request.session['tela_atual']
        return redirect('/')
    except:
        request.session['tela_atual'] = primeira_tela
        

    # iniciar sessão
    request.session['username'] = request.user.username
    request.session['arvore'] = arvore_do_dia.id
    request.session['tela_num'] = 0
    request.session.set_expiry(600)  

    return redirect('blog:arvore')
    

def verificarArv(arv):
    # verificar se árvore foi criada corretamente
    try:
        return arv.prim_tela
    except:
        return False

@login_required
def testar(request):
    if not request.user.is_superuser:
        return redirect('blog:home')
    
    arvores = Arvore.objects.all()
    for arv in arvores:
        if not verificarArv(arv):
            messages.warning(request, f"Parece que a arvore '{arv.nome}' não possui uma primeira tela. Por favor, verifique se ela foi preenchida corretamente.")
            return redirect('blog:home')
    
    context = {
        'arvores': arvores
    }
    return render(request, 'blog/testar.html', context)


@login_required
def teste(request, arvore_id, tela_id):
    if not request.user.is_superuser:
        return redirect('blog:home')

    tela_atual = Tela.objects.get(pk=tela_id)
    escolhas = tela_atual.question.escolha_set.all()
    if tela_atual.video:
        url = tela_atual.video + '?autoplay=1&controls=0&disablekb=1&modestbranding=1&rel=0&showinfo=0'
    else:
        url = None
    context= {
        'tela':tela_atual,
        'escolhas': escolhas,
        'url_tela':url,
    }

    return render(request, 'blog/telaTeste.html', context)

@login_required
def respostaTeste(request, tela_id):
    if not(request.user.is_superuser) or request.method == 'GET':
        return redirect('blog:home')
    
    tela        = Tela.objects.get(pk=tela_id)
    arvore      = tela.arvore
    question    = tela.question

     
    try:
        escolha_id = request.POST['escolha']
    except (KeyError, Escolha.DoesNotExist):
        return render(request, 'blog/telaTeste.html', {
            'tela':tela,
            'escolhas': question.escolha_set.all(),
            'error_message': "Você não escolheu uma alternativa."
        })

    escolha = Escolha.objects.get(pk=escolha_id)   



    if tela.ultimo:
        return redirect('blog:testar')
    else:
        prox_tela = Tela.objects.get(pk=escolha.tela.id)
        url = '/testar/arvore/' + str(arvore.id) + '/tela/' + str(prox_tela.id)
        return redirect(url)



    


# ===================


# @login_required
# def forms(request):
#     usuario_logado = request.user                                    #user logado
#     usuario_logado = usuario_logado.usuario                          #usuario logado
#     perfil = usuario_logado.perfil_especifico                        #perfil do usuario logado
#     forms_disponiveis = perfil.formularios.order_by('-data_inicial') #formularios do perfil
#     forms_respondidos = usuario_logado.formularios.all()

#     if len(forms_disponiveis) == len(forms_respondidos):             # se todos os formulários foram respondidos
#         return render(request, 'blog/forms_respondidos.html', {})

#     elif len(forms_disponiveis) < len(forms_respondidos):
#         return HttpResponse('<h1 style="color:red">ERRO: Mais formulários respondidos do que disponíveis<h1>')

#     if usuario_logado.form_atual:                                    #Continuar de onde parou
#         ultima_perg = len(usuario_logado.alternativas.all())
#     else:
#         ultima_perg = None

#     context = {
#     'forms_disponiveis' : forms_disponiveis,
#     'forms_respondidos' : forms_respondidos,
#     'ultima_perg' : ultima_perg
#     }
#     return render(request, 'blog/forms.html', context)


# @login_required
# def formulario(request, form_id):
#     try:
#         formulario = Formulario.objects.get(pk=form_id)
#     except Formulario.DoesNotExist:
#         raise Http404("Formulário inexistente")
#     return render(request, 'blog/formulario.html', {'formulario' : formulario})


# @login_required
# def pergunta(request, form_id, pergunta_num):

    
#     formulario = Formulario.objects.get(pk=form_id)
#     usuario = request.user.usuario

    
#     if not usuario.form_atual and pergunta_num == 0:                 # Usuario entrando no formulário pela primeira vez
#         print(formulario)
#         usuario.form_atual = formulario
#         usuario.save()

#     # terminou formulario
#     if pergunta_num == len(formulario.perguntas.all()):
#         for alt in usuario.alternativas.all():
#             usuario.alternativas.remove(alt)
#         usuario.formularios.add(formulario)
#         usuario.form_atual = None
#         usuario.save()
#         return redirect('/formulario')                               #tela de formulario terminado 


#     try:
#         pergunta_anterior = pergunta_num -1
#         pergunta = formulario.perguntas.all()[pergunta_num]
#         context = {
#             'formulario': formulario,
#             'pergunta': pergunta,
#             'pergunta_num': pergunta_num,
#             'num_de_perguntas': len(formulario.perguntas.all())
#         }
#     except IndexError:                                               # pergunta fora do formulario
#         return redirect('/error')
 
        
#     return render(request, 'blog/pergunta.html', context)



# def formConcluido(request):
    
#     forms_respondidos = len(request.user.usuario.formularios.all())
    
#     context = {
#         'forms_repondidos': forms_respondidos
#     }
#     return render(request, 'blog/form_concluido.html', context)


