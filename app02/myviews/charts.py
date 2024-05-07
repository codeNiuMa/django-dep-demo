from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    return render(request, 'chart.html')


def chart_bar(request):
    legend = {'data': ['销量', '成本']}

    series = [
        {
            'name': '销量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '成本',
            'type': 'bar',
            'data': [3, 10, 46, 15, 15, 10]
        }
    ]
    xAxis = {'data': ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']}
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series': series,
            'xAxis': xAxis
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    series = [{'value': 1048, 'name': 'Search Engine'},
              {'value': 735, 'name': 'Direct'},
              {'value': 580, 'name': 'Email'},
              {'value': 484, 'name': 'Union Ads'},
              {'value': 300, 'name': 'Video Ads'}]

    result = {
        'data': {
            'series': series
        }
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ['Email', 'Union Ads', 'Video Ads', 'Direct', 'Search Engine']
    series = [
        {
            'name': 'Email',
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
        },
        {
            'name': 'Union Ads',
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290, 330, 310]
        },
        {
            'name': 'Video Ads',
            'type': 'line',
            'stack': 'Total',
            'data': [150, 232, 201, 154, 190, 330, 410]
        },
        {
            'name': 'Direct',
            'type': 'line',
            'stack': 'Total',
            'data': [320, 332, 301, 334, 390, 330, 320]
        },
    ]
    xAxis = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series': series,
            'xAxis': xAxis
        }
    }
    return JsonResponse(result)
