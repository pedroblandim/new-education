from django.urls import path,include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-nos/', views.about, name='about'),

    path('iniciar/', views.iniciar, name='iniciar'),
    path('iniciar/<int:flag>/', views.iniciar, name='iniciar'),
    path('arvore/', views.arvore, name='arvore'),
    path('arvore/resposta/', views.resposta, name='resposta'),
    path('arvore/concluida/', views.arvoreConcluida, name='arvoreConcluida'),
    path('testar/', views.testar, name='testar'),
    path('testar/arvore/<int:arvore_id>/tela/<int:tela_id>/', views.teste, name='teste'),
    path('testar/resposta/<int:tela_id>/', views.respostaTeste, name='respostaTeste')
    
    # path('forms/', views.forms, name='forms'),
    # path('formulario/<int:form_id>', views.formulario, name='formulario'),
    # path('formulario/<int:form_id>/pergunta/<int:pergunta_num>', views.pergunta, name='pergunta'),
    # path('formulario/', views.formConcluido, name='formConcluido'),
]