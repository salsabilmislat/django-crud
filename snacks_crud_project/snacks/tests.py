from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="salsabil", email="salsabil@email.com", password="goodvibes"
        )

        self.snack = Snack.objects.create(
            title="Cereal", description="it is so good", purchaser=self.user,
        )

        self.snack1 = Snack.objects.create(
            title="hotdog", description="it looks so good", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "Cereal")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "Cereal")
        self.assertEqual(f"{self.snack.purchaser}", "salsabil")
        self.assertEqual(self.snack.description, "it is so good")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cereal")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "salsabil")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack1_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="2"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "hotdog")
        self.assertTemplateUsed(response, "snack_detail.html")

    
    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "pizza",
                "description": "it is so good",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="3"))
        self.assertContains(response, "it is so good")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Cereal","description":"really Good","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_thing_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="2"))
        self.assertEqual(response.status_code, 200)
