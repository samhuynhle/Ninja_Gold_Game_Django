from django.shortcuts import render, redirect
from random import randint

def home(request):
    if 'views' in request.session:
        request.session['views'] += 1
    else:
        request.session['views'] = 0
        set_session(request)
    
    return render(request, 'the_game/index.html')

def farm(request):
    if request.method == "POST":
        request.session['game_tracker'] += int(request.POST['time_cost'])
        request.session['get_gold'] = randint(15, 30)

        if request.session['buff'] > 1:
            buffed_amount = round(request.session['get_gold'] * (1 + request.session['buff']/100),2)
            request.session['total_gold'] += buffed_amount
            request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} day at the farm! You have earned {request.session['get_gold']} gold for a days worth of work! Since you also studied at the dojo beforehand your buff of {request.session['buff']}% has been applied, earning you a total of {buffed_amount} for the day! (Your buff has been reset) </li>")
            updategold(request)
            win_or_lose(request)
            return redirect('/')
        
        request.session['total_gold'] += request.session['get_gold']
        updategold(request)
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} day at the farm! You have earned {request.session['get_gold']} gold for a days worth of work! </li>")
        win_or_lose(request)
    return redirect('/')

def cave(request):
    if request.method == "POST":
        request.session['game_tracker'] += int(request.POST['time_cost'])
        request.session['get_gold'] = randint(0, 150)

        if request.session['buff'] > 1:
            buffed_amount = round(request.session['get_gold'] * (1 + request.session['buff']/100),2)
            request.session['total_gold'] += buffed_amount
            request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} days at searching through a deep cave! You discovered {request.session['get_gold']} gold! Since you also studied at the dojo beforehand your buff of {request.session['buff']}% has been applied, earning you a total of {buffed_amount} gold! (Your buff has been reset) </li>")
            updategold(request)
            win_or_lose(request)
            return redirect('/')

        request.session['total_gold'] += request.session['get_gold']
        updategold(request)
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} days at searching through a deep cave! You discovered {request.session['get_gold']} gold! </li>")
        win_or_lose(request)
    return redirect('/')

def casino(request):
    if request.method == "POST":
        request.session['game_tracker'] += int(request.POST['time_cost'])
        request.session['get_gold'] = randint(-100, 100)

        if request.session['get_gold'] < 0:
            request.session['gain_loss'] = 'red'
            request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} day at the casino! Unforunately, you lost {request.session['get_gold']} gold! </li>")
            request.session['gain_loss'] = 'green'
            request.session['total_gold'] += request.session['get_gold']
            updategold(request)
            win_or_lose(request)
            return redirect('/')

        if request.session['buff'] > 1:
            buffed_amount = round(request.session['get_gold'] * (1 + request.session['buff']/100),2)
            request.session['total_gold'] += buffed_amount
            request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} day at the casino! You have earned {request.session['get_gold']} gold for a days worth of gambling! Since you also studied at the dojo beforehand your buff of {request.session['buff']}% has been applied, earning you a total of {buffed_amount} for the day! (Your buff has been reset) </li>")
            win_or_lose(request)
            return redirect('/')
        
        request.session['total_gold'] += request.session['get_gold']
        updategold(request)
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent {request.POST['time_cost']} day at the casino! You have earned {request.session['get_gold']} gold for a days worth of gambling! </li>")
        win_or_lose(request)
        
    return redirect('/')

def dojo(request):
    if request.method == "POST":
        request.session['game_tracker'] += int(request.POST['time_cost'])
        request.session['buff'] = randint(0, 25)
    
        if request.session['buff'] == 0:
            request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> Unfortunately, you procrastinated and rested the whole day! You will have a buff of {request.session['buff']}% for the next activity. </li>")
        
        
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You spent the {request.POST['time_cost']} at the Dojo! You were diligent and earned yourself a {request.session['buff']}% buff for the next activity! </li>")
        win_or_lose(request)
    return redirect('/')

def reset(request):
    set_session(request)
    return redirect('/')

def updategold(request):
    request.session['rounded_gold'] = round(request.session['total_gold'],2)
    return request.session['rounded_gold']

def win_or_lose(request):
    if request.session['total_gold'] > request.session['user_goal']:
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You Win! </li>")
        request.session['end_game'] = 'none'
        return redirect('/')
    if request.session['total_gold'] < 0 or request.session['game_tracker'] >= request.session['user_ending']:
        request.session['end_game'] = 'none'
        request.session['gain_loss'] = 'red'
        request.session['game_history'].append(f"<li style='color: {request.session['gain_loss']}'> You Lose! </li>")
        return redirect('/')
    return redirect('/')

def rules(request):
    request.session['user_goal'] = int(request.POST['user_goal'])
    request.session['user_ending'] = int(request.POST['user_ending'])
    request.session['user_input_display'] = 'none'

    return redirect('/')

def set_session(request):
    request.session['total_gold'] = 0
    request.session['rounded_gold'] = round(request.session['total_gold'])
    request.session['game_history'] = []
    request.session['buff'] = 0
    request.session['game_tracker'] = 1
    request.session['gain_loss'] = 'green'
    request.session['end_game'] = 'inline-block'
    request.session['user_ending'] = 16
    request.session['user_goal'] = 500
    request.session['user_input_display'] = 'inline-block'
