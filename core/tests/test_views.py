from base64 import b64decode
from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from users.tests.factories import AdminUserFactory, UserFactory

from ..serializers import CustomUserSerializer, UserProfileSerializer
from .factories import CustomUserFactory, UserProfileFactory

TEST_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
)


class TestCustomUser(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.instance = CustomUserFactory()

    def test_list(self):
        """Test that CustomUser collection can be listed"""

        resp = self.client.get("/api/v1/core/custom-user/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["id"], self.instance.id)

    def test_get(self):
        """Test that an instance of CustomUser can be retrieved"""

        resp = self.client.get(f"/api/v1/core/custom-user/{self.instance.id}/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], self.instance.id)

    def test_anonymous_create_fails(self):
        """Test that anonymous users can't create a new CustomUser"""

        resp = self.client.post("/api/v1/core/custom-user/")
        self.assertEqual(resp.status_code, 403)

    @patch("core.views.CustomUserViewSet.get_serializer")
    def test_create(self, mock_get_serializer):
        """Test create view for CustomUser"""

        self.client.force_authenticate(user=self.user)
        serializer = mock_get_serializer.return_value
        serializer.is_valid.return_value = True
        serializer.data = CustomUserSerializer(self.instance).data

        resp = self.client.post("/api/v1/core/custom-user/", {})
        self.assertEqual(resp.status_code, 201)

        mock_get_serializer.assert_called_once_with(data={})
        serializer.save.assert_called_once_with()

    def test_anonymous_update_fails(self):
        """Test that anonymous users can't update an existing CustomUser"""

        resp = self.client.patch(f"/api/v1/core/custom-user/{self.instance.id}/", {})
        self.assertEqual(resp.status_code, 403)

    def test_update(self):
        """Test CustomUser update"""

        self.client.force_authenticate(user=self.admin)
        resp = self.client.patch(f"/api/v1/core/custom-user/{self.instance.id}/", {})
        self.assertEqual(resp.status_code, 200)

    def test_anonymous_delete_fails(self):
        """Test that anonymous users can't delete CustomUser"""

        resp = self.client.delete(f"/api/v1/core/custom-user/{self.instance.id}/")
        self.assertEqual(resp.status_code, 403)

    def test_delete(self):
        """Test CustomUser deletion"""

        self.client.force_authenticate(user=self.admin)
        resp = self.client.delete(f"/api/v1/core/custom-user/{self.instance.id}/")

        self.assertEqual(resp.status_code, 204)


class TestUserProfile(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = UserFactory()
        self.admin = AdminUserFactory()
        self.instance = UserProfileFactory()

    def test_list(self):
        """Test that UserProfile collection can be listed"""

        resp = self.client.get("/api/v1/core/user-profile/")
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["id"], self.instance.id)

    def test_get(self):
        """Test that an instance of UserProfile can be retrieved"""

        resp = self.client.get(f"/api/v1/core/user-profile/{self.instance.id}/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], self.instance.id)

    def test_anonymous_create_fails(self):
        """Test that anonymous users can't create a new UserProfile"""

        resp = self.client.post("/api/v1/core/user-profile/")
        self.assertEqual(resp.status_code, 403)

    @patch("core.views.UserProfileViewSet.get_serializer")
    def test_create(self, mock_get_serializer):
        """Test create view for UserProfile"""

        self.client.force_authenticate(user=self.user)
        serializer = mock_get_serializer.return_value
        serializer.is_valid.return_value = True
        serializer.data = UserProfileSerializer(self.instance).data

        resp = self.client.post("/api/v1/core/user-profile/", {})
        self.assertEqual(resp.status_code, 201)

        mock_get_serializer.assert_called_once_with(data={})
        serializer.save.assert_called_once_with()

    def test_anonymous_update_fails(self):
        """Test that anonymous users can't update an existing UserProfile"""

        resp = self.client.patch(f"/api/v1/core/user-profile/{self.instance.id}/", {})
        self.assertEqual(resp.status_code, 403)

    def test_update(self):
        """Test UserProfile update"""

        self.client.force_authenticate(user=self.admin)
        resp = self.client.patch(f"/api/v1/core/user-profile/{self.instance.id}/", {})
        self.assertEqual(resp.status_code, 200)

    def test_anonymous_delete_fails(self):
        """Test that anonymous users can't delete UserProfile"""

        resp = self.client.delete(f"/api/v1/core/user-profile/{self.instance.id}/")
        self.assertEqual(resp.status_code, 403)

    def test_delete(self):
        """Test UserProfile deletion"""

        self.client.force_authenticate(user=self.admin)
        resp = self.client.delete(f"/api/v1/core/user-profile/{self.instance.id}/")

        self.assertEqual(resp.status_code, 204)

    @patch("django.core.files.storage.FileSystemStorage.save")
    def test_upload_banner(self, mock_save):
        """Test uploading UserProfile.banner"""

        self.client.force_authenticate(user=self.admin)
        mock_save.return_value = "images/test.png"

        with override_settings(
            DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage"
        ):
            resp = self.client.put(
                f"/api/v1/core/user-profile/{self.instance.id}/upload_banner/",
                TEST_PNG,
                content_type="image/png",
                HTTP_CONTENT_DISPOSITION='attachment; filename="test.png"',
            )
        self.assertEqual(resp.status_code, 204)
        mock_save.assert_called_once()

    @patch("django.core.files.storage.FileSystemStorage.save")
    def test_upload_profile_picture(self, mock_save):
        """Test uploading UserProfile.profile_picture"""

        self.client.force_authenticate(user=self.admin)
        mock_save.return_value = "images/test.png"

        with override_settings(
            DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage"
        ):
            resp = self.client.put(
                f"/api/v1/core/user-profile/{self.instance.id}/upload_profile_picture/",
                TEST_PNG,
                content_type="image/png",
                HTTP_CONTENT_DISPOSITION='attachment; filename="test.png"',
            )
        self.assertEqual(resp.status_code, 204)
        mock_save.assert_called_once()
