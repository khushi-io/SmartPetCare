from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Pet, Adoption, Reminder, ChatbotQuery, UserProfile
from .forms import UserRegisterForm, PetForm
from datetime import datetime
from .chatbot import get_chatbot_response



# ============================================
# HELPER FUNCTION
# ============================================

def is_admin(user):
    """
    Returns True if user is admin or superuser
    Used to protect admin pages
    """
    return user.is_staff or user.is_superuser


# ============================================
# PUBLIC VIEWS
# ============================================

def home(request):
    """
    Home page
    """
    return render(request, 'pets/home.html')


def pet_list(request):
    pet_type = request.GET.get('type')

    pets = Pet.objects.filter(status='available')

    if pet_type and pet_type != 'all':
        pets = pets.filter(pet_type=pet_type)

    return render(request, 'pets/pet_list.html', {
        'pets': pets
    })


# ============================================
# AUTHENTICATION
# ============================================

def register_view(request):
    """
    Register a new user
    """
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Create profile automatically
            UserProfile.objects.create(user=user)

            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'pets/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # ADMIN → Django admin only
            if user.is_superuser:
                return redirect('/admin/')

            # NORMAL USER → HOME PAGE
            return redirect('home')

        messages.error(request, "Invalid credentials")

    return render(request, 'pets/login.html')


def logout_view(request):
    """
    Logout user
    """
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('home')


# ============================================
# USER DASHBOARD
# ============================================

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Pet, Adoption, Reminder


@login_required
def user_dashboard(request):
    # All adoption requests of the user
    adoptions = Adoption.objects.filter(user=request.user)

    # Active (not completed) reminders
    reminders = Reminder.objects.filter(
        user=request.user,
        is_completed=False
    )

    now = datetime.now()

    overdue_reminders = []
    today_reminders = []
    upcoming_reminders = []

    for reminder in reminders:
        reminder_datetime = datetime.combine(
            reminder.reminder_date,
            reminder.reminder_time
        )

        if reminder_datetime < now:
            overdue_reminders.append(reminder)
        elif reminder_datetime.date() == now.date():
            today_reminders.append(reminder)
        else:
            upcoming_reminders.append(reminder)

    context = {
        # Adoption data
        'adoptions': adoptions,
        'adopted_pets_count': adoptions.filter(status='approved').count(),
        'pending_adoptions_count': adoptions.filter(status='pending').count(),

        # Reminder intelligence
        'overdue_reminders': overdue_reminders,
        'today_reminders': today_reminders,
        'upcoming_reminders': upcoming_reminders,

        # Stats
        'active_reminders_count': reminders.count(),
    }

    return render(request, 'pets/user_dashboard.html', context)


@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.status != 'available':
        messages.error(request, 'This pet is not available for adoption.')
        return redirect('pet_list')

    if Adoption.objects.filter(user=request.user, pet=pet).exists():
        messages.warning(request, 'You have already requested this pet.')
        return redirect('user_dashboard')

    Adoption.objects.create(
        user=request.user,
        pet=pet,
        status='pending'
    )

    messages.success(request, 'Adoption request submitted successfully.')
    return redirect('user_dashboard')


@login_required
def cancel_adoption(request, adoption_id):
    adoption = get_object_or_404(
        Adoption,
        id=adoption_id,
        user=request.user
    )

    if adoption.status != 'pending':
        messages.error(request, 'You cannot cancel this request.')
        return redirect('user_dashboard')

    adoption.delete()
    messages.success(request, 'Adoption request cancelled.')
    return redirect('user_dashboard')

# ============================================
# REMINDERS (IN-APP ONLY)
# ============================================

@login_required
def reminder_list(request):
    """
    List reminders
    """
    reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'pets/reminder_list.html', {'reminders': reminders})


@login_required
def add_reminder(request):
    # ONLY pets that are ADOPTED by this user
    user_pets = Pet.objects.filter(
        adoption_requests__user=request.user,
        adoption_requests__status='approved'
    ).distinct()

    if request.method == 'POST':
        pet_id = request.POST.get('pet')

        Reminder.objects.create(
            user=request.user,
            pet_id=pet_id if pet_id else None,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            reminder_type=request.POST.get('reminder_type'),
            reminder_date=request.POST.get('reminder_date'),
            reminder_time=request.POST.get('reminder_time'),
            is_recurring=request.POST.get('is_recurring') == 'on'
        )

        messages.success(request, 'Reminder added successfully')
        return redirect('user_dashboard')

    return render(request, 'pets/add_reminder.html', {
        'user_pets': user_pets
    })

@login_required
def edit_reminder(request, reminder_id):
    """
    Edit an existing reminder
    """
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)

    if request.method == 'POST':
        reminder.title = request.POST.get('title')
        reminder.description = request.POST.get('description')
        reminder.reminder_type = request.POST.get('reminder_type')
        reminder.reminder_date = request.POST.get('reminder_date')
        reminder.reminder_time = request.POST.get('reminder_time')
        reminder.is_recurring = request.POST.get('is_recurring') == 'on'
        reminder.save()

        messages.success(request, 'Reminder updated successfully')
        return redirect('user_dashboard')

    return render(request, 'pets/edit_reminder.html', {'reminder': reminder})


@login_required
def delete_reminder(request, reminder_id):
    """
    Delete reminder
    """
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted')
    return redirect('user_dashboard')


# ============================================
# CHATBOT (RULE-BASED NLP, NO API)
# ============================================

def chatbot_response_logic(message):
    """
    Simple NLP logic (NO API)
    """
    msg = message.lower()

    if 'food' in msg:
        return 'Feed your pet twice a day with balanced nutrition.'
    if 'vaccination' in msg:
        return 'Vaccinations should be done as per vet schedule.'
    if 'bath' in msg:
        return 'Bath once every 2–4 weeks is enough.'
    if 'exercise' in msg:
        return 'Daily exercise keeps pets healthy.'
    return 'I am here to help with pet care questions.'


@login_required
def chatbot_view(request):
    """
    Chatbot page
    - Clears old chats when page is opened
    - Saves new chats during conversation
    """

    # 👉 CLEAR OLD CHAT WHEN PAGE IS OPENED
    if request.method == "GET":
        ChatbotQuery.objects.filter(user=request.user).delete()
        chat_history = []

    # 👉 HANDLE CHAT MESSAGE
    if request.method == "POST":
        message = request.POST.get("message")

        if message:
            response = get_chatbot_response(message)

            ChatbotQuery.objects.create(
                user=request.user,
                query=message,
                response=response
            )

            return JsonResponse({"response": response})

    return render(request, "pets/chatbot.html", {
        "chat_history": []
    })


