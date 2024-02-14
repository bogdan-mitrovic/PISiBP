from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from tinymce.widgets import TinyMCE

from .models import Category, News, News_draft, UserProfile


class Add_news_Form(forms.ModelForm):
    title = forms.CharField(max_length = 250, required=True)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField(required=False)
    is_up_for_review = forms.BooleanField(required=False)
    class Meta:
        model = News_draft
        fields = ['title', 'tags', 'content', 'category', 'image', 'is_up_for_review' ]
    def __init__(self, *args, **kwargs):
        category_queryset = kwargs.pop('category_queryset', None)
        super().__init__(*args, **kwargs)

        if category_queryset is not None:
            self.fields['category'].queryset = category_queryset

#used when adding a news article, creating a news_draft to be reviewed




class Edit_news_Form(forms.ModelForm):
    title = forms.CharField(max_length = 250, required=True)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField(required=False)
    class Meta:
        model = News
        fields = ['title', 'tags', 'content', 'image']

#used when editing an existing news article, will be used to create a news_draft 
#based on the existing instance of news




class Edit_draft_Form(forms.ModelForm):
    title = forms.CharField(max_length = 250, required=True)
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    image = forms.ImageField(required=False)
    is_up_for_review = forms.BooleanField(required=False)
    class Meta:
        model = News_draft
        fields = ['title', 'tags', 'content', 'image', 'is_up_for_review' ]

    def clean_image(self):
        cleaned_data = super().clean()
        image_changed = 'image' in self.changed_data

        # Check if the image field has changed and if there is an old image
        if image_changed and self.instance.image:
            old_image_path = self.instance.image.path

            # Delete the old image
            default_storage.delete(old_image_path)

        return cleaned_data['image']

#used when editing an existing news_draft




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

#used when the superuser is registering a new user




class CustomUserEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False,label="Editor")
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ('is_staff', 'categories')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        user_instance = kwargs.get('instance')

        if user_instance:
            initial_categories = user_instance.user_profile.categories.all()
            self.fields['categories'].initial = initial_categories

    def clean_categories(self):
        return list(self.cleaned_data.get('categories', []))

#used when a superuser is editing one of the user's privileges



class CustomJournalistEditForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ('categories',)
    def __init__(self, *args, **kwargs):
        editor_categories = kwargs.pop('editor_categories', None)
        super().__init__(*args, **kwargs)

        user_instance = kwargs.get('instance')

        if user_instance:
            initial_categories = user_instance.user_profile.categories.all()
            self.fields['categories'].initial = initial_categories

        if editor_categories:
            self.fields['categories'].queryset = editor_categories


    def clean_categories(self):
        return list(self.cleaned_data.get('categories', []))

#used when an editor want's to manage category privileges of one of journalist's
    


#simple form, used when creating a comment
class Comment_text_Form(forms.Form):
    text = forms.CharField(widget=forms.Textarea ,  label='Komentar', max_length=100)
    news_id = forms.CharField()
    text.widget.attrs.update({'class':'form-control', 'rows':'5'})
    news_id.widget = forms.HiddenInput()

    
