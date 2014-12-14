import json

from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.http import Http404
from django.http import QueryDict

from .tasks import test_backtest
from .queues import ReturnsQueue


class JSONResponse(JsonResponse):
    """
    An HttpResponse that send JSON in plain test.
    """
    def __init__(self, content, err, **kwargs):
        content = {'error': err, 'data': content}
        super(JSONResponse, self).__init__(content, **kwargs)


class RootView(TemplateView):
    template_name = 'backtest/root.html'


def run(request):
    """

    :return:
    """
    if request.is_ajax() and request.method == "POST":
        err = ''
        try:
            data = QueryDict(request.body).get('data', None)
            data = json.loads(data)
            test_backtest.delay(data)
            print('Celery: start backtest!!!')
        except Exception as e:
            err = e
        return JsonResponse({'error': err})

    else:
        return Http404


class ResultView(TemplateView):
    """
    The api for serving the data while running backtest

    """
    template_name = 'backtest/result.html'

    def get_context_data(self, **kwargs):
        content = super(ResultView, self).get_context_data(**kwargs)
        content['id'] = self.kwargs.get('id', None)
        return content
            # returns_queue = ReturnsQueue(id)
            # content = returns_queue.dequeue(int(n))
            # return JSONResponse(content[0], content[1])

def data(request, id, num):
    print(id, num)
    returns_queue = ReturnsQueue(id)
    content = returns_queue.dequeue(int(num))
    return JSONResponse(content[0], content[1])
