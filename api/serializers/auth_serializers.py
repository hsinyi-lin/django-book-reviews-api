from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    id = serializers.CharField()
    pwd = serializers.CharField(max_length=30)
    name = serializers.CharField(max_length=30)
    gender = serializers.BooleanField()
    photo = serializers.ImageField()
    birth = serializers.DateField(allow_null=True)