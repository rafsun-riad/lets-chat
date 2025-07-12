from rest_framework import serializers

from .models import Server


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
