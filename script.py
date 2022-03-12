from matriculas.matricula.models import Matricula, Turma, SubNivel
from django.utils import timezone
from datetime import datetime 

# for m in Matricula.objects.all():
#     m.delete()

# for idade in range(7,17):
#     date = f"{str(timezone.now().year-idade)}-07-31"
#     birth_date = datetime.strptime(f"{str(timezone.now().year-idade)}-07-31", '%Y-%m-%d').date()
#     for count in range(1,16):
#         Matricula.objects.create(
#             name=f"Catequisando {count}-{idade}",
#             email=f"email{count}-{idade}@email.com",
#             birth_date=birth_date,
#             cpf='35486890001',
#             mother_name=f"Mãe {count}-{idade}",
#             address=f"Address {count}-{idade}",

#         )

for turma in Turma.objects.all():
    turma.delete()

for nivel in SubNivel.objects.all():
    for count in range(3):
        Turma.objects.create(
            nivel=nivel,
            local="matriz",
            dia="sabado",
            horario="15",
            sala=1
        )