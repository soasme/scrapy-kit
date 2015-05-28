# -*- coding: utf-8 -*-

import os
import json
from scrapyd.webservice import WsResource
from subprocess import Popen, PIPE
from scrapyd.utils import get_crawl_args

class Crawl(WsResource):

    def jsonize(self, data):
        try:
            data = json.loads(data)
            return {'code': 0, 'message': 'success', 'data': data}
        except ValueError as e:
            return {'code': 1, 'message': 'json parse error', 'data': data}

    def crawl(self, args):
        env = os.environ.copy()
        cmd = ['scrapy', 'crawl']
        args['_spider'] = args.get('spider')
        args['_project'] = args.get('project')
        cargs = get_crawl_args(args)
        cmd = cmd + cargs + ['-t', 'json', '-o', '-']
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, env=env)
        out, _ = process.communicate()
        return self.jsonize(out)

    def render_POST(self, request):
        settings = request.args.pop('setting', [])
        settings = dict(x.split('=', 1) for x in settings)
        args = dict((k, v[0]) for k, v in request.args.items())
        resp = self.crawl(args)
        return resp
