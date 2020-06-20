from django.shortcuts import render
from django.http import JsonResponse
from bot.models import *

import json


def content_gen(request):
    if request.method == 'GET':
        # print(request.user)
        qs = QuranOneDayContent.objects.all().order_by('-day')#[:10]
        for q in qs:
            print(q)
        context = {
            'qs': qs
        }
        return render(request, 'content_gen_vue.html', context)
    else:
        print(request.body)
        # print(request.method)
        print('take')
        data = eval(request.body)
        sura = data.get('sura')
        #qs = QuranAyat.objects.filter(sura=sura, one_day_content=None).order_by('pk')
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
    data = json.loads(request.body)
    print(data)
    taken_ayats = data.get('ayat')
    taken_day = data.get('content_day')
    content_day = QuranOneDayContent.objects.get_or_create(day=taken_day)[0]
    for i in range(len(taken_ayats)):
        taken_sura = taken_ayats[i].get('sura')
        taken_ayat = taken_ayats[i].get('ayat')
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

