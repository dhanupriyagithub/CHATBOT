# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import openai
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate

from chatbot.backends import CustomEmailBackend

import openai



@login_required(login_url='login')
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        
        # Use OpenAI GPT-3 to generate a response
        response = generate_response(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response,'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')})
    
    return render(request, 'chatbot.html', {'chats': chats})

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY
model = 'text-davinci-002'

temperature = 0.5

def generate_response(prompt):
    women_prompt = ' '.join(['women', 'feminism', 'girl', 'girls', 'female', 'ladies', 'woman', 'lady', 'madam', 'gentlewoman',
                             'spouse', 'wife', 'bride', 'wifey', 'lady', 'old lady', 'housewife', 'housekeeper', 'homemaker',
                             'partner', 'feminine', 'womanly', 'womanish', 'womanlike', 'sissy', 'sister', 'mother',
                             'grandmother', 'grandmothers', 'great grandmother'])
    
    # Combine the user's input with the women-related prompt
    full_prompt = f'{women_prompt}\nUser: {prompt} for women\nAI:'

    # Use OpenAI GPT-3 to generate a response
    response = openai.Completion.create(
        engine=model,
        prompt=full_prompt,
        max_tokens=150,
    )
    return response.choices[0].text.strip()


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('chatbot')
#         else:
#             error_message = 'Invalid username or password'
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         return render(request, 'login.html')

#------------------------------------------------------------------------------------------

# def user_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email,password)
#         user = auth.authenticate(request, email=email, password=password)
#         print(user)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('chatbot')
#         else:
#             error_message = 'Invalid Email or password'
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Email: {email}, Password: {password}")

        try:
            user = auth.authenticate(request, email=email, password=password)
            
            print(user)

            if user is not None:
                auth.login(request, user)
                return redirect('chatbot')
            else:
                error_message = 'Invalid Email or password'
                return render(request, 'login.html', {'error_message': error_message})
        except Exception as e:
            print(f"Exception during authentication: {e}")
            error_message = 'An error occurred during authentication'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                # Check if the username already exists
                if User.objects.filter(username=username).exists():
                    error_message = 'Username is already taken. Please choose a different one.'
                    messages.error(request, error_message)
                    return render(request, 'register.html', {'error_message': error_message})

                # Create a new user
                user = User.objects.create_user(username, email, password1)

                # Authenticate the user to set the backend
                authenticated_user = authenticate(request, username=username, password=password1)
                print(f"Authentication result for user '{username}': {authenticated_user}")

                # If authentication is successful, user will be an authenticated user
                if authenticated_user is not None:
                    auth.login(request, authenticated_user)
                    return redirect('chatbot')
                else:
                    raise ValueError('Authentication failed')

            except IntegrityError as e:
                error_message = f'Error creating account: {str(e)}'
                messages.error(request, error_message)
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords don\'t match'
            messages.error(request, error_message)
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')



def logout(request):
    auth.logout(request)
    return redirect('login')

