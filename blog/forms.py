from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .models import Profile
User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "location", "website"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Write something about yourself..."}),
            "location": forms.TextInput(attrs={"placeholder": "City, Country"}),
            "website": forms.URLInput(attrs={"placeholder": "https://"}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "body", "image", "published"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "slug": forms.TextInput(attrs={"placeholder": "unique-slug-for-post"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a comment..."}
            )
        }
