import os
import json
import nsq
import requests

NSQ_ADDR = os.environ.get("NSQ_ADDR")
POST_ADDR = os.environ.get("POST_ADDR")


def handler(message):
    requests.post("http://django:5000/results", data=json.loads(message.body.decode()))
    return json.loads(message.body.decode())


r = nsq.Reader(message_handler=handler, nsqd_tcp_addresses=NSQ_ADDR, topic='bg_worker', channel='consumer_channel', lookupd_poll_interval=15)


if __name__ == '__main__':
    nsq.run()