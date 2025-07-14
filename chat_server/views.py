from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schemas import server_list_doc
from .serializers import ServerSerializer

# Create your views here.


class ServerListViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing servers with various filtering options.

    Query Parameters:
        - category (str, optional): Filter servers by category name (case-insensitive).
        - qty (int, optional): Limit the number of servers returned.
        - by_user (bool, optional): If "true", return only servers where the authenticated user is a member.
                                    Requires the user to be authenticated.
        - by_serverid (int, optional): Filter by specific server ID. Requires authentication.
                                       Raises a validation error if the server does not exist.
        - with_num_members (bool, optional): If "true", annotates each server with the number of members.

    Authentication:
        - Required when `by_user` is "true" or `by_serverid` is provided.

    Responses:
        - 200 OK: Returns a list of servers serialized by `ServerSerializer`.
        - 401 Unauthorized: If attempting to use `by_user` or `by_serverid` without being authenticated.
        - 400 Bad Request: If `by_serverid` is invalid or refers to a non-existent server.

    Example Usage:
        GET /api/servers/?category=gaming&qty=5&with_num_members=true
        GET /api/servers/?by_user=true
        GET /api/servers/?by_serverid=42
    """

    def get_queryset(self, request):
        queryset = Server.objects.all()
        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if (by_user or by_serverid) and not request.user.is_authenticated:
            raise AuthenticationFailed(
                "You must be authenticated to access this resource."
            )

        if category:
            queryset = queryset.filter(category__name__icontains=category)

        if by_user:
            queryset = queryset.filter(member=request.user.id)

        if by_serverid:
            try:
                queryset = queryset.filter(id=int(by_serverid))
                if not queryset.exists():
                    raise ValidationError(
                        f"Server with this ID {by_serverid} does not exist."
                    )
            except (ValueError, TypeError):
                raise ValidationError("Invalid server ID format.")

        if with_num_members:
            queryset = queryset.annotate(num_members=Count("member"))

        return queryset

    @server_list_doc
    def list(self, request):
        queryset = self.get_queryset(request)

        qty = request.query_params.get("qty")
        if qty:
            try:
                qty = int(qty)
                queryset = queryset[:qty]
            except (ValueError, TypeError):
                raise ValidationError("qty must be an integer.")

        with_num_members = request.query_params.get("with_num_members") == "true"

        serializer = ServerSerializer(
            queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
