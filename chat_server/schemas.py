from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import ServerSerializer

server_list_doc = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter servers by category name (case-insensitive)",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Limit the number of servers returned",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="If 'true', return only servers where the authenticated user is a member. Requires authentication.",
        ),
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description="Filter by specific server ID. Requires authentication. Raises a validation error if the server does not exist.",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="If 'true', annotates each server with the number of members.",
        ),
    ],
)
