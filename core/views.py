from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest, User
from .forms import ServiceRequestForm, DispatchUpdateForm, SignUpForm

# 0. SignUp View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'family'  # Default role for new users
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

# 1. The Central Hub
@login_required
def dashboard(request):
    user = request.user
    # If superuser/staff without role, treat as admin
    if user.is_superuser or user.is_staff:
        return redirect('admin_portal')
    
    # Get role safely with default fallback
    user_role = getattr(user, 'role', 'family')
    
    if user_role == 'family':
        return redirect('family_portal')
    elif user_role == 'staff':
        return redirect('staff_portal')
    elif user_role in ['admin', 'manager']:
        return redirect('admin_portal')
    
    # Default fallback
    return redirect('family_portal')

# 2. Family View
@login_required
def family_portal(request):
    my_requests = ServiceRequest.objects.filter(family_user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.family_user = request.user
            service.save()
            return redirect('family_portal')
    else:
        form = ServiceRequestForm()
    return render(request, 'core/portal_family.html', {'requests': my_requests, 'form': form})

# 3. Staff View
@login_required
def staff_portal(request):
    my_tasks = ServiceRequest.objects.filter(assigned_staff=request.user).exclude(status='Completed')
    
    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        new_status = request.POST.get('status')
        task = get_object_or_404(ServiceRequest, id=req_id, assigned_staff=request.user)
        
        # Allow transition: Pending -> In Progress -> Completed
        if new_status in ['In Progress', 'Completed']:
            task.status = new_status
            task.save()
        
        return redirect('staff_portal')
    
    return render(request, 'core/portal_staff.html', {'tasks': my_tasks})

# 4. Admin/Manager View (FIXED)
@login_required
def admin_portal(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.role in ['admin', 'manager']):
        return redirect('dashboard')

    active_requests = ServiceRequest.objects.all().order_by('created_at')
    
    # FIX: Fetch specific list of staff for the dropdown
    staff_list = User.objects.filter(role='staff')

    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        instance = get_object_or_404(ServiceRequest, id=req_id)
        form = DispatchUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('admin_portal')
    
    return render(request, 'core/portal_admin.html', {
        'requests': active_requests, 
        'staff_list': staff_list
    })