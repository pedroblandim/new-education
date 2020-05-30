from django.db import models
from django.contrib.auth.models import User

class Arvore(models.Model):
    nome = models.CharField('Nome da Árvore', null=True, blank=False,max_length=120)
    submetida = models.BooleanField('Já foi submetida à resposta', default=False, blank=False)
    prim_tela = models.OneToOneField('Tela', on_delete=models.CASCADE, blank= True, null = True, related_name='+')
    timeout = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return 'Árvore ' + str(self.id) + ': ' + self.nome

class Usuario(models.Model):

    escolaridades = [('FI',   'Ensino Fundamental Incompleto'),
                     ('FC',   'Ensino Fundamental Completo'),
                     ('MI',   'Ensino Medio Incompleto'),
                     ('MC',   'Ensino Medio Completo'),
                     ('SI',  'Ensino Superior Incompleto'),
                     ('SC',  'Ensino Superior Completo')
    ]
    generos = [('Masc', 'Masculino'), ('Femin', 'Feminino'), ('Outro', 'Outro')]

    nome = models.CharField('Nome do Usuário', max_length=120, blank=False, null=True)
    email = models.EmailField('Email',blank=False,null=True,unique=True)
    idade = models.IntegerField(blank=False, null=True)
    genero = models.CharField('Gênero', blank=False,max_length=15, choices=generos, null=True)
    escolaridade = models.CharField('Escolaridade', choices=escolaridades, max_length=3, blank=False, null=True)
    curso = models.CharField('Curso', max_length=120, blank=False, null=True)
    nacionalidade = models.CharField('Nacionalidade', max_length=120, blank=False, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, editable=False)

    # arvores ja respondidas
    arvores = models.ManyToManyField('Arvore', blank =True)
    # arvores = models.ManyToManyField('Arvore', blank =True, editable=False)


    def __str__(self):
        return self.nome


class Tela(models.Model):
    arvore = models.ForeignKey(Arvore,on_delete=models.CASCADE, null = True)
    nome = models.CharField('Nome da Tela', null=True, blank=False, max_length=120)
    question = models.OneToOneField('Question', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Pergunta')
    
    ultimo = models.BooleanField('Final', default=False, blank=False)

    # estimulos:
    video = models.URLField(max_length=250, null=True, blank=True)
    imagem = models.ImageField(upload_to='estimulos/', blank=True, null=True, help_text='A ordem de prioridade dos estímulos é de Vídeo > Imagem > Texto')
    texto = models.CharField(null=True, blank=True, max_length=250)

    def __str__(self):
        return 'Árvore ' + str(self.arvore.id) + ': ' + self.nome



class Question(models.Model):
    texto = models.CharField('Texto da questão', max_length=120, blank=False, null=True)
    tela_filha = models.ManyToManyField(Tela, through='Escolha', related_name='questions')
    
    class Meta:
        verbose_name = 'Pergunta'


    def __str__(self):
        try:
            return 'Árvore ' + str(self.tela.arvore.id) + ': ' + self.texto
        except:
            return self.texto




class Escolha(models.Model):

    nome = models.CharField('Nome da Escolha', null=True, blank=False, max_length=120)

    # Question pai
    question = models.ForeignKey(Question,on_delete=models.CASCADE, null = True, blank=True)

    # Tela filha
    tela = models.ForeignKey(Tela ,on_delete=models.CASCADE, null = True, blank=True)
    
    def __str__(self):
        return self.nome
    


class Raiz(models.Model):

    arvore = models.OneToOneField(Arvore, on_delete=models.CASCADE, null=True,blank=True, help_text="<h1><strong>Ao submeter uma árvore a ser respondinda no site, ela não poderá mais ser editada.</strong></h1>")

    # tempo de duração, etc
    def __str__(self):
        if self.arvore:
            return 'Árvore ' +  str(self.arvore.id) + ': ' + self.arvore.nome
        else:
            return 'Raiz vazia'

    class Meta:
        verbose_name_plural = "Raizes"

class Resposta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, null=True, editable=False)
    arvore = models.ForeignKey(Arvore, on_delete=models.DO_NOTHING, null=True, editable=True)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, null=True, editable=True)
    escolha = models.ForeignKey(Escolha, on_delete=models.DO_NOTHING, null=True, editable=True)
    tempo = models.IntegerField(blank=True, null=True)

    pub_data = models.DateField('Data da resposta', null=True, blank=True, editable=True)

    def __str__(self):
        return self.usuario.nome + ': ' + self.question.texto



# ================================================



# class Pergunta(models.Model):
#     nome = models.CharField('Nome da pergunta', max_length=120, blank=False)
#     pergunta = models.CharField('Pergunta', max_length=120, blank=False)

#     def __str__(self):
#         return self.nome

# class Formulario(models.Model):

#     nome = models.CharField('Nome do formulário', max_length=120, blank=False)
#     descricao = models.CharField('Descricao', max_length=120, blank=True, null=True)
#     data_inicial = models.DateField('Data de Início', auto_now=False, auto_now_add=False, null=True)
#     data_final = models.DateField('Data Final', auto_now=False, auto_now_add=False, null=True)
#     perguntas = models.ManyToManyField(Pergunta, blank=True)

#     def __str__(self):
#         return self.nome


# class PerfilGeral(models.Model):

#     nome = models.CharField('Nome do Perfil', max_length=120, blank=False)
#     numero_de_usuarios = models.PositiveIntegerField(blank=False, default=0)
#     formularios = models.ManyToManyField(Formulario, blank=True)

#     def __str__(self):
#         return self.nome

# class Alternativa(models.Model):
#     texto = models.CharField('Texto da alternativa', max_length=120, blank=False, null=True)

#     # cada alternativa está ligada a apenas uma pergunta
#     pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)

#     # Dados: quantas vezes escolhida, tempo médio de tempo de respota, etc...

#     def __str__(self):
#         return self.texto



