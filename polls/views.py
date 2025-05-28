from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render, redirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question, TimeRecord
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including future ones)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()  
        ).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """
            The detail view of a question with a pub_date in the future
            returns a 404 not found.
            """
            future_question = create_question(question_text="Future question.", days=5)
            url = reverse("polls:detail", args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def test_past_question(self):
            """
            The detail view of a question with a pub_date in the past
            displays the question's text.
            """
            past_question = create_question(question_text="Past Question.", days=-5)
            url = reverse("polls:detail", args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)
            

#Registro
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente")
            return redirect('polls:index')

    else:
        form = UserCreationForm()
    return render(request, 'polls/signup.html', {'form': form})

#Inicio de sesion
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:overview')
        else:
            messages.error(request, "Parametros incorrectos")
    return render(request, 'polls/signin.html')



def overview(request):
    return render(request, 'polls/overview.html')
            
def orders(request):
    question = Question.objects.first() 
    return render(request, 'polls/orders.html', {'question': question})
               
def horario(request):
    tiempo = None
    trabajando = False
    usuarios = User.objects.all()

    if 'inicio' in request.session:
        trabajando = True
        inicio = request.session['inicio']
        ahora = timezone.now().timestamp()
        tiempo = int(ahora - inicio)
    elif 'tiempo_total' in request.session:
        tiempo = int(request.session['tiempo_total'])

    horas = minutos = segundos = 0
    if tiempo is not None:
        horas = tiempo // 3600
        minutos = (tiempo % 3600) // 60
        segundos = tiempo % 60

    return render(request, 'polls/horario.html', {
        'usuarios': usuarios,
        'corriendo': trabajando,
        'horas': horas,
        'minutos': minutos,
        'segundos': segundos
    })

def checkin(request):
    request.session['inicio'] = timezone.now().timestamp()
    request.session.pop('tiempo_total', None)
    return redirect('polls:horario')

def checkout(request):
    if 'inicio' in request.session:
        inicio = request.session['inicio']
        ahora = timezone.now().timestamp()
        tiempo_total = int(ahora - inicio)
        request.session['tiempo_total'] = tiempo_total
        del request.session['inicio']
    return redirect('polls:horario')

#Pendiente cambiar el nombre del archivo "horario.html" a "controlhoras.html"

class TimeRecordListView(generic.ListView):
    model = TimeRecord
    template_name = "polls/horario.html"
    context_object_name = "lista_usuarios"

    def get_queryset(self):
        return TimeRecord.objects.all().order_by("nombre_usuario","fecha_checkin")


class TimeRecordCreateView(generic.CreateView):
    model  = TimeRecord
    fields = ["nombre_usuario", "fecha_checkin", "fecha_checkout", "duracion"]
    template_name = "polls/horario.html" 
 
class TimeRecordUpdateView(generic.UpdateView):
    model = TimeRecord
    fields = ["nombre_usuario", "fecha_checkin", "fecha_checkout", "duracion"]
    template_name = "polls/horario.html" 
    
class TimeRecordDeleteView(generic.DeleteView):
    model = TimeRecord
    template_name = "polls/horario.html" 
    

