from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse

# Create your tests here.
class Tests(TestCase):
    def setUp(self) -> None:
        self.username = 'JJTest'
        self.email = 'test@memphis.edu.edu'
        self.password = 'H3||0w0r|d'
    
    def test_register_url(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')
    
    def test_homepage_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='home.html')
    
    def test_register_form(self):
            response = self.client.post(reverse('register'), data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            })
            
            self.assertEqual(response.status_code, 302)
            users = get_user_model().objects.all()
            self.assertEqual(users.count(), 1)
   
