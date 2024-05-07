from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')

    # print(request.POST)
    # print(request.FILES)
    # < QueryDict: {'username': ['123'], '提交': ['提交']} >
    # <MultiValueDict: {'avatar': [<InMemoryUploadedFile: 11第十回 二将军宫门镇鬼 唐太宗地府还魂.txt (text/plain)>]}>
    file_obj = request.FILES.get('avatar')
    file_name = file_obj.name
    with open(r'app02/static/media/%s' % file_name, mode='wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
    return HttpResponse('ok')
