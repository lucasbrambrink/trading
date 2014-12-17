from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView


from uuid import uuid1

def uuid_view(request):
    algo_id = uuid1().hex
    return redirect(reverse('builder:new', kwargs={'algo_id': algo_id}))


class NewView(TemplateView):
    template_name = 'algo_builder/builder.html'

    def get_context_data(self, **kwargs):
        content = super(NewView, self).get_context_data(**kwargs)
        content['algo_id'] = self.kwargs.get('algo_id', None)
        return content


class JsonBuilder(TemplateView):
	template_name = 'algo_builder/builder.html'

	def post(self,request):
		"""

		:return:
		"""
		if request.is_ajax() and request.method == "POST":
			err = ''
			try:
				block_json = {}
				buy,sell = [],[]
				data = request.POST['data'].split('&')
				print(data)
				block = {}
				for item in data:
					key,value = item.split('=')
					block[key] = value
				formatted_block = self.parse_block(block)
				if block['behavior'] == 'Buy':
					buy.append(formatted_block)
				if block['behavior'] == 'Sell':
					sell.append(formatted_block)
				block_json[block['id'].lower()] = {
					'buy' : buy,
					'sell' : sell
				}
				return JsonResponse({'block' : block_json})
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
			print(block['name'])
			if block['name'] == "Cash+per+Revenue":
				name = 'CASH_REV'
			elif block['name'] == 'EV+%2F+EBITDA':
				name = 'EV_EBITDA'
			elif block['name'] == 'PE+(Current)':
				name = 'PE_CURR'
			elif block['name'] == 'Market+Cap':
				name = 'MKT_CAP'
			elif block['name'] == 'Return+on+Equity':
				name = 'ROE'
			formatted_block = {
					'name' : name,
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
