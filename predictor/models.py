from django.db import models

class LearnerData(models.Model):
    # Identifying Info
    learner_id = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    
    # Dates
    enrollment_date = models.DateField()
    enrollment_month = models.IntegerField()
    enrollment_day_of_week = models.IntegerField()
    
    # Core Metrics
    time_spent_hours = models.FloatField()
    interaction_count = models.IntegerField()
    video_completion_rate = models.FloatField()
    assessment_score = models.FloatField()
    feedback_score = models.FloatField()
    
    # Calculated/Engineered Features
    avg_completion_rate = models.FloatField()
    avg_assessment_score = models.FloatField()
    engagement_score = models.FloatField()
    
    # Binary Flags (1 or 0)
    completion_status = models.IntegerField()
    anomaly_flag = models.IntegerField()
    is_high_feedback = models.IntegerField()
    course_quality_label = models.IntegerField()

    def __str__(self):
        return f"Learner {self.learner_id} - Course {self.course_id}"