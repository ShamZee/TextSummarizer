from django.shortcuts import render,redirect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .models import Concise

@login_required(login_url="/login/")
def summary(request):
    if request.method == "POST":
        data = request.POST
        text = data.get("text_concise")
    
        # Use sumy for text summarization
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=3)  # Adjust the number of sentences as needed

        # Concatenate the sentences into a single paragraph
        summarized_paragraph = ' '.join([str(sentence) for sentence in summary])

        context = {
            'summarized_paragraph': summarized_paragraph,
            # 'text_instance': text_instance
        }
        return render(request, "textConcise/summary.html", context)

    return render(request, "textConcise/summary.html")




def welcome(request):
    return render(request,"textConcise/welcome.html")

def login_page(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/summary/')
            
    return render(request,"textConcise/login.html")



from django.contrib.auth.hashers import make_password
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        
        hashed_password = make_password(password)  # Hash the password
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_password  # Use the hashed password
        )
        
        messages.success(request, 'Account Created Successfully')
        
        return redirect('/register/')

    return render(request,"textConcise/register.html")
    
    
    
def logout_page(request):
    logout(request)
    return redirect('/login/')


