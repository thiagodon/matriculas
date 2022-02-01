from django.shortcuts import render
import re
from matriculas.matricula.models import Proof
from .models import Matricula
from .forms import MatriculaForm, ProofForm
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

# Create your views here.
def cpf_display(request):
    return render(request, 'matricula/cpf_display.html', {})

def cpf_not_validate(request):
    return render(request, 'matricula/cpf_not_validate.html', {})

def input_mask_remove(value):
    regex_syntax = r"\D"
    value = re.sub(regex_syntax, "", value)
    return value

def cpf_validate(request, cpf):
    cpf = input_mask_remove(cpf)
    if request.method == 'GET':
        matriculas = Matricula.objects.all()
        if cpf:
            matriculas = matriculas.filter(cpf=cpf)
        else:
            return HttpResponseNotFound("Impossível prosseguir sem CPF")     
        return render(request, 'matricula/cpf_validate.html', {'cpf': cpf, 'matriculas': matriculas})

def catequisando(request, cpf):
    cpf = input_mask_remove(cpf)
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


def proof_list(request, cpf):
    cpf = input_mask_remove(cpf)
    if request.method == 'GET':
        proofs = Proof.objects.all()
        if cpf:
            proofs = proofs.filter(cpf=cpf)
        else:
            return HttpResponseNotFound("Impossível prosseguir sem CPF")     
        return render(request, 'matricula/proof_list.html', {'cpf': cpf, 'proofs': proofs})


def proof(request, cpf):
    cpf = input_mask_remove(cpf)
    if request.method == 'GET':
        form = ProofForm(**{'cpf': cpf})

    if request.method == "POST":
         form = ProofForm(request.POST, request.FILES, **{'cpf': cpf})
         if form.is_valid():
             proof = form.save(commit=False)
             proof_file = form.cleaned_data.get("proof")
             proof.proof = proof_file
             proof.save()
             return redirect('proof_list', cpf=proof.cpf)
    return render(request, 'matricula/proof_edit.html', {'form': form})