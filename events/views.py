from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, TrainingSite
# Import User Model From Django
from django.contrib.auth.models import User
from .forms import TrainingSiteForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages

# Import PDF Stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import Pagination Stuff
from django.core.paginator import Paginator


# Show Event
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {
        "event": event
    })


# Show Events In A TrainingSite
def site_events(request, site_id):
    # Grab the site
    site = TrainingSite.objects.get(id=site_id)
    # Grab the events from that site
    events = site.event_set.all()
    if events:
        return render(request, 'events/site_events.html', {
            "events": events
        })
    else:
        messages.success(request, ("That TrainingSite Has No Events At This Time..."))
        return redirect('admin_approval')


# Create Admin Event Approval Page
def admin_approval(request):
    # Get The TrainingSites
    site_list = TrainingSite.objects.all()
    # Get Counts
    event_count = Event.objects.all().count()
    site_count = TrainingSite.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            # Get list of checked box id's
            id_list = request.POST.getlist('boxes')

            # Uncheck all events
            event_list.update(approved=False)

            # Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)

            # Show Success Message and Redirect
            messages.success(request, ("Event List Approval Has Been Updated!"))
            return redirect('list-events')



        else:
            return render(request, 'events/admin_approval.html',
                          {"event_list": event_list,
                           "event_count": event_count,
                           "site_count": site_count,
                           "user_count": user_count,
                           "site_list": site_list})
    else:
        messages.success(request, ("You aren't authorized to view this page!"))
        return redirect('home')

    return render(request, 'events/admin_approval.html')


# Create My Events Page
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(volunteers=me)
        return render(request,
                      'events/my_events.html', {
                          "events": events
                      })

    else:
        messages.success(request, ("You Aren't Authorized To View This Page"))
        return redirect('home')


# Generate a PDF File TrainingSite List
def site_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    # lines = [
    #  "This is line 1",
    #  "This is line 2",
    #  "This is line 3",
    # ]

    # Designate The Model
    sites = TrainingSite.objects.all()

    # Create blank list
    lines = []

    for site in sites:
        lines.append(site.name)
        lines.append(site.address)
        lines.append(site.zip_code)
        lines.append(site.phone)
        lines.append(site.web)
        lines.append(site.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='site.pdf')


# Generate CSV File TrainingSite List
def site_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=sites.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    sites = TrainingSite.objects.all()

    # Add column headings to the csv file
    writer.writerow(['TrainingSite Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])

    # Loop Thu and output
    for site in sites:
        writer.writerow([site.name, site.address, site.zip_code, site.phone, site.web, site.email_address])

    return response


# Generate Text File TrainingSite List
def site_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=sites.txt'
    # Designate The Model
    sites = TrainingSite.objects.all()

    # Create blank list
    lines = []
    # Loop Thu and output
    for site in sites:
        lines.append(
            f'{site.name}\n{site.address}\n{site.zip_code}\n{site.phone}\n{site.web}\n{site.email_address}\n\n\n')

    # lines = ["This is line 1\n",
    # "This is line 2\n",
    # "This is line 3\n\n",
    # "John Elder Is Awesome!\n"]

    # Write To TextFile
    response.writelines(lines)
    return response


# Delete a TrainingSite
def delete_site(request, site_id):
    site = TrainingSite.objects.get(pk=site_id)
    site.delete()
    return redirect('list-sites')


# Delete an Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!!"))
        return redirect('list-events')
    else:
        messages.success(request, ("You Aren't Authorized To Delete This Event!"))
        return redirect('list-events')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                # form.save()
                event = form.save(commit=False)
                event.manager = request.user  # logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # Just Going To The Page, Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html',
                  {'event': event,
                   'form': form})


def update_site(request, site_id):
    site = TrainingSite.objects.get(pk=site_id)
    form = TrainingSiteForm(request.POST or None, request.FILES or None, instance=site)
    if form.is_valid():
        form.save()
        return redirect('list-sites')

    return render(request, 'events/update_site.html',
                  {'site': site,
                   'form': form})


def search_sites(request):
    if request.method == "POST":
        searched = request.POST['searched']
        sites = TrainingSite.objects.filter(name__contains=searched)

        return render(request,
                      'events/search_sites.html',
                      {'searched': searched,
                       'sites': sites})
    else:
        return render(request,
                      'events/search_sites.html',
                      {})


def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)

        return render(request,
                      'events/search_events.html',
                      {'searched': searched,
                       'events': events})
    else:
        return render(request,
                      'events/search_events.html',
                      {})


def show_site(request, site_id):
    site = TrainingSite.objects.get(pk=site_id)
    site_owner = User.objects.get(pk=site.owner)

    # Grab the events from that site
    events = site.event_set.all()

    return render(request, 'events/show_site.html',
                  {'site': site,
                   'site_owner': site_owner,
                   'events': events})


def list_sites(request):
    # site_list = TrainingSite.objects.all().order_by('?')
    site_list = TrainingSite.objects.all()

    # Set up Pagination
    p = Paginator(TrainingSite.objects.all(), 3)
    page = request.GET.get('page')
    sites = p.get_page(page)
    nums = "a" * sites.paginator.num_pages
    return render(request, 'events/site.html',
                  {'site_list': site_list,
                   'sites': sites,
                   'nums': nums}
                  )


def add_site(request):
    submitted = False
    if request.method == "POST":
        form = TrainingSiteForm(request.POST, request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.owner = request.user.id  # logged in user
            site.save()
            # form.save()
            return HttpResponseRedirect('/add_site?submitted=True')
    else:
        form = TrainingSiteForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_site.html', {'form': form, 'submitted': submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/event_list.html',
                  {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Soldier"
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year

    # Query the Events Model For Dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    )

    # Get current time
    time = now.strftime('%I:%M %p')
    return render(request,
                  'events/home.html', {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "current_year": current_year,
                      "time": time,
                      "event_list": event_list,
                  })
