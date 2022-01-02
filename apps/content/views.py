"""Вьюхи контента."""
import ast

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.content.models import Ayat, MorningContent


def get_content(request):
    """Вьюха возвращает день и контент для html генератора."""
    morning_content = MorningContent.objects.all().order_by('-pk')[:10]
    res = [
        {
            'day': x.day,
            'content': x.content_for_day(),
        }
        for x in morning_content
    ]
    return JsonResponse(res, safe=False)


def create_content(request):
    """Вьюха генерит страницу для удобной генерации контента."""
    return render(request, 'content/create.html')


def get_ayats(request):
    """Получить аяты по номеру суры."""
    sura_num = request.GET.get('sura_num')
    ayats = [
        {
            'pk': ayat.pk,
            'sura': ayat.sura,
            'ayat': ayat.ayat,
            'content_length': len(ayat.content),
        }
        for ayat in Ayat.objects.filter(one_day_content__isnull=True, sura=sura_num).order_by('pk')
    ]
    return JsonResponse(ayats, safe=False)


@csrf_exempt
def send_ayats(request):
    """Записать выбранный контент в БД."""
    data = ast.literal_eval(request.body)
    morning_content, _ = MorningContent.objects.get_or_create(day=data.get('day'))
    ayats = [Ayat.objects.get(pk=x) for x in data.get('ayats')]
    for ayat in ayats:
        ayat.one_day_content = morning_content
        if len(morning_content.content_for_day()) > 4095:
            return JsonResponse({'ok': False, 'error': 'too many symbols in content for day'})
        ayat.save()
    return JsonResponse({'ok': True})
