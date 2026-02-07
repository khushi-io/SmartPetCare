from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Adoption


@receiver(post_save, sender=Adoption)
def update_pet_status_on_approval(sender, instance, **kwargs):
    """
    When an adoption is approved, mark the pet as adopted
    """
    if instance.status == 'approved':
        pet = instance.pet
        if pet.status != 'adopted':
            pet.status = 'adopted'
            pet.save()
