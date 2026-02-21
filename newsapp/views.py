import random
import re

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import NewsInputForm, RegisterForm
from .models import NewsCheck

POPULAR_NEWS_SAMPLES = [
    {
        'headline': 'Scientists discover water traces on distant exoplanet',
        'content': 'A peer-reviewed study reports atmospheric signatures consistent with water vapor.',
    },
    {
        'headline': 'Celebrity claims moon is made of chocolate in viral clip',
        'content': 'A satirical channel posted edited statements without any factual support.',
    },
    {
        'headline': 'City announces free public Wi-Fi expansion across 200 zones',
        'content': 'Municipal records and policy documents confirm the approved infrastructure project.',
    },
]

TRENDING_CLASSIFIED = [
    {'title': 'Global renewable energy investment reaches record high', 'classification': 'True', 'score': 91.4},
    {'title': 'Miracle herb cures all diseases in 24 hours', 'classification': 'False', 'score': 94.2},
    {'title': 'Major social platform announces stronger AI content labels', 'classification': 'True', 'score': 82.7},
    {'title': 'Aliens elected as mayors in multiple cities', 'classification': 'False', 'score': 97.1},
]

REFERENCE_POOL = ['Google', 'Reddit', 'Wikipedia', 'News Archive']


def _simple_fake_news_detector(text):
    normalized = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
    tokens = [token for token in normalized.split() if token]

    fake_keywords = {
        'shocking', 'miracle', 'guaranteed', 'secret', 'conspiracy', 'banned',
        'viral', '100', 'instantly', 'aliens', 'hoax', 'click', 'unbelievable'
    }
    real_keywords = {
        'report', 'study', 'official', 'confirmed', 'data', 'evidence',
        'analysis', 'government', 'research', 'documented'
    }

    fake_hits = sum(1 for token in tokens if token in fake_keywords)
    real_hits = sum(1 for token in tokens if token in real_keywords)
    length_bonus = min(len(tokens) / 200, 0.15)

    raw_fake_score = 0.45 + (fake_hits * 0.08) - (real_hits * 0.06) - length_bonus
    fake_probability = max(0.03, min(raw_fake_score, 0.97))

    if fake_probability >= 0.5:
        label = 'False'
        confidence = round(fake_probability * 100, 2)
    else:
        label = 'True'
        confidence = round((1 - fake_probability) * 100, 2)

    return label, confidence


def landing_page(request):
    return render(request, 'newsapp/landing.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    result = None

    if request.method == 'POST':
        form = NewsInputForm(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            content = form.cleaned_data['content']
            label, confidence = _simple_fake_news_detector(f"{headline} {content}")
            source = random.choice(REFERENCE_POOL)

            saved_check = NewsCheck.objects.create(
                user=request.user,
                headline=headline,
                content=content,
                classification=label,
                score=confidence,
                source_reference=source,
            )

            result = saved_check
            messages.info(request, 'Analysis complete. Review the credibility score below.')
    else:
        form = NewsInputForm()

    recent_checks = NewsCheck.objects.filter(user=request.user)[:5]

    context = {
        'form': form,
        'result': result,
        'popular_news_samples': POPULAR_NEWS_SAMPLES,
        'trending_news': TRENDING_CLASSIFIED,
        'recent_checks': recent_checks,
    }
    return render(request, 'newsapp/dashboard.html', context)
