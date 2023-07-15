from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    login = serializers.IntegerField(required=False)
    server = serializers.CharField(required=False,  max_length=100)
    balance = serializers.IntegerField(required=False)
    equity = serializers.IntegerField(required=False)
    watch_time = serializers.DateTimeField()