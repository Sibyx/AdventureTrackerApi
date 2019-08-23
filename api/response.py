from django.http import JsonResponse


class SingleResponse(JsonResponse):
    def __init__(self, data, **kwargs):

        data = {
            'response': data,
            'metadata': []
        }

        super().__init__(data=data, **kwargs)
