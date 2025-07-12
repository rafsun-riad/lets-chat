from rest_framework import viewsets
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer

# Create your views here.


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category", None)
        qty = request.query_params.get("qty", None)
        by_user = request.query_params.get("by_user") == "true"

        if category:
            self.queryset = self.queryset.filter(category=category)

        if by_user:
            self.queryset = self.queryset.filter(member=request.user.id)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
