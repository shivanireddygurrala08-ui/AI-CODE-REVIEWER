"""Views for AI Code Reviewer."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from .forms import UserRegisterForm, CodeReviewForm, CodeSnippetForm
from .models import CodeReview, CodeSnippet, UserProfile, ActivityLog
from .analyzer import analyze_code


def index(request):
    """Landing page view."""
    return render(request, 'index.html')


def user_register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            ActivityLog.objects.create(
                user=user,
                action='register',
                description=f'User {user.username} registered'
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to AI Code Reviewer.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            ActivityLog.objects.create(
                user=user,
                action='login',
                description=f'User {user.username} logged in'
            )
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def user_logout(request):
    """User logout view."""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f'You have been logged out. See you soon, {username}!')
    return redirect('login')


@login_required
def dashboard(request):
    """Dashboard view."""
    # Get user profile
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get recent reviews
    recent_reviews = CodeReview.objects.filter(user=request.user)[:5]
    
    # Get statistics
    total_reviews = CodeReview.objects.filter(user=request.user).count()
    total_issues = sum(len(r.issues_found.get('issues', [])) for r in CodeReview.objects.filter(user=request.user))
    avg_score = sum(r.score for r in CodeReview.objects.filter(user=request.user)) / max(total_reviews, 1)
    
    # Get recent activities
    recent_activities = ActivityLog.objects.filter(user=request.user)[:10]
    
    context = {
        'profile': profile,
        'recent_reviews': recent_reviews,
        'total_reviews': total_reviews,
        'total_issues': total_issues,
        'avg_score': round(avg_score, 1),
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def review(request):
    """Code review view."""
    if request.method == 'POST':
        code = request.POST.get('code_content', '')
        language = request.POST.get('language', 'python')
        
        if not code.strip():
            messages.error(request, 'Please provide code to review.')
            return redirect('review')
        
        # Analyze the code
        result = analyze_code(code, language)
        
        # Save the review
        review = CodeReview.objects.create(
            user=request.user,
            code_content=code,
            language=language,
            issues_found=result,
            score=result['score']
        )
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action='review',
            description=f'Reviewed {language} code - Score: {result["score"]}'
        )
        
        # Update user profile
        try:
            profile = request.user.profile
            profile.total_reviews += 1
            profile.average_score = (
                (profile.average_score * (profile.total_reviews - 1) + result['score']) 
                / profile.total_reviews
            )
            profile.save()
        except UserProfile.DoesNotExist:
            pass
        
        context = {
            'review': review,
            'result': result,
            'code': code,
            'language': language,
        }
        
        return render(request, 'review_result.html', context)
    
    return render(request, 'review.html')


@login_required
def review_history(request):
    """View for review history."""
    reviews = CodeReview.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'review_history.html', context)


@login_required
def snippets(request):
    """View for code snippets."""
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='snippet',
                description=f'Created snippet: {snippet.title}'
            )
            
            messages.success(request, 'Snippet saved successfully!')
            return redirect('snippets')
    else:
        form = CodeSnippetForm()
    
    snippets = CodeSnippet.objects.filter(user=request.user)
    
    context = {
        'form': form,
        'snippets': snippets,
    }
    
    return render(request, 'snippets.html', context)


@login_required
def delete_snippet(request, snippet_id):
    """Delete a code snippet."""
    try:
        snippet = CodeSnippet.objects.get(id=snippet_id, user=request.user)
        snippet.delete()
        messages.success(request, 'Snippet deleted successfully!')
    except CodeSnippet.DoesNotExist:
        messages.error(request, 'Snippet not found.')
    
    return redirect('snippets')


@csrf_exempt
def api_review(request):
    """API endpoint for code review."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            
            if not code.strip():
                return JsonResponse({'error': 'No code provided'}, status=400)
            
            result = analyze_code(code, language)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def about(request):
    """About page view."""
    return render(request, 'about.html')


def features(request):
    """Features page view."""
    return render(request, 'features.html')