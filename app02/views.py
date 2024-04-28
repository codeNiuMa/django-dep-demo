import copy
import math

from django import forms
from django.core.validators import RegexValidator
from django.http import QueryDict
from django.shortcuts import render, redirect

from app02.Fenye import Fenye
from app02.models import *
from app02.tests import md5


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
    fenye = Fenye(request, queryset=user_set, page_param='page', query_dict=(request.GET.copy()))
    return render(request, 'user_list.html', {'user_set': fenye.queryset, 'page_string': fenye.html()})


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

    def clean_password(self):
        return md5(self.cleaned_data['password'])


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})

    if request.method == 'POST':
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data['password'])
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


class NumModelForm(forms.ModelForm):
    # 验证方式1
    mobile = forms.CharField(label='手机号', max_length=11, min_length=11,
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = PrettyNum
        fields = '__all__'
        # exclude = ['level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 验证方式2
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if PrettyNum.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('手机号已存在')

        if not mobile.startswith('1'):
            raise forms.ValidationError('手机号格式错误')
        return mobile


def num_list(request):
    num_set = PrettyNum.objects.all()

    # 在这里实现一个查找功能
    query_dict: QueryDict = copy.deepcopy(request.GET)  # 保留GET的q查询参数
    query_dict._mutable = True

    value = request.GET.get('q', default='')
    if value:
        data_dict = {}
        data_dict['mobile__contains'] = value
        num_set = PrettyNum.objects.filter(**data_dict).order_by('-level')
        query_dict.setlist('q', [value])

    fenye = Fenye(request, page_param='page', queryset=num_set, query_dict=query_dict)
    num_set = fenye.queryset
    form = NumModelForm()

    context = {
        'num_set': num_set,
        'page_string': fenye.html(),
        'form': form,
        'value': value
    }

    return render(request, 'num_list.html', context)


def num_add(request):
    if request.method == 'GET':
        form = NumModelForm()
        return render(request, 'num_add.html', {'form': form})

    if request.method == 'POST':
        form = NumModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/num/list/')
        else:
            return render(request, 'num_add.html', {"form": form})


def num_del(request):
    id = request.GET.get('id')
    PrettyNum.objects.filter(id=id).delete()
    return redirect('/usr/list')


class NumEditModelForm(forms.ModelForm):
    # 验证方式1
    mobile = forms.CharField(label='手机号', max_length=11, min_length=11, disabled=True,
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')])

    class Meta:
        model = PrettyNum
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        # 加入重复检查
        if PrettyNum.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('手机号已存在')
        return mobile


def num_edit(request, id):
    row_data = PrettyNum.objects.filter(id=id).first()
    if request.method == 'POST':
        # 加上instance=row_data，还代表form就是instance这一行，保存时也就是更新
        forms = NumEditModelForm(data=request.POST, instance=row_data)
        if forms.is_valid():
            forms.save()
            return redirect('/num/list/')
        else:
            return render(request, 'num_edit.html', {"form": forms})

    if request.method == 'GET':
        # 加上instance=row_data就有默认值了
        form = NumEditModelForm(instance=row_data)
        return render(request, 'num_edit.html', {'form': form})


def index(request):
    return redirect('/usr/list/')


class LoginForm(forms.Form):
    name = forms.CharField(label='用户名', max_length=32, min_length=3,
                           error_messages={'max_length': '用户名最长为32位', 'min_length': '用户名最短为3位'},
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', max_length=32, min_length=3,
                               error_messages={'max_length': '密码最长为32位', 'min_length': '密码最短为3位'},
                               widget=forms.PasswordInput(render_value=True)
                               )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = '__all__'


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            user_obj = UserInfo.objects.filter(**form.cleaned_data).first()
            if user_obj is None:
                form.add_error('password', '用户名or密码错误')
                return render(request, 'login.html', {'form': form})
            request.session['info'] = {'id':user_obj.id, 'name':user_obj.name}
            return redirect('/usr/list/')

        return render(request, 'login.html', {'form': form})
