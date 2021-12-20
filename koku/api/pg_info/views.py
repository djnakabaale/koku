from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import get_blocked_process_info
from .models import PGStatActivity
from .models import PGStatStatements
from .serializers import PGLocksSerializer
from .serializers import PGStatActivitySerializer
from .serializers import PGStatStatementsSerializer


class PGLocksView(APIView):
    serializer_class = PGLocksSerializer
    # http_method_names = ["GET"]
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAdminUser,)

    @method_decorator(never_cache)
    def list(self, request):
        data = PGLocksSerializer(get_blocked_process_info(), many=True).data
        return Response(data)


class PGStatStatementsView(APIView):
    serializer_class = PGStatStatementsSerializer
    # http_method_names = ["GET"]
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAdminUser,)

    @method_decorator(never_cache)
    def list(self, request):
        self.queryset = PGStatStatements.objects.all()[:25]

        return super().list(request)


class PGStatActivityView(APIView):
    serializer_class = PGStatActivitySerializer
    # http_method_names = ["GET"]
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAdminUser,)

    @method_decorator(never_cache)
    def list(self, request):
        self.queryset = PGStatActivity.objects.all()

        return super().list(request)
