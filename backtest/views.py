from uuid import uuid1

from django.shortcuts import redirect, render_to_response
from django.http import JsonResponse, HttpResponseNotFound, Http404
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

from account.mixins import LoginRequiredMixin

from backtest.tasks import run_backtest
from backtest.queues import ReturnsQueue
from backtest.models import (Backtests, Assets, RiskMetrics)
from backtest.serializers import (AssetsSerializer, RiskMetricsSerializer)


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
                run_backtest.delay(algo_id, backtest_environ)
            except Exception as e:
                err = e
            return JsonResponse({'backtest_id': backtest_environ['uuid'], 'error': err})
        else:
            return HttpResponseNotFound('<h1>No Page Here</h1>')


def realtime_view(request, backtest_id, num):
    print(backtest_id, num)
    returns_queue = ReturnsQueue(backtest_id)
    content = returns_queue.dequeue(int(num))
    return JSONResponse(content[0], content[1])


class AssetsList(APIView):
    """
    List all assets for a backtest
    """
    def get_object(self, uuid):
        try:
            return Backtests.objects.get(uuid=uuid)
        except Backtests.DoesNotExist:
            raise Http404

    def get(self, request, backtest_uuid, format=None):
        backtest = self.get_object(backtest_uuid)
        assets = Assets.objects.filter(backtest=backtest)
        serializer = AssetsSerializer(assets, many=True)
        return Response(serializer.data)


class AssetsDateList(APIView):
    """
    List all assets for a backtest
    """
    def get_object(self, uuid):
        try:
            return Backtests.objects.get(uuid=uuid)
        except Backtests.DoesNotExist:
            raise Http404

    def get(self, request, backtest_uuid, year, month, day, format=None):
        backtest = self.get_object(backtest_uuid)
        date = '{}-{}-{}'.format(year, month, day)
        assets = Assets.objects.filter(backtest=backtest, date=date)
        serializer = AssetsSerializer(assets, many=True)
        return Response(serializer.data)


class RiskMetricsList(APIView):
    """
    List all risk metrics for a backtest
    """
    def get_object(self, uuid):
        try:
            return Backtests.objects.get(uuid=uuid)
        except Backtests.DoesNotExist:
            raise Http404

    def get(self, request, backtest_uuid, format=None):
        backtest = self.get_object(backtest_uuid)
        risks = RiskMetrics.objects.filter(backtest=backtest)
        serializer = RiskMetricsSerializer(risks, many=True)
        return Response(serializer.data)


class RiskMetricsDateList(APIView):
    """
    List all assets for a backtest
    """
    def get_object(self, uuid):
        try:
            return Backtests.objects.get(uuid=uuid)
        except Backtests.DoesNotExist:
            raise Http404

    def get(self, request, backtest_uuid, year, month, day, format=None):
        backtest = self.get_object(backtest_uuid)
        date = '{}-{}-{}'.format(year, month, day)
        risks = RiskMetrics.objects.filter(backtest=backtest, date=date)
        serializer = RiskMetricsSerializer(risks, many=True)
        return Response(serializer.data)