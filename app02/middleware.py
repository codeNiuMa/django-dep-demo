from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要登录验证的login

        if request.path_info in ['/login/', '/img/']:
            return None

        info_dict = request.session.get('info')
        if info_dict:
            return None
        else:
            return redirect('/login/')
