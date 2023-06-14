from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomAuthenticationForm, FileUploadForm
from django.shortcuts import redirect, render
from .forms import EnergyForm
from .models import Energy, AdminLog
from .utils import send_transaction
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
import json
from django.http import HttpResponseBadRequest, HttpResponse
import hashlib


# Renders the 'home.html' template for the home page
def home(request):
    return render(request, 'home.html')


# Authenticates a user based on the provided form data
def authenticate_user(request, form):
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bentornato, {username}.')
            return user
    messages.error(request, 'Username o password errati.')
    return None


# Redirects a user to the next page or the home page
def redirect_user(request, user):
    next_page = request.GET.get('next')
    if next_page and next_page != reverse('logout'):  # Adds a check to avoid redirection to the logout page
        return redirect(next_page)
    return redirect('home')


# Checks if the user has admin access and logs the admin access details
def check_admin_access(request, user):
    if user.is_superuser:
        current_admin = request.user.username
        current_ip_address = request.META.get('REMOTE_ADDR')
        try:
            last_log = AdminLog.objects.filter(admin_user=current_admin).latest('login_time')
            last_ip_address = last_log.last_ip_address
            if last_ip_address != current_ip_address:
                messages.warning(request,
                                 "Attenzione: l'ultimo accesso registrato per l'amministratore {} è stato "
                                 "effettuato da un indirizzo IP diverso ({}) "
                                 "rispetto all'accesso corrente.".format(
                                     current_admin, last_ip_address))
        except AdminLog.DoesNotExist:
            pass

        admin_log = AdminLog.objects.create(admin_user=current_admin, last_ip_address=current_ip_address)
        admin_log.login_time = timezone.now()
        admin_log.save()


# Handles the login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        user = authenticate_user(request, form)
        if user:
            check_admin_access(request, user)
            return redirect_user(request, user)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logs out the user and renders the 'logout.html' template
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')


# Displays an energy table for logged-in users
@login_required
def energy_table(request):
    # Retrieves Energy objects from the database, ordered by creation date in descending order
    energy = Energy.objects.order_by('-created_at')
    # Renders the 'energy_table.html' template, passing the energy objects as context
    return render(request, 'energy_table.html', {'energy': energy})


# Displays energy totals for logged-in superusers
@login_required
@user_passes_test(lambda u: u.is_superuser)
def energy_totals(request):
    # Retrieves the sum of produced and consumed energy values from the database
    total_produced = Energy.objects.aggregate(Sum('produced_energy_in_watt'))['produced_energy_in_watt__sum']
    total_consumed = Energy.objects.aggregate(Sum('consumed_energy_in_watt'))['consumed_energy_in_watt__sum']
    # Renders the 'energy_totals.html' template, passing the total produced and consumed energy as context
    return render(request, 'energy_totals.html', {'total_produced': total_produced, 'total_consumed': total_consumed})


# Handles the energy insertion view for logged-in superusers
@login_required
@user_passes_test(lambda u: u.is_superuser)
def insert_energy(request):
    if request.method == 'POST':
        energy_form = EnergyForm(request.POST)
        file_form = FileUploadForm(request.POST, request.FILES)

        if file_form.is_valid():
            file = file_form.cleaned_data['file']
            try:
                data = json.load(file)
                produced_energy = data.get('produced_energy_in_watt')
                consumed_energy = data.get('consumed_energy_in_watt')
                if not isinstance(produced_energy, int) or not isinstance(consumed_energy, int):
                    raise ValueError("I valori di energia devono essere numeri interi.")

                energy_form = EnergyForm(data={'produced_energy_in_watt': produced_energy, 'consumed_energy_in_watt': consumed_energy})
            except (json.JSONDecodeError, ValueError) as e:
                messages.error(request, f'File JSON non valido: {str(e)}')
                return redirect('insert_energy')

        if energy_form.is_valid():
            energy = energy_form.save(commit=False)
            energy.hash = hashlib.sha256(f"produced: {energy.produced_energy_in_watt}, consumed: {energy.consumed_energy_in_watt}".encode('utf-8')).hexdigest()
            energy.txId = send_transaction(f"produced: {energy.produced_energy_in_watt}, consumed: {energy.consumed_energy_in_watt}")
            energy.save()
            messages.success(request, 'Energia inserita con successo.')
            return redirect('energy_table')
        else:
            messages.error(request, 'Errore nel salvataggio dei dati di energia.')
    else:
        energy_form = EnergyForm()
        file_form = FileUploadForm()

    return render(request, 'insert_energy.html', {'energy_form': energy_form, 'file_form': file_form})


# Handles the access control view for logged-in superusers
@login_required
@user_passes_test(lambda u: u.is_superuser)
def access_control(request):
    logs = AdminLog.objects.order_by('-login_time')
    return render(request, 'access_control.html', {'logs': logs})


# Handles the file insertion view
def insert_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                data = json.load(file)
                produced_energy = data.get('produced_energy_in_watt')
                consumed_energy = data.get('consumed_energy_in_watt')
                if not isinstance(produced_energy, int) or not isinstance(consumed_energy, int):
                    raise ValueError("I valori di energia devono essere numeri interi.")

                return HttpResponse("File caricato con successo.")
            except (json.JSONDecodeError, ValueError) as e:
                return HttpResponseBadRequest(f"File JSON non valido: {str(e)}")
    else:
        form = FileUploadForm()
    return HttpResponse("Inserire un file valido.")

