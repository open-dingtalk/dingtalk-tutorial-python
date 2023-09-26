#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import time
import dingtalk_stream


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


class MyEventHandler(dingtalk_stream.EventHandler):
    async def process(self, event: dingtalk_stream.EventMessage):
        if event.headers.event_type != 'chat_update_title':
            # ignore events not equals `chat_update_title`; 忽略`chat_update_title`之外的其他事件；
            # 该示例仅演示 chat_update_title 类型的事件订阅；
            return dingtalk_stream.AckMessage.STATUS_OK, 'OK'
        self.logger.info(
            'received event, delay=%sms, eventType=%s, eventId=%s, eventBornTime=%d, eventCorpId=%s, '
            'eventUnifiedAppId=%s, data=%s',
            int(time.time() * 1000) - event.headers.event_born_time,
            event.headers.event_type,
            event.headers.event_id,
            event.headers.event_born_time,
            event.headers.event_corp_id,
            event.headers.event_unified_app_id,
            event.data)
        # put your code here; 可以在这里添加你的业务代码，处理事件订阅的业务逻辑；

        return dingtalk_stream.AckMessage.STATUS_OK, 'OK'


def main():
    options = define_options()
    credential = dingtalk_stream.Credential(options.client_id, options.client_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_all_event_handler(MyEventHandler())
    client.start_forever()


if __name__ == '__main__':
    main()
