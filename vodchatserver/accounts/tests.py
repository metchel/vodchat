from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignupForm

# Create your tests here.
class LoginAndRedirectTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='aAE$Ol0w0#K(ws')
        user.save()

    def test_upload_redirect_if_not_logged_in(self):
        response = self.client.get('/videos/upload')
        self.assertRedirects(response, '/accounts/login?next=/videos/upload')

    def test_upload_when_logged_in(self):
        login = self.client.login(username='test', password='aAE$Ol0w0#K(ws')
        response = self.client.get('/videos/upload')
        self.assertEqual(str(response.context['user']), 'test')
        self.assertEqual(response.status_code, 200)

class SignUpFormErrorMessagesTest(TestCase):
     def test_username_error_messages(self):
        form = SignupForm()
        self.assertEqual(form.fields['username'].error_messages, {'required':'Please enter an username.'})

     def test_email_error_messages(self):
       form = SignupForm()
       self.assertEqual(form.fields['email'].error_messages, {'required':'Please enter your email.'})

     def test_password_error_messages(self):
       form = SignupForm()
       self.assertEqual(form.fields['password'].error_messages, {'required':'Please enter a password.'})

     def test_password_confirm_error_messages(self):
        form = SignupForm()
        self.assertEqual(form.fields['password_confirm'].error_messages, {'required':'Please confirm you password.'})
