from django import forms
from django.shortcuts import render, redirect
from app02.models import *


# Create your views here.
def dep_list(request):
    dep_set = Department.objects.all()

    return render(request, 'dep_list.html', {'dep_set': dep_set})


def dep_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Department.objects.create(title=title)
        return redirect('/dep/list')

    if request.method == 'GET':
        return render(request, 'dep_add.html')


def dep_del(request):
    id = request.GET.get('id')
    Department.objects.filter(id=id).delete()

    return redirect('/dep/list')


def dep_edit(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        Department.objects.filter(id=id).update(title=title)
        return redirect('/dep/list')
    dep_data = Department.objects.filter(id=id).first()
    return render(request, 'dep_edit.html', {'dep_data': dep_data})


def user_list(request):
    user_set = UserInfo.objects.all()
    return render(request, 'user_list.html', {'user_set': user_set})


class UserModelForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = UserInfo
        # fields = '__all__'
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})

    if request.method == 'POST':
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/usr/list/')
        else:
            return render(request, 'user_add.html', {"form": form})


def user_edit(request, id):
    row_data = UserInfo.objects.filter(id=id).first()
    if request.method == 'POST':
        # 加上instance=row_data，还代表form就是instance这一行，保存时也就是更新
        forms = UserModelForm(data=request.POST, instance=row_data)
        if forms.is_valid():
            forms.save()
            return redirect('/usr/list/')
        else:
            return render(request, 'user_edit.html', {"form": forms})
    if request.method == 'GET':
        # 加上instance=row_data就有默认值了
        form = UserModelForm(instance=row_data)
        return render(request, 'user_edit.html', {'form': form})


def user_del(request):
    id = request.GET.get('id')
    UserInfo.objects.filter(id=id).delete()

    return redirect('/usr/list')
