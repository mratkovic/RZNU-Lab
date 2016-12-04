from django.utils.decorators import decorator_from_middleware
from django.conf import settings

class RequestLogMiddleware(object):

    def process_request(self, request):
        browser = request.user_agent.browser.family
        path = request.get_full_path()

        with open(settings.REQUESTS_LOG_PATH, "a") as logfile:
            logfile.write('%s\t%s\n' % (path, browser))

    def process_response(self, request, response):
        return response

"""
Log all requests mixin 
"""
class RequestLogViewMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(RequestLogViewMixin, cls).as_view(*args, **kwargs)
        view = decorator_from_middleware(RequestLogMiddleware)(view)
        return view
