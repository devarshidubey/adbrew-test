import logging
from rest_framework.views import exception_handler as drf_exception_handler
from django.http import JsonResponse
from core.utils.exceptions import HTTPError

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    if isinstance(exc, HTTPError):
        return JsonResponse(
            {
                "success": False,
                "message": exc.message,
                "errors": getattr(exc, "payload", None),
            },
            status=exc.status_code
        )

    response = drf_exception_handler(exc, context)

    if response is not None:
        return JsonResponse(
            {
                "success": False,
                "message": "Request failed",
                "errors": response.data,
            },
            status=response.status_code,
        )

    logger.exception("Unhandled exception", exc_info=exc)

    return JsonResponse(
        {
            "success": False,
            "message": "Internal server error",
            "errors": None,
        },
        status=500,
    )

def handler404(request, exception):
    return JsonResponse(
        {
            "success": False,
            "message": "Endpoint not found",
            "errors": None,
        },
        status=404,
    )

def handler500(request):
    return JsonResponse(
        {
            "success": False,
            "message": "Internal server error",
            "errors": None,
        },
        status=500,
    )
