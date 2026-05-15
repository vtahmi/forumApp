from datetime import time

from django.utils.deprecation import MiddlewareMixin


class TimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        response.process_time = time.time() - request.start_time
        print(f"Process time: {response.process_time}")
        return response

# def middleware(get_response):
#     def middleware(request, *args, **kwargs):
#         start_time = time.time() # process request time
#         response = get_response(request, *args, **kwargs)
#         end_time = time.time() # process response time
#         process_time = end_time - start_time
#         print(f"Process time: {process_time}")
#         return response
#     return middleware