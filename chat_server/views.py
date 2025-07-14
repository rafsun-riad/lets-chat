from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
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
        by_serverid = request.query_params.get("by_serverid", None)
        with_num_members = request.query_params.get("with_num_members") == "true"

        if (by_user or by_serverid) and not request.user.is_authenticated:
            raise AuthenticationFailed(
                "You must be authenticated to access this resource."
            )

        if category:
            self.queryset = self.queryset.filter(category__name__icontains=category)

        if by_user:
            self.queryset = self.queryset.filter(member=request.user.id)

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        f"Server with this ID {by_serverid} does not exist."
                    )
            except ValueError:
                raise ValidationError("Invalid server ID format.")

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
