from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *  # Ensure all necessary forms are imported
from .forms import LocationForm, CustomUserRegistrationForm, FeedbackForm, ServiceForm # Explicitly import necessary forms
from django.contrib import messages

# ------------------
# Register View
# ------------------
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            if user.role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            login(request, user)
            if user.role == 'admin':
                return redirect('dashboard/admin/')
            return redirect('login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

# ------------------
# Login View
# ------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'user':
                return redirect('user_dashboard')
            elif user.role == 'worker':
                return redirect('worker_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')


# ------------------
# User Dashboard
# ------------------
@login_required
def user_dashboard(request):
    workers = WorkerProfile.objects.all()
    return render(request, 'core/user_dashboard.html', {'workers': workers})


# ------------------
# Book Worker
# ------------------
@login_required
def book_worker(request, worker_id):
    worker = get_object_or_404(CustomUser, id=worker_id)
    if request.method == 'POST':
        booking = Booking.objects.create(user=request.user, worker=worker)
        messages.success(request, 'Booking submitted.')
        return redirect('user_dashboard')
    return render(request, 'core/book_worker.html', {'worker': worker})


# ------------------
# Give Feedback
# ------------------
@login_required
def give_feedback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.booking = booking
            feedback.save()
            messages.success(request, 'Feedback submitted.')
            return redirect('user_dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'core/give_feedback.html', {'form': form})


# ------------------
# Worker Dashboard
# ------------------
@login_required
def worker_dashboard(request):
    bookings = Booking.objects.filter(worker=request.user)
    return render(request, 'core/worker_dashboard.html', {'bookings': bookings})


# ------------------
# Create Worker Profile
# ------------------
@login_required
def create_worker_profile(request):
    try:
        profile = WorkerProfile.objects.get(user=request.user)  # Changed 'worker' to 'user'
    except WorkerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            worker_profile = form.save(commit=False)
            worker_profile.user = request.user  # Changed 'worker' to 'user'
            worker_profile.save()
            messages.success(request, 'Profile updated.')
            return redirect('worker_dashboard')
    else:
        form = WorkerProfileForm(instance=profile)
    return render(request, 'core/create_worker_profile.html', {'form': form})

# ------------------
# Accept Booking (by Worker)
# ------------------
@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, worker=request.user)
    booking.status = 'accepted'
    booking.save()
    messages.success(request, 'Booking accepted.')
    return redirect('worker_dashboard')


# ------------------
# View Feedback (Worker)
# ------------------
@login_required
def view_feedback(request):
    feedbacks = Feedback.objects.filter(booking__worker=request.user)
    return render(request, 'core/view_feedback.html', {'feedbacks': feedbacks})


# ------------------
# Admin Dashboard
# ------------------
@login_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


# ------------------
# Manage Services
# ------------------
@login_required
def manage_services(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added.')
    else:
        form = ServiceForm()
    services = Service.objects.all()
    return render(request, 'core/manage_services.html', {'form': form, 'services': services})


# ------------------
# Manage Locations
# ------------------
@login_required
def manage_locations(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location added.')
    else:
        form = LocationForm()
    locations = Location.objects.all()
    return render(request, 'core/manage_locations.html', {'form': form, 'locations': locations})


# ------------------
# Approve Users (Proceed Registration)
# ------------------
@login_required
def proceed_user_registration(request):
    users = CustomUser.objects.filter(is_active=False)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, 'User approved.')
        return redirect('proceed_user_registration')
    return render(request, 'core/approve_users.html', {'users': users})

def home_view(request):
    return render(request, 'core/home.html')