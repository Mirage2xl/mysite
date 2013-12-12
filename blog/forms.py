from django import forms
from haystack.forms import SearchForm


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SubscribeForm(forms.Form):
    email = forms.EmailField()


class PostSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
