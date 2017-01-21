from django.conf import settings
from django.utils.translation import activate, deactivate

try:
    ADMIN_LANGUAGE_CODE = settings.ADMIN_LANGUAGE_CODE
except AttributeError:
    # Fallback on default language if not set.
    ADMIN_LANGUAGE_CODE = settings.LANGUAGE_CODE

class AdminLanguageMiddleware(object):
    def process_request(self, request):
        if not request.path.startswith('/admin'):
            return

        request.LANG = ADMIN_LANGUAGE_CODE
        request.LANGUAGE_CODE = request.LANG
        activate(request.LANG)

    def process_response(self, request, response):
        deactivate()
        return response
