from django.contrib import admin

from auctionapp.models import *

@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    pass

@admin.register(ArchivedItem)
class ArchivedItemAdmin(admin.ModelAdmin):
    pass