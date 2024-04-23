"""
ASGI config for djangoProject project.
Django项目的ASGI配置。
It exposes the ASGI callable as a module-level variable named ``application``.
它将ASGI callable公开为一个名为 “application” 的模块级变量。
For more information on this file, see
有关此文件的更多信息，请参见
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_asgi_application()
