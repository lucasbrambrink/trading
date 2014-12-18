import json
from uuid import uuid1
from datetime import date

from django.shortcuts import redirect, render_to_response
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseNotFound, QueryDict
from django.core.urlresolvers import reverse

from account.mixins import LoginRequiredMixin

from backtest.tasks import test_backtest
from backtest.queues import ReturnsQueue


class JSONResponse(JsonResponse):
    """
    An HttpResponse that send JSON in plain test.
    """
    def __init__(self, content, err, **kwargs):
        content = {'error': err, 'data': content}
        super(JSONResponse, self).__init__(content, **kwargs)


class RunView(LoginRequiredMixin, TemplateView):
    """

    :return:
    """
    template_name = 'backtest/run.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        algo_id = kwargs.get('algo_id')
        if request.is_ajax():
            err = ''
            try:
                print(self.request.POST)
                data = self.request.POST
                backtest_environ = {
                    'uuid': uuid1().hex,
                    'start_date': data.get('start_date'),
                    'end_date': data.get('end_date'),
                    'initial_balance': float(data.get('initial_balance')),
                    'frequency': int(data.get('frequency')),
                    'num_holdings': int(data.get('num_holdings'))
                }
                print(backtest_environ)
                test_backtest.delay(algo_id, backtest_environ)
            except Exception as e:
                err = e
            return JsonResponse({'backtest_id': backtest_environ['uuid'], 'error': err})
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')


# class RealView(TemplateView):
#     """
#     The api for serving the data while running backtest
#
#     """
#     template_name = 'backtest/result.html'
#
#     def get_context_data(self, **kwargs):
#         content = super(ResultView, self).get_context_data(**kwargs)
#         content['id'] = self.kwargs.get('id', None)
#         return content
#             # returns_queue = ReturnsQueue(id)
#             # content = returns_queue.dequeue(int(n))
#             # return JSONResponse(content[0], content[1])

def realtime_view(request, backtest_id, num):
    print(backtest_id, num)
    returns_queue = ReturnsQueue(backtest_id)
    content = returns_queue.dequeue(int(num))
    return JSONResponse(content[0], content[1])
