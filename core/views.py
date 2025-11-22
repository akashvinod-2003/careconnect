from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import ServiceRequest, User
from .forms import ServiceRequestForm, DispatchUpdateForm, SignUpForm
from .serializers import RequestSerializer

# --- WEB VIEWS ---

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'family':
        return redirect('family_portal')
    elif user.role == 'staff':
        return redirect('staff_portal')
    elif user.role in ['admin', 'manager']:
        return redirect('admin_portal')
    return redirect('login')

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

@login_required
def staff_portal(request):
    my_tasks = ServiceRequest.objects.filter(assigned_staff=request.user).exclude(status='Completed')
    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        new_status = request.POST.get('status')
        task = get_object_or_404(ServiceRequest, id=req_id, assigned_staff=request.user)
        task.status = new_status
        task.save()
        return redirect('staff_portal')
    return render(request, 'core/portal_staff.html', {'tasks': my_tasks})

@login_required
def admin_portal(request):
    if request.user.role not in ['admin', 'manager']:
        return redirect('dashboard')

    active_requests = ServiceRequest.objects.all().order_by('created_at')
    staff_list = User.objects.filter(role='staff')

    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        instance = get_object_or_404(ServiceRequest, id=req_id)
        form = DispatchUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('admin_portal')
    
    return render(request, 'core/portal_admin.html', {'requests': active_requests, 'staff_list': staff_list})

# --- API VIEWS ---

@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password, role='family')
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'role': user.role, 'name': user.username})

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'role': user.role, 'name': user.username})
    return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_family_requests(request):
    if request.method == 'POST':
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure time_preference is passed through
            serializer.save(family_user=request.user, service_type=request.data.get('service_type'), time_preference=request.data.get('time_preference'))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    tasks = ServiceRequest.objects.filter(family_user=request.user).order_by('-created_at')
    serializer = RequestSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_staff_requests(request):
    tasks = ServiceRequest.objects.filter(assigned_staff=request.user).exclude(status='Completed')
    if request.method == 'POST':
        req_id = request.data.get('id')
        status = request.data.get('status')
        try:
            task = ServiceRequest.objects.get(id=req_id, assigned_staff=request.user)
            task.status = status
            task.save()
            return Response({'status': 'updated'})
        except ServiceRequest.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)
    serializer = RequestSerializer(tasks, many=True)
    return Response(serializer.data)