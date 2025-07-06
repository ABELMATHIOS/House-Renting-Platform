from django.contrib import admin
from .models import ListingModel, Booking, Revenue

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ('get_total_price',)
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'

class RevenueInline(admin.TabularInline):
    model = Revenue
    extra = 0
    readonly_fields = ('get_net_amount', 'get_created_at')
    
    def get_net_amount(self, obj):
        return obj.net_amount
    get_net_amount.short_description = 'Net Amount'
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'

@admin.register(ListingModel)
class ListingAdmin(admin.ModelAdmin):
    inlines = [BookingInline]
    list_display = ('title', 'property_type', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'get_guest_name', 'get_check_in', 'get_check_out', 'get_total_price')
    inlines = [RevenueInline]
    
    def get_guest_name(self, obj):
        return obj.guest_name
    get_guest_name.short_description = 'Guest Name'
    
    def get_check_in(self, obj):
        return obj.check_in
    get_check_in.short_description = 'Check In'
    
    def get_check_out(self, obj):
        return obj.check_out
    get_check_out.short_description = 'Check Out'
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Total Price'

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'homeowner', 'booking', 'amount', 'get_net_amount')
    readonly_fields = ('get_created_at',)
    
    def get_net_amount(self, obj):
        return obj.net_amount
    get_net_amount.short_description = 'Net Amount'
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'