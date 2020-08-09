from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from content.models import MorningContent, Ayat


def get_content(request):
    morning_content = MorningContent.objects.all().order_by('-pk')[:10]
    res = [
        {
            'day': x.day,
            'content': x.content_for_day()
        }
        for x in morning_content
    ]
    return JsonResponse(res, safe=False)


def create_content(request):
    return render(request, 'content/create.html')


def get_ayats(request):
    sura_num = request.GET.get('sura_num')
    ayats = list(Ayat.objects.filter(one_day_content__isnull=True, sura=sura_num).values('pk', 'sura', 'ayat'))
    return JsonResponse(ayats, safe=False)


@csrf_exempt
def send_ayats(request):
    data = eval(request.body)
    morning_content, _ = MorningContent.objects.get_or_create(day=data.get('day'))
    ayats = [Ayat.objects.get(pk=x) for x in data.get('ayats')]
    for ayat in ayats:
        ayat.one_day_content = morning_content
        ayat.save()
    return JsonResponse({'ok': True})
