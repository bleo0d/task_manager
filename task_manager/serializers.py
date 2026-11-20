from rest_framework import serializers
from .models import Task, Category, SubTask
from datetime import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id',)

class SubTaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('id','created_at')


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('id',)

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id','created_at')

    def create(self, validated_data):
        name = validated_data.get('name')
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'detail': 'Category with this name already exists!'})

        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=name).exclude(id=instance.id).exists():
            raise serializers.ValidationError({'detail': 'Category with this name already exists!'})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    class TaskDetailSerializer(serializers.ModelSerializer):
        subtasks = SubTaskSerializer(many=True, read_only=True)
        class Meta:
            model = Task
            fields = '__all__'
            read_only_fields = ('id','created_at')

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id','created_at')

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError({'detail': 'Deadline date cannot be less than now!'})
        return value





