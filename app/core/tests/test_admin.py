""" Test custom admin commands """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from core.admin import UserCreationForm, UserChangeForm, UserAdmin
from django.contrib.auth import get_user_model

from django.urls import reverse
from django.test import Client


User = get_user_model()


class AdminSiteTests(TestCase):
    """Tests for django admin."""

    def setUp(self):
        """Create user and client"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            name="Test user"
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


class UserCreationFormTest(TestCase):
    """Test user creation in admin"""

    def test_password_match(self):
        """Test passwords that match"""
        form_data = {
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_do_not_match(self):
        """Test passwords that do not match"""
        form_data = {
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass456",
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["Passwords don't match"])

    def test_save_user(self):
        """Test saving user"""
        form_data = {
            "email": "test@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        }

        form = UserCreationForm(data=form_data)
        user = form.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))


class UserChangeFormTest(TestCase):
    """Test user change form in admin"""

    def test_password_field_is_read_only(self):
        """Test that the password field is read only"""
        form = UserChangeForm()
        self.assertIsInstance(
            form.fields["password"], ReadOnlyPasswordHashField)

    def test_form_has_expected_fields(self):
        form = UserChangeForm()
        expected_fields = ["email", "password", "is_active", "is_staff"]
        form_fields = list(form.fields.keys())
        self.assertEqual(form_fields, expected_fields)


class UserAdminTest(TestCase):
    def test_admin_attributes(self):
        """Test attributes of UserAdmin class"""

        admin_instance = UserAdmin(User, None)

        self.assertEqual(admin_instance.form, UserAdmin.form)
        self.assertEqual(admin_instance.add_form, UserAdmin.add_form)
        self.assertEqual(admin_instance.list_display, [
                         "email", "name", "is_staff"])
        self.assertEqual(admin_instance.list_filter, ["is_staff"])

        self.assertEqual(
            admin_instance.fieldsets,
            [
                (None, {"fields": ["email", "password"]}),
                ("Permissions", {"fields": ["is_staff"]}),
            ],
        )
        self.assertEqual(
            admin_instance.add_fieldsets,
            [
                (
                    None,
                    {
                        "classes": ["wide"],
                        "fields": ["email", "password1", "password2", "name", "is_active", "is_staff", "is_superuser"],
                    },
                ),
            ],
        )
        self.assertEqual(admin_instance.search_fields, ["email"])
        self.assertEqual(admin_instance.ordering, ["id"])
        self.assertEqual(admin_instance.filter_horizontal, [])
