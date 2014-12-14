from rabbitmq.queue import BaseQueue


class ReturnsQueue(BaseQueue):
    def __init__(self, id):
        prefix = 'returns'
        data_structure = {
            'date': [],
            'returns': [],
        }
        super(ReturnsQueue, self).__init__(id, prefix, data_structure)