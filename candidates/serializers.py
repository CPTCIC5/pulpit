from rest_framework import serializers
from .models import Resume, Notes
from .tasks import process_resume
from django.core.files.storage import FileSystemStorage
from django.db import transaction


class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Resume
        fields= ['title', 'resume_file', 'template_type']
    
    def create(self, validated_data):
        # Get the user from context
        user = self.context['request'].user if 'request' in self.context else None
        
        # Add user to validated data
        if user and 'user' not in validated_data:
            validated_data['user'] = user
            
        # Create the instance inside a transaction
        with transaction.atomic():
            inst = super().create(validated_data)
            
            # Save the instance to ensure it's in the database
            inst.save()
            
            if resume_file := validated_data.get("resume_file"):
                fs = FileSystemStorage()
                filename = fs.save(resume_file.name, resume_file)
                file_path = fs.path(filename)
                print("filepath------", file_path)
                print("resume_slug---", inst.slug)
                
                # Use on_commit to ensure the task is only queued after the transaction completes
                transaction.on_commit(lambda: process_resume.delay(inst.slug, file_path))
            
        return inst


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields= ['identifier', 'note', 'note_file', 'section', 'selected_text', 'context', 'id']


class ResumeSerializer(serializers.ModelSerializer):
    get_all_notes= NoteSerializer(many=True)
    class Meta:
        model= Resume
        fields= ['id', 'user', 'title', 'slug', 'resume_file', 'resume_data', 'get_all_notes', 'created_at', 'template_type', 'views']




class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields= ['identifier', 'note', 'section', 'selected_text', 'context', 'note_file']


class PromptSerializer(serializers.Serializer):
    input_text = serializers.CharField()
    resume_slug = serializers.CharField()
    thread_id = serializers.CharField(required=False, allow_null=True)

class PromptResponseSerializer(serializers.Serializer):
    output = serializers.CharField()
    thread_id = serializers.CharField()