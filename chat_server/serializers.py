from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Server
        exclude = ("member",)
        read_only_fields = ("id", "created_at", "updated_at")

    def get_num_members(self, obj):
        return (
            obj.num_members
            if hasattr(obj, "member") and hasattr(obj, "num_members")
            else None
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            representation.pop("num_members")
        return representation
