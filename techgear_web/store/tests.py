from django.test import SimpleTestCase
from django.urls import reverse


class AuthenticationAccessTests(SimpleTestCase):
    def test_dashboard_redirects_anonymous_user(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_product_management_redirects_anonymous_user(self):
        response = self.client.get(reverse("product_create"))
        self.assertRedirects(response, reverse("login"), fetch_redirect_response=False)

    def test_logout_requires_post(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_catalog_is_public(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)


from unittest.mock import Mock, patch

from django.test import TestCase


class DashboardTests(TestCase):
    def _api_response(self, payload, status_code=200):
        response = Mock()
        response.status_code = status_code
        response.json.return_value = payload
        return response

    @patch("store.views.requests.get")
    def test_dashboard_loads_without_decorator_error(self, mock_get):
        def api_get(url, **kwargs):
            if url.endswith("/users/me"):
                return self._api_response({"nombre": "Administrador", "rol": "admin"})
            if url.endswith("/products"):
                return self._api_response([
                    {"id": "1", "nombre": "Equipo", "precio": "100", "stock": "2", "categoria": "Hardware"},
                    {"id": "2", "nombre": "Dato incompleto", "precio": "no-numero", "stock": None, "categoria": "Otros"},
                ])
            if url.endswith("/orders") or url.endswith("/users"):
                return self._api_response([])
            return self._api_response({}, 404)

        mock_get.side_effect = api_get
        session = self.client.session
        session["access_token"] = "token-de-prueba"
        session["rol"] = "admin"
        session.save()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PANEL PRINCIPAL")
        self.assertContains(response, "Administrador")

    @patch("store.views.requests.get")
    def test_private_list_helper_accepts_path_and_token(self, mock_get):
        from store.views import _fetch_private_list
        mock_get.return_value = self._api_response([])

        result = _fetch_private_list("/orders", "token")

        self.assertEqual(result, [])
        mock_get.assert_called_once()
