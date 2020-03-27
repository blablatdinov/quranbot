from django.shortcuts import render
from django.http import JsonResponse
from bot.models import *


def content_gen(request):
    if request.method == 'GET':
        # print(request.user)
        qs = QuranOneDayContent.objects.all().order_by('-day')
        context = {
            'qs': qs
        }
        return render(request, 'content_gen.html', context)
    else:
        # print(request.POST)
        # print(request.method)
        sura = request.POST['sura']
        qs = QuranAyat.objects.filter(sura=sura).order_by('pk')
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
    taken_ayats = data.getlist('ayat[]')
    taken_day = data.get('content_day')
    content_day = QuranOneDayContent.objects.get_or_create(day=taken_day)[0]
    for i in range(len(taken_ayats)):
        taken_sura = taken_ayats[i].split(':')[0]
        taken_ayat = taken_ayats[i].split(':')[1]
        ayat = QuranAyat.objects.filter(sura=taken_sura, ayat=taken_ayat)[0]
        # print(ayat)
        ayat.one_day_content = content_day
        p = ayat.save()
        # print(p)
    q = QuranOneDayContent.objects.last()
    return JsonResponse({
                'day': q.day,
                'content': q.content_for_day()
                        })

