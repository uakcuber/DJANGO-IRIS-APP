# iris_app/views.py

# 1. Standart Kütüphaneler
import csv
import io

# 2. Django Çekirdek Modülleri
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# 3. Rest Framework (API)
from rest_framework import viewsets

# 4. Scikit-Learn (Yapay Zeka)
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

# 5. Kendi Uygulamanızın Dosyaları
from .models import IrisPlant, Location
from .forms import IrisPlantForm
from .decorators import writer_required
# Eğer serializers.py dosyan yoksa bu satır hata verir, aşağıda onu da vereceğim.
from .serializers import IrisPlantSerializer 

# --- IMPORT / EXPORT ---
@writer_required
def data_import_export(request):
    if request.method == "POST":
        # --- EXPORT İŞLEMİ ---
        if 'export_data' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="iris_plants.csv"'

            writer = csv.writer(response)
            writer.writerow(['Species', 'Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width', 'Location'])

            plants = IrisPlant.objects.all()
            for plant in plants:
                loc_name = plant.location.city if plant.location else ''
                writer.writerow([
                    plant.species, 
                    plant.sepal_length, 
                    plant.sepal_width, 
                    plant.petal_length, 
                    plant.petal_width, 
                    loc_name
                ])
            return response

        # --- IMPORT İŞLEMİ ---
        elif 'import_data' in request.POST:
            csv_file = request.FILES.get('csv_file')

            if not csv_file:
                messages.error(request, "Lütfen bir dosya seçin.")
                return redirect('data_import_export')

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Bu bir CSV dosyası değil.")
                return redirect('data_import_export')

            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) 

            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                try:
                    location_obj = None
                    if len(column) > 5 and column[5].strip():
                        city_name = column[5].strip()
                        location_obj, _ = Location.objects.get_or_create(city=city_name)

                    _, created = IrisPlant.objects.update_or_create(
                        sepal_length=float(column[1]),
                        sepal_width=float(column[2]),
                        petal_length=float(column[3]),
                        petal_width=float(column[4]),
                        defaults={
                            'species': column[0],
                            'location': location_obj
                        }
                    )
                except Exception as e:
                    print(f"Satır hatası: {e}")
                    continue

            messages.success(request, "Veriler başarıyla yüklendi.")
            return redirect('plant_list')

    return render(request, 'import_export.html')

# --- KULLANICI İŞLEMLERİ ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('plant_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- CRUD İŞLEMLERİ ---
@login_required
def plant_list(request):
    plants = IrisPlant.objects.all().order_by('-created_at')
    is_writer = request.user.groups.filter(name='Writer').exists()
    context = {
        'plants': plants,
        'is_writer': is_writer,
    }
    return render(request, 'plant_list.html', context)

@writer_required
def plant_create(request):
    if request.method == 'POST':
        form = IrisPlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plant_list')
    else:
        form = IrisPlantForm()
    return render(request, 'plant_form.html', {'form': form, 'title': 'Yeni Bitki Ekle'})

@writer_required
def plant_update(request, pk):
    plant = get_object_or_404(IrisPlant, pk=pk)
    if request.method == "POST":
        form = IrisPlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant_list')
    else:
        form = IrisPlantForm(instance=plant)
    return render(request, 'plant_form.html', {'form': form, 'title': 'Bitkiyi Düzenle'})

@writer_required
def plant_delete(request, pk):
    plant = get_object_or_404(IrisPlant, pk=pk)
    if request.method == "POST":
        plant.delete()
        return redirect('plant_list')
    return render(request, 'plant_confirm_delete.html', {'plant': plant})

# --- ARAMA ---
@login_required
def plant_search(request):
    plants = IrisPlant.objects.all().order_by('-created_at')

    query_species = request.GET.get('species')
    query_sepal = request.GET.get('min_sepal')
    query_city = request.GET.get('city')

    if query_species:
        plants = plants.filter(species__icontains=query_species)
    if query_sepal:
        plants = plants.filter(sepal_length__gte=query_sepal)
    if query_city:
        plants = plants.filter(location__city__icontains=query_city)

    context = {'plants': plants}
    return render(request, 'plant_search.html', context)

# --- BONUS: API VIEWSET ---
class IrisPlantViewSet(viewsets.ModelViewSet):
    queryset = IrisPlant.objects.all()
    serializer_class = IrisPlantSerializer

# --- BONUS: YAPAY ZEKA TAHMİNİ ---
@login_required
def predict_species(request):
    prediction = None
    selected_algo = ''
    confidence = 0

    if request.method == 'POST':
        sepal_length = float(request.POST.get('sepal_length'))
        sepal_width = float(request.POST.get('sepal_width'))
        petal_length = float(request.POST.get('petal_length'))
        petal_width = float(request.POST.get('petal_width'))
        selected_algo = request.POST.get('algorithm')

        iris = load_iris()
        X = iris.data
        y = iris.target

        if selected_algo == 'knn':
            model = KNeighborsClassifier(n_neighbors=3)
        elif selected_algo == 'dt':
            model = DecisionTreeClassifier()
        else:
            model = LogisticRegression(max_iter=200)

        model.fit(X, y)

        input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
        
        prediction_index = model.predict(input_data)[0]
        prediction = iris.target_names[prediction_index]

        probs = model.predict_proba(input_data)[0]
        raw_confidence = max(probs) * 100
        confidence = round(raw_confidence, 1)

    return render(request, 'predict.html', {
        'prediction': prediction,
        'selected_algo': selected_algo,
        'confidence': confidence
    })