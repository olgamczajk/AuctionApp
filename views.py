from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *


@login_required
def home(request):
    items = AuctionItem.objects.all()
    return render(request, 'app/home.html', {'items': items})


def log_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('home')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def log_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/register.html', {'form': form})


@login_required
def add_item(request):
    if request.method == 'GET':
        form = AuctionItemForm()
        return render(request, 'app/add_item.html', {'form': form})
    if request.method == 'POST':
        form = AuctionItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = AuctionItem()
            item.title = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            item.start_price = form.cleaned_data['start_price']
            item.current_bid = form.cleaned_data['start_price']
            item.currency = form.cleaned_data['currency']
            item.image = form.cleaned_data['image']
            item.owner = request.user
            item.save()
            create_bid(request, item, item.start_price)
            return redirect('home')
    else:
        form = AuctionItemForm()
    return render(request, 'app/add_item.html', {'form': form})


def create_bid(request, item, bid_amount):
    new_bid = Bid()
    new_bid.amount = bid_amount
    new_bid.auction_item = item
    new_bid.bidder = request.user
    new_bid.save()
    return


@login_required
def item_detail(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    if item.owner != request.user:

        if request.method == 'GET':
            form = BidForm()
            form.fields['amount'].initial = item.current_bid
            return render(request, 'app/item_detail.html', {'item': item, 'form':form})
        if request.method == 'POST':
            form = BidForm(request.POST)
            if form.is_valid():
                bid_amount = form.cleaned_data['amount']
        # Validate bid amount
            if bid_amount <= item.current_bid:
                return render(request, 'app/item_detail.html', {'item': item, 'error_message': 'Bid amount must be higher than current bid'})

        # Update the current bid amount
            item.current_bid = bid_amount
            item.save()
            create_bid(request, item, bid_amount)
            return redirect('item_detail', item_id=item_id)

        return render(request, 'app/item_detail.html', {'item': item})
    else:
        if request.method == 'GET':
            form = BidForm()
            return render(request, 'app/item_detail.html', {'item': item})
        if request.method == 'POST':
            end_auction(request, item_id)
            return render(request, 'app/item_detail.html', {'item': item})


def end_auction(request, item_id):
    item = AuctionItem.objects.get(id=item_id)
    archive = ArchivedItem()
    archive.title = item.title
    archive.description = item.description
    archive.image = item.image
    archive.owner = item.owner
    archive.end_bid = item.current_bid
    archive.currency = item.currency
    buyer = Bid.objects.get(amount=item.current_bid)
    archive.buyer_username = buyer.bidder.username
    archive.buyer_email = buyer.bidder.email
    archive.save()
    item.delete()