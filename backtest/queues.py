from rabbitmq.queue import BaseQueue


class ReturnsQueue(BaseQueue):
    prefix = 'returns'
    data_structure = [
        {'key': 'date', 'values': []},
        {'key': 'returns', 'values': []}
    ]