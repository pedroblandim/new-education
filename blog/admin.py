from django.contrib import admin
from .models import Usuario, Resposta, Tela, Arvore, Raiz, Question, Escolha
from django import forms

admin.site.site_header = "Pratica de Lembrar"
admin.site.site_title = "Área de Administração"
admin.site.index_title = "Bem vindo à Administração do site Prática de Lembrar"

# Register your models here.

# class AlternativaInline(admin.TabularInline):
#     model = Alternativa
#     extra = 2

# class PerguntaAdmin(admin.ModelAdmin):
#     fieldsets = [(None, {'fields': ['nome']}),
#                 ('Pergunta', {'fields': ['pergunta']}),]

#     inlines = [AlternativaInline]

class UsuarioInline(admin.TabularInline):
    model = Usuario
    extra = 0

# class PerfilGeralAdmin(admin.ModelAdmin):
#     fieldsets = [(None, {'fields': ['nome']}),
#                 ('Numero de Usuarios', {'fields': ['numero_de_usuarios']}),
#                 ('Formularios', {'fields' : ['formularios']}),]


#     inlines = [UsuarioInline]



class TelaInline(admin.TabularInline):
    model = Tela
    extra = 0
    


class RaizAdmin(admin.ModelAdmin):
    fieldsets = [('Nome', {'fields':['nome']}),]
    inlines = [TelaInline]


class ArvoreAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['nome']}), (None, {'fields': ['timeout']}), ('Primeira Tela', {'fields': ['prim_tela']})]
    # fieldsets = [(None, {'fields': ['nome']}),(None, {'fields': ['submetida']}), (None, {'fields': ['timeout']}), ('Primeira Tela', {'fields': ['prim_tela']})]
    inlines = [TelaInline]





class EscolhaInline(admin.TabularInline):
    model = Escolha
    extra = 0



class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['texto']}),]


    inlines = [EscolhaInline]




admin.site.register(Usuario)
admin.site.register(Arvore, ArvoreAdmin)
admin.site.register(Raiz)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Resposta)
admin.site.register(Escolha)



# admin.site.register(PerfilGeral, PerfilGeralAdmin)
# admin.site.register(Formulario)
# admin.site.register(Resposta)
# admin.site.register(Pergunta, PerguntaAdmin)
# admin.site.register(Alternativa)