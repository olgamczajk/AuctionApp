from django.db import models
from django.contrib.auth.models import User

class AuctionItem(models.Model):
    CURRENCIES = {
        "EUR": "EUR",
        "USD": "USD",
        "PLN": "PLN",
    }
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/images/')
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES)

class ArchivedItem(models.Model):
    CURRENCIES = {
        "EUR": "EUR",
        "USD": "USD",
        "PLN": "PLN",
    }
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images/')
    end_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    buyer_username = models.CharField(max_length=65)
    buyer_email = models.EmailField()

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of ${self.amount} on {self.item.title} by {self.bidder.username}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name