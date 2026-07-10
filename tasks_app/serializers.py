from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class TaskSerializer(serializers.ModelSerializer):
    # Nested read representation of tags
    tags = TagSerializer(many=True, read_only=True)
    # Write-only list of tag IDs for create/update
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'tags', 'tag_ids', 'owner',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def create(self, validated_data):
        tag_objs = validated_data.pop('tag_ids', [])
        task = Task.objects.create(**validated_data)
        task.tags.set(tag_objs)
        return task

    def update(self, instance, validated_data):
        tag_objs = validated_data.pop('tag_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_objs is not None:
            instance.tags.set(tag_objs)
        return instance
