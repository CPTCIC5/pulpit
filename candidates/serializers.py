from rest_framework import serializers
from .models import Resume, Notes
from .tasks import process_resume
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.utils.text import slugify
import uuid


class ResumeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Resume
        fields= ['title', 'resume_file', 'template_type']
    
    def create(self, validated_data):
        with transaction.atomic():
            # Generate slug explicitly before saving
            title = validated_data.get('title', '')
            base_slug = slugify(title)
            unique_id = str(uuid.uuid4())[:8]
            slug = f"{base_slug}-{unique_id}"
            
            # Set slug in validated data
            validated_data['slug'] = slug
            
            # Create instance
            inst = super().create(validated_data)
            
            # Make sure the slug is persisted
            inst.save()
            
            if resume_file := validated_data.get("resume_file"):
                fs = FileSystemStorage()
                filename = fs.save(resume_file.name, resume_file)
                file_path = fs.path(filename)
                print("filepath------", file_path)
                print("slug being used for task------", inst.slug)
                
                # Force the transaction to commit before sending to Celery
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