from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Item
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.safestring import mark_safe
#TODO GO through all stub view errors when done
def view_error(request):
    return render(request, "auctions/404.html")

class ItemCreateForm(forms.Form):
    item_name = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder': 'Item name', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    item_image = forms.CharField(max_length=512, required=False, widget=forms.TextInput(attrs={'placeholder': 'Item image URL', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    item_price = forms.FloatField(label="Item Price", widget=forms.NumberInput(attrs={'placeholder': 'Item Price'}))

class BidForm(forms.Form):
    price = forms.FloatField(label="Bid Price", widget=forms.NumberInput(attrs={'placeholder': 'Item Price'}))

class UpdatePersonalInfo(forms.Form):
    first_name = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder': 'First Name', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    last_name = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder': 'Last Name', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    address = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    dob_year = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "YYYY"}))
    dob_month = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "MM"}))
    dob_day = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': "DD"}))
class Search(forms.Form):
    SEARCH_TYPES = [
        ("profile", "Profile")
    ]
    query = forms.CharField(required=False, max_length=512, widget=forms.Textarea(attrs={'placeholder': 'Profile Name', 'rows': 1, "cols": 40, 'style': "overflow:hidden;resize:none;"}))
    query_type = forms.CharField(label="Search Type", widget=forms.Select(choices=SEARCH_TYPES))
def index(request):
    return render(request, "auctions/index.html", {
        'items': Item.objects.all()
    })

@login_required
def my_listings(request):
    return render(request, "auctions/listings.html", {
        'items': Item.objects.filter(user_id=request.user)
    })

def login_view(request, name="Default Name"):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if password == "":
            return render(request, "auctions/login.html", {
                "message": "Password can\'t be blank."
            })
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        if password == "":
            return render(request, "auctions/register.html", {
                "message": "Password can\'t be blank."
            })
        if username == "admin":
            return render(request, "auctions/register.html", {
                "message": "Reserved username. Please choose a different username"
            })
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if(request.method=="POST"):
        ItemCreator = ItemCreateForm(request.POST)
        if(ItemCreator.is_valid() == False):
            return render(request, "auctions/502.html", {})
        user = request.user
        item_image = ItemCreator.cleaned_data["item_image"]
        item_name = ItemCreator.cleaned_data["item_name"]
        item_price = ItemCreator.cleaned_data["item_price"]
        new_item = Item(user_id=user, name=item_name, current_price=item_price, price=item_price, image=item_image)
        new_item.save()
        return render(request, "auctions/done.html", {})
    return render(request, "auctions/create.html", {
        'form': ItemCreateForm()
    })

@login_required
def bid(request, name):
    try:
        test1 = int(name)
    except:
        return HttpResponseBadRequest("Not integer")
    if(test1 < 0):
        return HttpResponseBadRequest("Integer must be positive")
    item = Item.objects.filter(item_id=name)
    if(item.count() == 0):
        return HttpResponseBadRequest("No item found")
    item_query = item.get()
    if(request.method=="POST"):
        bid = BidForm(request.POST)
        if(bid.is_valid() == False):
            return render(request, "auctions/502.html", {})
        price = bid.cleaned_data["price"]
        if(price <= item_query.current_price):
            return render(request, "auctions/msg.html", {
                "title": "Invalid Price",
                "message": f"${price} is less than ${item_query.current_price}!"
            })
        item_query.current_price = price
        item_query.bidder = request.user.username
        item_query.save()
        return render(request, "auctions/msg.html", {
            "title": "Successfully added your new bid!",
            "message": f"Successfully added your new bid of {price} on item {item_query.name} successfully!"
        })
    return render(request, "auctions/bid.html", {
        "form": BidForm(),
        "iid": item_query.item_id
    })
def view(request, name):
    # Lots of checks
    try:
        test1 = int(name)
    except:
        return view_error(request)
    if(test1 < 0):
        return view_error(request)
    item = Item.objects.filter(item_id=name)
    if(item.count() == 0):
        return view_error(request)
    item_query = item.get()
    if(item_query.image == '' or item_query.image == ' '):
        pic = "No image provided"
    else:
        pic = item_query.image
    if(request.user.username == item_query.user_id.username):
        owner = True
    elif(request.user.username == "admin"):
        owner = True
    else:
        owner = False
    return render(request, "auctions/view.html", {
        "iowner": item_query.user_id.username,
        "iid": item_query.item_id,
        "iname": item_query.name,
        "ipic": pic,
        "icost": item_query.price,
        "icosthigh": item_query.current_price,
        "ibidder": item_query.bidder,
        "isowner": owner
    })

@login_required
def delete(request, name):
    # Lots of checks
    try:
        test1 = int(name)
    except:
        return view_error(request)
    if(test1 < 0):
        return view_error(request)
    item = Item.objects.filter(item_id=name)
    if(item.count() == 0):
        return view_error(request)
    item_query = item.get()
    if(request.user.username == item_query.user_id.username):
        owner = True
    elif(request.user.username == "admin"):
        owner = True
    else:
        owner = False
    if(owner == False):
        return render(request, "auctions/msg.html", {
            "title": "Error",
            "message": f"You are not the owner of {item_query.name}.\nYou may only delete item listings that you own."
        })
    item_query.delete()
    return HttpResponse("Done")

@login_required
def update_personal_info(request):
    user = request.user
    if(request.method == "POST"):
        pinfo = UpdatePersonalInfo(request.POST)
        if(pinfo.is_valid() == False):
            return render(request, "auctions/502.html", {})
        first_name = pinfo.cleaned_data["first_name"]
        last_name = pinfo.cleaned_data["last_name"]
        address = pinfo.cleaned_data["address"]
        dob_year = pinfo.cleaned_data["dob_year"]
        dob_month = pinfo.cleaned_data["dob_month"]
        dob_day = pinfo.cleaned_data["dob_day"]
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.dob = datetime(dob_year, dob_month, dob_day)
        user.save()
        return render(request, "auctions/msg.html", {
            "title": "Successfully updated your profile",
            "message": mark_safe("Your profile was updated successfully!<br /><a href=\"profile\">Back to your profile</a>")
        })
    return render(request, "auctions/profile.html", {
        "form": UpdatePersonalInfo(),
        "user": user,
        "dobmonth": user.dob.strftime("%B")
    })

def get_profile_info(request, name):
    username = User.objects.filter(username=name)
    if(username.count() == 0):
        return render(request, "auctions/msg.html", {
            "title": "Invalid user",
            "message": "The specified user could not be found!"
        })
    username = username.get()
    return render(request, "auctions/profile_view.html", {
        "user": username
    })

def search(request):
    if(request.method == "POST"):
        query = Search(request.POST)
        if(query.is_valid() == False):
            return render(request, "auctions/502.html", {})
        result = query.cleaned_data["query"]
        result_type = query.cleaned_data["query_type"]
        # All Profile List
        if(result == ""):
            users = User.objects.all()
            l = []
            for user in users.iterator():
                l.append(user)
            return render(request, "auctions/search_results.html", {
                "matches": l,
                "type": "profile",
                "input": "all"
            })

        # Exact match
        userlist = User.objects.all()
        filtered = userlist.filter(username=result)
        if(filtered.count() == 1):
            filtered = filtered.get()
            return HttpResponseRedirect("profile/" + filtered.username)
        
        # Similar search
        similar = []
        for user in userlist.iterator():
            name = user.username
            if(name.__contains__(result)):
                similar.append(user.username)
        print(similar)
        return render(request, "auctions/search_results.html", {
            "matches": similar,
            "type": "profile",
            "input": result
        })
    return render(request, "auctions/search.html", {
        "form": Search()
    })