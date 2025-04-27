from django.shortcuts import render, redirect
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Report
from .blockchain import blockchain
from django.contrib.auth.decorators import login_required
# Load stopwords
with open("stopwords.txt", "r") as file:
    stopwords = file.read().splitlines()

# Load vectorizer and model
vectorizer = TfidfVectorizer(stop_words=stopwords, lowercase=True, vocabulary=pickle.load(open("tfidfvectoizer.pkl", "rb")))
model = pickle.load(open("LinearSVCTuned.pkl", "rb"))


# Registration view (homepage)
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

from .forms import BlockUserForm
from .models import UserProfile

@login_required
def index(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    if 'bully_count' not in request.session:
        request.session['bully_count'] = 0

    show_popup = False
    block_form = BlockUserForm()

    if request.method == 'POST':
        if 'text' in request.POST:
            user_input = request.POST.get('text')
            transformed_input = vectorizer.fit_transform([user_input])
            prediction = model.predict(transformed_input)[0]

            if prediction == 1:
                request.session['bully_count'] += 1
            else:
                request.session['bully_count'] = 0

            if request.session['bully_count'] >= 3:
                show_popup = True
                request.session['bully_count'] = 0

            request.session['chat_history'].append({'sender': 'user', 'message': user_input})
            request.session['chat_history'].append({
                'sender': 'bot',
                'message': '🚫 Bullying - Hate Speech Sentence' if prediction == 1 else '✅ Non-Bullying-Neutral Text',
                'is_bullying': int(prediction)
            })
            request.session.modified = True

        elif 'instaid' in request.POST:
            block_form = BlockUserForm(request.POST)
            if block_form.is_valid():
                instaid = block_form.cleaned_data['instaid']
                try:
                    profile = UserProfile.objects.get(instaid=instaid)
                except UserProfile.DoesNotExist:
                    # Create a new dummy user and profile if not found
                    dummy_user = User.objects.create(username=instaid)
                    profile = UserProfile.objects.create(user=dummy_user, instaid=instaid)
                
                profile.is_blocked = True
                profile.save()

                return redirect('index')

    return render(request, 'index.html', {
        'chat_history': request.session['chat_history'],
        'show_popup': show_popup,
        'block_form': block_form
    })



def clear_chat(request):
    request.session['chat_history'] = []
    return redirect('index')

@login_required
def report_fake_profile(request):
    """Handles reporting of fake profiles with blockchain integration."""
    if request.method == 'POST':
        reported_profile = request.POST.get('reported_profile')
        reason = request.POST.get('reason')

        # Create a report
        report = Report(user=request.user, reported_profile=reported_profile, reason=reason)
        report.save()  # Save to generate a timestamp

        # Store in Blockchain
        report_hash = blockchain.create_block({
            'reported_profile': reported_profile,
            'reason': reason,
            'timestamp': str(report.timestamp)
        })
        report.blockchain_tx_hash = report_hash
        report.save()

        return redirect('register')

    return render(request, 'report.html')