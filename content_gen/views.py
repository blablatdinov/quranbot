from django.shortcuts import render
from django.http import JsonResponse
from bot.models import *


def content_gen(request):
    if request.method == 'GET':
        qs = QuranOneDayContent.objects.all().order_by('-pk')
        context = {
            'qs': qs
        }
        return render(request, 'content_gen.html', context)
    else:
        sura = request.POST['sura']
        qs = QuranAyat.objects.filter(sura=sura)
        data = []
        for q in qs:
            data.append({
                'sura': q.sura,
                'ayat': q.ayat,
            })
        response = {
            'data': data
        }
        return JsonResponse(response)


def send_content(request):
    data = request.POST
    for key in data:
        print(data[key])
    taken_content_day = data['content_day']
    taken_sura = data['ayats[]'].split(':')[0]
    taken_ayat = data['ayats[]']
    # print(taken_ayat)
    # print('asdf', taken_sura, taken_ayat)
    content_day = QuranOneDayContent.objects.get_or_create(day=taken_content_day)
    content_day = QuranOneDayContent.objects.get_or_create(day=taken_content_day)
    # print(content_day, ayats)
    return JsonResponse({'ok': 'true'})
