from django import forms
from .models import LearnerData

# 1. Define choices OUTSIDE the class so the Meta class can access it
PLATFORM_CHOICES = [
    (0, 'Coursera'),
    (1, 'edX'),
    (2, 'Udemy'),
    (3, 'FutureLearn'),
    (4, 'Skillshare'),
]

class LearnerDataForm(forms.ModelForm):
    class Meta:
        model = LearnerData
        fields = '__all__'
        widgets = {
            # 2. Turn Platform into a Dropdown
            'platform': forms.Select(choices=PLATFORM_CHOICES),
            
            # 3. Turn Flags into Checkboxes
            'completion_status': forms.CheckboxInput(),
            'anomaly_flag': forms.CheckboxInput(),
            'is_high_feedback': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Apply styling based on widget type
            if isinstance(field.widget, forms.CheckboxInput):
                # Bootstrap styling for checkboxes
                field.widget.attrs['class'] = 'form-check-input mb-2'
            else:
                # Bootstrap styling for Select and Number/Text inputs
                field.widget.attrs['class'] = 'form-control mb-2'