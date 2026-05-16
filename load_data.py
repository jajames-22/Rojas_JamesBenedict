import os
import django
import pandas as pd

# 1. Setup Django environment so this script can talk to your database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course_quality_system.settings')
django.setup()

# 2. Import your new MySQL Model
from predictor.models import LearnerData

def run_import():
    csv_path = os.path.join('saved_models', 'course_quality_label_final_cleaned.csv')
    
    print("Reading CSV file...")
    df = pd.read_csv(csv_path)
    
    # CRITICAL FIX: Replace any blank/NaN cells with 0 so MySQL doesn't crash
    df = df.fillna(0)
    
    print("Clearing any old data from the database...")
    LearnerData.objects.all().delete()
    
    print(f"Found {len(df)} records. Preparing for insertion...")
    
    # 3. Translate CSV rows into Django Database Objects
    db_records = []
    for index, row in df.iterrows():
        record = LearnerData(
            learner_id=row['learner_id'],
            course_id=row['course_id'],
            platform=row['platform'],
            enrollment_date=row['enrollment_date'],
            enrollment_month=row['enrollment_month'],
            enrollment_day_of_week=row['enrollment_day_of_week'],
            time_spent_hours=row['time_spent_hours'],
            interaction_count=row['interaction_count'],
            video_completion_rate=row['video_completion_rate'],
            assessment_score=row['assessment_score'],
            feedback_score=row['feedback_score'],
            avg_completion_rate=row['avg_completion_rate'],
            avg_assessment_score=row['avg_assessment_score'],
            engagement_score=row['engagement_score'],
            completion_status=row['completion_status'],
            anomaly_flag=row['anomaly_flag'],
            is_high_feedback=row['is_high_feedback'],
            course_quality_label=row['course_quality_label']
        )
        db_records.append(record)
        
    # 4. Insert everything into MySQL at once
    LearnerData.objects.bulk_create(db_records)
    print(f"Success! {len(db_records)} records were securely added to MySQL 8.4.")

if __name__ == '__main__':
    run_import()