from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Pet Model
class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending'),
    ]
    
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES, default='dog')
    age = models.IntegerField(help_text="Age in years")
    description = models.TextField()
    health_status = models.CharField(max_length=200, default="Healthy")
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.breed}"
    
    class Meta:
        ordering = ['-added_date']


# Adoption Request Model
class Adoption(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoptions')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.pet.name} ({self.status})"
    
    class Meta:
        ordering = ['-request_date']
        unique_together = ['user', 'pet']


# Reminder Model
class Reminder(models.Model):
    REMINDER_TYPES = [
        ('vaccination', 'Vaccination'),
        ('feeding', 'Feeding'),
        ('grooming', 'Grooming'),
        ('vet_visit', 'Vet Visit'),
        ('medication', 'Medication'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reminders', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, default='other')
    reminder_date = models.DateField()
    reminder_time = models.TimeField()
    is_recurring = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.reminder_date}"
    
    class Meta:
        ordering = ['reminder_date', 'reminder_time']
    
    @property
    def is_overdue(self):
        from datetime import datetime, date, time
        reminder_datetime = datetime.combine(self.reminder_date, self.reminder_time)
        return reminder_datetime < datetime.now() and not self.is_completed


# Chatbot Query Model
class ChatbotQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatbot_queries', blank=True, null=True)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.query[:50]}"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Chatbot Query"
        verbose_name_plural = "Chatbot Queries"


# User Profile Model (Extended User Info)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"