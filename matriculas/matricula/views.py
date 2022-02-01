from django.shortcuts import render
from .models import Matricula
from .forms import MatriculaForm
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

# Create your views here.
def cpf_display(request):
    return render(request, 'matricula/cpf_display.html', {})

def cpf_not_validate(request):
    return render(request, 'matricula/cpf_not_validate.html', {})

def cpf_validate(request, cpf):
    if request.method == 'GET':
        matriculas = Matricula.objects.all()
        if cpf:
            matriculas = matriculas.filter(cpf=cpf)
        else:
            return HttpResponseNotFound("Impossível prosseguir sem CPF")     
        return render(request, 'matricula/cpf_validate.html', {'cpf': cpf, 'matriculas': matriculas})

def catequisando(request, cpf):
    if request.method == 'GET':
        form = MatriculaForm(**{'cpf': cpf})

    if request.method == "POST":
         form = MatriculaForm(request.POST, request.FILES, **{'cpf': cpf})
         if form.is_valid():
             matricula = form.save(commit=False)
             document = form.cleaned_data.get("document")
             baptism = form.cleaned_data.get("baptism")
             eucharist = form.cleaned_data.get("eucharist")
             matricula.document = document
             matricula.baptism = baptism
             matricula.eucharist = eucharist
             matricula.save()
             return redirect('cpf_validate', cpf=matricula.cpf)
    return render(request, 'matricula/matricula_edit.html', {'form': form})