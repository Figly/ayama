from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "home.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"


def healthz(request):
    """Return all-is-ok response on test.
    :param request: Not required for this method, but will get passed with GET request.
    :return: 200, "OK"
    """
    message = ""
    if int(str(HttpResponse.status_code)[:1]) == 2:
        message = f"Everything is OK and the API is running. Request: {request}"
    elif int(str(HttpResponse.status_code)[:1]) == 5:
        message = f"Internal Server Error: Request: {request}"
    response = {
        "status": HttpResponse.status_code,
        "message": message,
        "datetime": datetime.now(),
    }
    return JsonResponse(response)
