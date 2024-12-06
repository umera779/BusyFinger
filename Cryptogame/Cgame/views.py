from django.shortcuts import render, redirect
from .models import Counter, TaskList, Boost, Mining, Level, CustomUser
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import intcomma

@login_required
def home(request):
    mining_speed = request.user.mining.speed
    # Get the counter object associated with the current user

    counter = request.user.counter
    user_balance = request.user.counter.value
    level = "Learner"
    if user_balance > 15000000:
        level = "newbie"
    if user_balance >= 24000000 :
        level = "Amature"
    if user_balance >= 100000000:
        level = "Pro"
    if user_balance >= 500000000:
        level = "Elite"

    players = Counter.objects.all().order_by('-value')[:3]  # Get top 10
    
    leaderboard = []
    
    if len(players) > 0:
        leaderboard.append({
            'rank': 1,
            'username': players[0].user.username,
            'balance': players[0].value
        })
    if len(players) > 1:
        leaderboard.append({
            'rank': 2,
            'username': players[1].user.username,
            'balance': players[1].value
        })
    if len(players) > 2:
        leaderboard.append({
            'rank': 3,
            'username': players[2].user.username,
            'balance': players[2].value
        })

    # return render(request, 'pain.html', {
    #     'counter': counter,
    #     'mining_speed': mining_speed,
    #     'level': level,
    #     'leaderboard': leaderboard
    # })

# This assumes that each user has a unique Counter object
    return render(request, 'pain.html', {'counter': counter,'mining_speed': mining_speed, 'level':level, 'leaderboard': leaderboard})

@login_required
def increment_counter(request):
    # Get the mining speed associated with the current user
    mining_speed = request.user.mining  # This assumes that each user has a unique Mining object
    mining_goat = mining_speed.speed

    if request.method == 'POST':
        # Get the counter object associated with the current user
        counter = request.user.counter
        counter.value += int(mining_goat)
        counter.save()
        formatted_counter_value = f"{counter.value:,}"

        # Return the updated counter value as a JSON response
        # return JsonResponse({'counter_value': counter.value})
        return JsonResponse({'counter_value': formatted_counter_value})

    return render(request, 'pain.html', {'counter': request.user.counter})

@login_required
def boost(request):
    boosting_rate = Boost.objects.filter(assigned_users=request.user)
    # Get the boosts available to the current user
    # boosting_rate = request.user.boost
    mining_speed = request.user.mining
    counter = request.user.counter

    if request.method == "POST":
        boost_rate = request.POST.get('booster_value')
        needed = request.POST.get('needed_value')
        boost_id = request.POST.get('boost_id')
        if boost_rate and boost_id:
            if counter.value <= int(needed):
                response_message = "Insufficient Balance"
                messages.info(request, response_message)
            else:
                counter.value -= int(needed)
                counter.save()
                mining_speed.speed += int(boost_rate)
                mining_speed.save()
                boost_delete = Boost.objects.get(id=boost_id)
                boost_delete.assigned_users.remove(request.user)
                response_message = "Successfully Boosted"
                messages.success(request, response_message)
        
                return redirect('/boost')

    context = {
        'boosting_rate': boosting_rate,
    }
    return render(request, 'boost.html', context)





@login_required
def taskList(request):
    counter = request.user.counter
    user_tasks = TaskList.objects.filter(assigned_users=request.user)

    if request.method == "POST":
        task_value = request.POST.get('taskvalue')
        task_id = request.POST.get('task_id')
        print(task_id)
        redirect_url = request.POST.get('redirect_url')

        if task_value and task_id:
            counter.value += int(task_value)
            counter.save()

            task = TaskList.objects.get(id=task_id)
            task.assigned_users.remove(request.user)
            return redirect(redirect_url)
            messages.success(request, f"Task '{task.Taskname}' completed successfully!")


        return redirect('/task')

    context = {"tasklist": user_tasks}
    return render(request, 'task.html', context)




from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import UserSession  # Import the custom UserSession model
from django.contrib.sessions.models import Session



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Counter, Mining, Boost, TaskList, Level

# Sign-up View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()

            # Create related models for the new user
            Counter.objects.create(user=user, value=0)  # Create Counter for the new user
            Mining.objects.create(user=user, speed=3000)  # Create Mining with default speed
            Boost.objects.create(user=user, boost_name='Default', boost_value=0, needed_coin=0, level='level_1')  # Default boost
            TaskList.objects.create(user=user)  # You might need to add specific fields for TaskList
            Level.objects.create(user=user, level=1)  # Default level 1 for the new user

            # Log the user in after successful registration
            login(request, user)
            return redirect('home')  # Redirect to the home page or dashboard after signup

    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def wallet(request):
    return render(request, 'wallet.html')

## invite logic 
