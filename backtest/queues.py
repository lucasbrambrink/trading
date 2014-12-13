from rabbitmq.queue import BaseQueue


class ReturnsQueue(BaseQueue):
    prefix = 'returns'
    data_structure = [{'key': 'returns', 'values': []}]