from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
from ..models import Category
from ..models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    is_staff = forms.BooleanField(required=False,label="Editor")
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'categories')
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user)
            user_profile.categories.set(self.cleaned_data['categories'])
        return user



class CustomUserEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False,label="Editor")
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ('is_staff', 'categories')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retrieve the user instance being edited
        user_instance = kwargs.get('instance')

        # Set initial values for categories based on user's existing privileges
        if user_instance:
            initial_categories = user_instance.user_profile.categories.all()
            self.fields['categories'].initial = initial_categories

    def clean_categories(self):
        # Ensure the categories field returns a list of category objects
        return list(self.cleaned_data.get('categories', []))



class CustomJournalistEditForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ('categories',)
    def __init__(self, *args, **kwargs):
        editor_categories = kwargs.pop('editor_categories', None)
        super().__init__(*args, **kwargs)

        # Retrieve the user instance being edited
        user_instance = kwargs.get('instance')

        # Set initial values for categories based on user's existing privileges
        if user_instance:
            initial_categories = user_instance.user_profile.categories.all()
            self.fields['categories'].initial = initial_categories

        if editor_categories:
            # Assume you have a way to identify the editor, such as a user type field
            # Adjust this condition based on your actual user model structure
            self.fields['categories'].queryset = editor_categories


    def clean_categories(self):
        # Ensure the categories field returns a list of category objects
        return list(self.cleaned_data.get('categories', []))
