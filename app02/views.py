from django.shortcuts import render, redirect
from app02.models import *

# Create your views here.
def dep_list(request):
    dep_set = Department.objects.all()

    return render(request, 'dep_list.html', {'dep_set': dep_set})


def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Department.objects.create(title=title)
        return redirect('/dep/list')

    if request.method == 'GET':
        return render(request, 'dep_add.html')


def dele(request):
    id = request.GET.get('id')
    Department.objects.filter(id=id).delete()

    return redirect('/dep/list')


def edit(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        Department.objects.filter(id=id).update(title=title)
        return redirect('/dep/list')
    dep_data = Department.objects.filter(id=id).first()
    return render(request, 'dep_edit.html', {'dep_data': dep_data})