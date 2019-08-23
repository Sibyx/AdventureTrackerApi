import json


class JsonMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_type = request.headers.get('Content-Type')

        if content_type == 'application/json':
            request.POST = json.loads(request.body)

        return self.get_response(request)
