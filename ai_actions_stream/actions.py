# !/usr/bin/env python

import json
import argparse
import logging
from dingtalk_stream import AckMessage
import dingtalk_stream

def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client_id', dest='client_id', required=True,
        help='app_key or suite_key from https://open-dev.digntalk.com'
    )
    parser.add_argument(
        '--client_secret', dest='client_secret', required=True,
        help='app_secret or suite_secret from https://open-dev.digntalk.com'
    )
    options = parser.parse_args()
    return options


class WeatherHandler(dingtalk_stream.GraphHandler):
    def __init__(self, logger: logging.Logger = None):
        super(dingtalk_stream.GraphHandler, self).__init__()
        if logger:
            self.logger = logger

    async def process(self, callback: dingtalk_stream.CallbackMessage):
        request = dingtalk_stream.GraphRequest.from_dict(callback.data)
        self.logger.info('incoming request, method=%s, uri=%s', request.request_line.method, request.request_line.uri)

        response = dingtalk_stream.GraphResponse()
        response.status_line.code = 200
        response.status_line.reason_phrase = 'OK'
        response.headers['Content-Type'] = 'application/json'
        response.body = json.dumps({
            'location': '杭州',
            'dateStr': '2024-10-24',
            'text': '晴天',
            'temperature': 22,
            'humidity': 65,
            'wind_direction': '东南风'
        }, ensure_ascii=False)
        return AckMessage.STATUS_OK, response.to_dict()


def main():
    logger = setup_logger()
    options = define_options()

    credential = dingtalk_stream.Credential(options.client_id, options.client_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.graph.GraphMessage.TOPIC, WeatherHandler(logger))
    client.start_forever()


if __name__ == '__main__':
    main()
