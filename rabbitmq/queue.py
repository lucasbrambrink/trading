import json

from django.conf import settings

import pika
from pika.exceptions import ConnectionClosed, ChannelError


host = settings.RABBITMQ_HOST


class QueueEmptyError(Exception):
    """
    Raise when the queue is empty
    """
    pass


class BaseQueue:
    def __init__(self, id, prefix='queue', data_structure=None):
        self.name =  prefix + '_' + id
        self.data_structure = data_structure

    def enqueue(self, data):
        """
        Put data into queue with prefix_id as queue name

        :param data: data to be enqueue
        :return:
        """
        # Enqueue
        # Setup rabbitMQ connection
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
            channel = connection.channel()
            channel.queue_declare(queue=self.name)

            channel.basic_publish(
                exchange='',
                routing_key=self.name,
                body=json.dumps(data)
            )
            connection.close()
        except ChannelError as e:
            print(e)
        except ConnectionClosed as e:
            print(e)
        except Exception as e:
            print(e)

    def dequeue(self, num):
        """
        Consume a queue with prefix_id as queue name

        :param num: Number of messages to get
        :return:
        """
        if self.data_structure is None:
            data = []
        else:
            data = self.data_structure
        err = ''
        count = num
        # Consume queue
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
            channel = connection.channel()

            while count > 0:
                method_frame, properties, body = channel.basic_get(queue=self.name)
                if method_frame is None:
                    channel.close()
                    connection.close()
                    raise QueueEmptyError
                # Display the message parts
                print(method_frame)
                print(properties)
                print(json.loads(body.decode()))
                res = json.loads(body.decode())

                if self.data_structure is None:
                    data.append(res)
                else:
                    for key in data:
                        data[key].append(res[key])

                # Acknowledge the message
                channel.basic_ack(method_frame.delivery_tag)
                count -= 1

                # Cancel the consumer and return any pending messages
                requeued_messages = channel.cancel()
                print('Requeued {} messages'.format(requeued_messages))

            # Close the channel and the connection
            channel.close()
            connection.close()
        except ConnectionClosed as e:
            print(e)
            err = 'Error'
        except QueueEmptyError:
            err = 'Insufficient data'
        except Exception as e:
            print(e)
            err = 'Error'
        finally:
            return data, err


if __name__ == '__main__':
    pass