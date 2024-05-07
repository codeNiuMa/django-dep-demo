import copy
import json
import math
import random
from datetime import datetime
from io import BytesIO

from django import forms
from django.core.validators import RegexValidator
from django.http import QueryDict, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app02.Fenye import Fenye
from app02.models import *
from app02.tests import md5, check_code


# Create your views here.

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
    # info_dict = request.session['info']

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
    return redirect('/login/')


class LoginForm(forms.Form):
    name = forms.CharField(label='用户名', max_length=32, min_length=3,
                           error_messages={'max_length': '用户名最长为32位', 'min_length': '用户名最短为3位'},
                           widget=forms.TextInput(attrs={'placeholder': 'root'}))
    password = forms.CharField(label='密码', max_length=32, min_length=3,
                               error_messages={'max_length': '密码最长为32位', 'min_length': '密码最短为3位'},
                               widget=forms.PasswordInput(render_value=True, attrs={'placeholder': '123456'})
                               )
    code = forms.CharField(label='验证码', max_length=4, min_length=4,
                           widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if 'attrs' not in field.widget.__dict__:
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = '__all__'


def login(request):
    if request.method == 'GET':
        # check_code()
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            input_code = form.cleaned_data.pop('code')  # 既剔除了code，又返回了code值
            user_obj = UserInfo.objects.filter(**form.cleaned_data).first()
            if user_obj is None:
                form.add_error('password', '用户名or密码错误')
                return render(request, 'login.html', {'form': form})
            elif str(input_code).upper() != str(request.session.get('img_code')).upper():
                form.add_error('code', '验证码错误')
                return render(request, 'login.html', {'form': form})
            request.session['info'] = {'id': user_obj.id, 'name': user_obj.name}
            print(request.session['info'])
            return redirect('/usr/list/')

        return render(request, 'login.html', {'form': form})


def img_code(request):
    img, code = check_code()
    print(code)
    request.session['img_code'] = code
    request.session.set_expiry(60 * 60 * 24 * 7)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect('/login/')


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def task(request):
    form = TaskModelForm()
    return render(request, 'task_list.html', {'form': form})


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {'status': True, 'data': [1, 2, 3, 4, 56]}
    json_str = json.dumps(data_dict)
    return HttpResponse(json_str)


@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()

        return HttpResponse(json.dumps({'status': True}))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['oid', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def order_list(request):
    form = OrderModelForm()
    order_set = Order.objects.all().order_by('-id')
    query_dict: QueryDict = copy.deepcopy(request.GET)  # 保留GET的q查询参数
    query_dict._mutable = True
    page = Fenye(request, order_set, query_dict=query_dict)

    context = {'form': form, 'order_set': page.queryset, 'page_string': page.html()}
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        rnd_oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000, 99999))
        form.instance.oid = rnd_oid
        form.instance.user_id = request.session.get('info').get('id')
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):
    uid = request.GET.get('uid')
    item = Order.objects.filter(id=uid)
    if not item.exists():
        return JsonResponse({'status': False, 'error': '该订单不存在'})
    item.delete()
    return JsonResponse({'status': True})


@csrf_exempt
def order_edit(request):
    if request.method == 'POST':
        # 传给后端的只有id信息
        print('POST is ', request.POST)
        uid = request.GET.get('uid')
        row = Order.objects.filter(id=uid).first()
        formx = OrderModelForm(data=request.POST, instance=row)

        if formx.is_valid():
            print('进入了保存')
            formx.save()
            print('保存了')
            return JsonResponse({'status': True})
        else:
            print('post存在错误')
            return JsonResponse({'status': False, 'error': formx.errors})
        # if not formx.is_valid():
        #     for field in formx:
        #         if field.errors:
        #             print(f"Field {field.name} has errors: {field.errors}")

    if request.method == 'GET':
        print('走了GET方法')
        uid = request.GET.get('uid')
        item_dict = Order.objects.filter(id=uid).values('id', 'oid', 'title', 'price', 'status', 'user_id').first()
        if not item_dict:
            return JsonResponse({'status': False, 'error': '该订单不存在'})

        result = {
            'status': True,
            'data': item_dict
        }
        return JsonResponse(result)
