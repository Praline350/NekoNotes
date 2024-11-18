import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client
from django import forms

from app_authentication.forms import LoginForm, SignupForm

User = get_user_model()


@pytest.mark.django_db
class TestLogin:
    def setup_method(self):
        self.client = Client()

    def test_login_form_valid_data(self):
        # Données valides pour le formulaire
        form_data = {
            "login_username": "testuser",
            "password": "securepassword123",
        }
        form = LoginForm(data=form_data)
        assert form.is_valid()  # Le formulaire doit être valide avec ces données

    def test_login_form_missing_username(self):
        # Tester le formulaire avec le champ login_username manquant
        form_data = {
            "password": "securepassword123",
        }
        form = LoginForm(data=form_data)
        assert not form.is_valid()  # Le formulaire doit être invalide
        assert "login_username" in form.errors  # L'erreur doit être liée à ce champ

    def test_login_form_missing_password(self):
        # Tester le formulaire avec le champ password manquant
        form_data = {
            "login_username": "testuser",
        }
        form = LoginForm(data=form_data)
        assert not form.is_valid()
        assert "password" in form.errors

    def test_login_view_get_authenticated_user_redirect(self):
        # Créer un utilisateur et se connecter
        user = User.objects.create_user(
            username="testuser", password="securepassword123"
        )
        self.client.login(username="testuser", password="securepassword123")

        # Effectuer une requête GET
        response = self.client.get(reverse("login"))

        # Vérifier que l'utilisateur authentifié est redirigé vers la page "home"
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_login_view_get_anonymous_user(self):
        # Requête GET pour un utilisateur non authentifié
        response = self.client.get(reverse("login"))

        # Vérifier que la page de connexion est chargée avec un formulaire
        assert response.status_code == 200
        assert (
            "login_form" in response.context
        )  # Vérifie que le formulaire est dans le contexte

    def test_login_view_post_valid_credentials(self):
        # Créer un utilisateur dans la base de données
        user = User.objects.create_user(
            username="testuser", password="securepassword123"
        )

        # Envoyer une requête POST avec des identifiants valides
        response = self.client.post(
            reverse("login"),
            data={"login_username": "testuser", "password": "securepassword123"},
        )

        # Vérifier que l'utilisateur est connecté et redirigé vers "home"
        assert response.status_code == 302
        assert response.url == reverse("home")
        assert response.wsgi_request.user.is_authenticated

    def test_login_view_post_invalid_credentials(self):
        # Envoyer une requête POST avec des identifiants invalides
        response = self.client.post(
            reverse("login"),
            data={"login_username": "wronguser", "password": "wrongpassword"},
        )

        # Vérifier que l'utilisateur reste sur la page de connexion
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated
        assert "Identifiants invalides" in response.content.decode()

    def test_login_view_post_invalid_form(self):
        # Envoyer une requête POST avec un formulaire incomplet
        response = self.client.post(
            reverse("login"), data={"login_username": "", "password": ""}
        )

        # Vérifier que l'utilisateur reste sur la page de connexion avec une erreur
        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated
        messages = list(get_messages(response.wsgi_request))
        assert any(
            "Erreur lors de l'inscription" in str(message) for message in messages
        )

    def test_logout(self):
        User.objects.create(username="testuser", password="securepassword123")
        self.client.login(username="testuser", password="securepassword123")
        url = reverse("logout")
        response = self.client.get(url)

        assert not "_auth_user_id" in self.client.session
        assert response.status_code == 302
        assert response.url == reverse("welcome")


@pytest.mark.django_db
class TestSignupForm:

    def test_signup_form_valid_data(self):
        # Données valides pour le formulaire d'inscription
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        form = SignupForm(data=form_data)
        assert form.is_valid()

    def test_signup_form_email_already_exists(self):
        # Création d'un utilisateur avec une adresse e-mail
        user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="password123",
        )

        # Formulaire d'inscription avec une adresse e-mail déjà utilisée
        form_data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors  # Vérifie que le formulaire rejette l'email
        assert str(user) == "existinguser"  # test __str__ model

    def test_signup_form_password_mismatch(self):
        # Mot de passe et confirmation ne correspondent pas
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "securepassword123",
            "password2": "differentpassword",
        }
        form = SignupForm(data=form_data)
        assert not form.is_valid()
        assert (
            "password2" in form.errors
        )  # Le formulaire doit signaler l'erreur de correspondance


@pytest.mark.django_db
class TestWelcomeView:

    def setup_method(self):
        self.client = Client()  # Client pour simuler les requêtes

    def test_get_welcome_view_anonymous(self):
        # Simuler une requête GET pour un utilisateur non authentifié
        response = self.client.get(reverse("welcome"))

        assert response.status_code == 200  # Le statut doit être 200
        assert (
            "signup_form" in response.context
        )  # Le formulaire doit être dans le contexte
        assert isinstance(response.context["signup_form"], SignupForm)

    def test_get_welcome_view_authenticated(self):
        # Créer et authentifier un utilisateur
        user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        # Simuler une requête GET pour un utilisateur authentifié
        response = self.client.get(reverse("welcome"))

        # L’utilisateur doit être redirigé vers la page "home"
        assert response.status_code == 302
        assert response.url == reverse("home")

    def test_post_signup_successful(self):
        # Simuler une inscription réussie avec les bonnes données
        response = self.client.post(
            reverse("welcome"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "securepassword123",
                "password2": "securepassword123",
            },
        )

        # L’utilisateur est redirigé vers la page "home" après l’inscription
        assert response.status_code == 302
        assert response.url == reverse("home")
        assert User.objects.filter(
            username="newuser"
        ).exists()  # Vérifie que l'utilisateur a bien été créé

    def test_post_signup_failed(self):
        # Tester une inscription avec des données invalides (mots de passe différents)
        response = self.client.post(
            reverse("welcome"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "password123",
                "password2": "differentpassword",
            },
        )

        # Le formulaire doit être invalide et rester sur la page d’inscription
        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))
        assert any(
            "Erreur lors de l'inscription" in str(message) for message in messages
        )  # Vérifie le message d'erreur
        assert (
            User.objects.filter(username="newuser").exists() is False
        )  # Vérifie qu'aucun utilisateur n'a été créé
