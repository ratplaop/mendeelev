from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Actual

class ActualListView(ListView):
    model = Actual
    template_name = 'actual/list.html'
    context_object_name = 'objects'

class IndexView(ListView):
    model = Actual
    template_name = 'actual/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Actual.objects.all()

def index(request):
    actuals = Actual.objects.all()  # Извлекаем все записи из базы данных
    return render(request, 'actual/index.html', {'actuals': actuals})  # Передаем данные в шаблон

def actual_detail(request, actual_id):
    actual = get_object_or_404(Actual, id=actual_id)  # Извлекаем конкретную запись
    return render(request, 'actual/detail.html', {'actual': actual})  # Передаем данные в шаблон
