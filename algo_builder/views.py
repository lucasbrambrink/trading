from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


from uuid import uuid1

def UUIDView(request):
    id = uuid1().hex
    return redirect(reverse('builder:builder', kwargs={'id': id}))


class BuilderView(TemplateView):
    template_name = 'algo_builder/builder.html'

    def get_context_data(self, **kwargs):
        content = super(BuilderView, self).get_context_data(**kwargs)
        content['id'] = self.kwargs.get('id', None)
        return content


class JsonBuilder(TemplateView):
	template_name = 'algo_builder/builder.html'
	block_json = {}

	def post(self,request):
		"""

		:return:
		"""
		if request.is_ajax() and request.method == "POST":
			err = ''
			try:
				buy,sell = [],[]
				data = request.POST['data'].split('&')
				print(data)
				block = {}
				for item in data:
					key,value = item.split('=')
					block[key] = value
				formatted_block = self.parse_block(block)
				if block['behavior'] == 'buy':
					buy.append(formatted_block)
				if block['behavior'] == 'sell':
					sell.append(formatted_block)
				self.block_json[block['id'].lower()] = {
					'buy' : buy,
					'sell' : sell
				}
				return JsonResponse({'block' : self.block_json})
			except Exception as e:
				err = e
				return JsonResponse({'error': err})

		else:
			return Http404


	def parse_block(self,block):
		if block['id'].lower() == 'sma':
			formatted_block = {
					'period1' : block['period1'],
					'period2' : block['period2'],
					'range': (block['range0'],block['range1']),
					'appetite': block['appetite']
					}
		if block['id'].lower() == 'volatility' or block['id'].lower() == 'covariance':
			formatted_block = {
					'period1' : block['period'],
					'range': (block['range0'],block['range1']),
					'appetite': block['appetite']
					}
		if block['id'].lower() == 'event':
			formatted_block = {
					'stock' : block['stock'],
					'attribute': 'close',
					'range': (block['range0'],block['range1']),
					'appetite': block['appetite']
					}
		if block['id'].lower() == 'ratio':
			formatted_block = {
					'name' : block['name'],
					'range': (block['range0'],block['range1']),
					'appetite': block['appetite']
					}
		if block['id'].lower() == 'thresholds':
			formatted_block = {
					'price_range' : (block['price_range0'],block['price_range1']),
					'sector': {block['inout']: block['sector']}
					}
		if block['id'].lower() == 'diversity':
			formatted_block = {
					'num_sector' : block['num_sector'],
					'num_industry': block['num_industry']
					}
		return formatted_block
