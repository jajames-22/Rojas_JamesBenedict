from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg
from .forms import LearnerDataForm
import joblib
import pandas as pd
import os

# Import the database model
from .models import LearnerData

# ==========================================
# 1. MACHINE LEARNING SETUP (Loads Once)
# ==========================================
BASE_DIR = settings.BASE_DIR
MODEL_PATH = os.path.join(BASE_DIR, 'saved_models', 'best_course_quality_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'saved_models', 'robust_scaler.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'saved_models', 'selected_features.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
selected_features = joblib.load(FEATURES_PATH)

# ==========================================
# 2. MACHINE LEARNING PREDICTOR VIEW
# ==========================================
def predict_quality(request):
    result = None
    # Create a list of dictionaries with clean labels for the UI
    feature_list = [{'id': f, 'label': f.replace('_', ' ').title()} for f in selected_features]

    if request.method == 'POST':
        try:
            # Capture data from the form
            input_data = {}
            # Inside predict_quality view:
            for feature in selected_features:
                val = request.POST.get(feature)
                
                if val is None:
                    # Checkbox was unchecked or data missing, default to 0
                    input_data[feature] = [0.0]
                else:
                    # Platform dropdown, text input, or checked box
                    input_data[feature] = [float(val)]
            
            # Convert and Scale
            input_df = pd.DataFrame(input_data)
            input_scaled = scaler.transform(input_df)
            
            # Predict
            prediction = model.predict(input_scaled)[0]
            result = "High Quality" if prediction == 1 else "Low Quality"
            
        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'predictor/index.html', {
        'feature_list': feature_list,
        'result': result
    })

# ==========================================
# 3. DASHBOARD VIEW (MySQL)
# ==========================================
def dashboard_view(request):
    try:
        # Count total rows directly from MySQL
        total_learners = f"{LearnerData.objects.count():,}"

        # Calculate averages using Django's database aggregation
        averages = LearnerData.objects.aggregate(
            avg_score=Avg('assessment_score'),
            avg_interaction=Avg('interaction_count'),
            avg_prod=Avg('engagement_score')
        )

        # Format the averages safely
        avg_score = round(averages['avg_score'], 1) if averages['avg_score'] else "0.0"
        avg_interaction = int(averages['avg_interaction']) if averages['avg_interaction'] else "0"
        avg_prod = round(averages['avg_prod'], 2) if averages['avg_prod'] else "0.00"

        context = {
            'total_learners': total_learners,
            'avg_score': avg_score,
            'avg_interaction': avg_interaction,
            'avg_prod': avg_prod,
        }
    except Exception as e:
        context = {'error': f"Database error: {str(e)}"}

    return render(request, 'predictor/dashboard.html', context)

# ==========================================
# 4. DATA TABLE VIEW (MySQL + Pagination)
# ==========================================
# ==========================================
# 4. DATA TABLE VIEW (MySQL + Pagination + Modals)
# ==========================================
def view_data(request):
    try:
        # Fetch actual objects so we can bind them to the Edit Forms
        records = LearnerData.objects.all().order_by('-id')

        # Set up pagination
        paginator = Paginator(records, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Create a list pairing each row's data with a pre-filled Edit Form
        table_data = []
        for obj in page_obj:
            table_data.append({
                'data': obj,
                'edit_form': LearnerDataForm(instance=obj)
            })

        # Create one empty form for the Add Data Modal
        add_form = LearnerDataForm()

        columns = ['ID', 'Learner ID', 'Course ID', 'Platform', 'Status', 'Score', 'Time (Hrs)', 'Interactions', 'Engagement']
        error = None
    except Exception as e:
        page_obj = None
        table_data = []
        add_form = None
        columns = []
        error = f"Database error: {str(e)}"

    return render(request, 'predictor/data.html', {
        'page_obj': page_obj,
        'table_data': table_data,
        'add_form': add_form,
        'columns': columns,
        'error': error
    })

# ==========================================
# 5. CRUD OPERATIONS (Add, Edit, Delete)
# ==========================================
def add_record(request):
    if request.method == 'POST':
        form = LearnerDataForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('view_data')

def edit_record(request, pk):
    record = get_object_or_404(LearnerData, pk=pk)
    if request.method == 'POST':
        form = LearnerDataForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
    return redirect('view_data')

def delete_record(request, pk):
    record = get_object_or_404(LearnerData, pk=pk)
    record.delete()
    return redirect('view_data')