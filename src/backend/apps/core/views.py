import structlog
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = structlog.getLogger(__name__)


@api_view(["GET"])
def ping(request):
    return Response(status=status.HTTP_200_OK)
