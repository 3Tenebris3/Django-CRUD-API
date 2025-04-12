from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.management import call_command
from io import StringIO
from unittest.mock import patch, MagicMock
from .models import Planet

# --- Model Tests ---
class PlanetModelTest(TestCase):
    def setUp(self):
        self.planet = Planet.objects.create(
            name="TestPlanet",
            population="1000",
            terrains="desert",
            climates="arid"
        )

    def test_planet_str(self):
        # Verify the __str__ method returns the planet's name.
        self.assertEqual(str(self.planet), "TestPlanet")

# --- API (Integration) Tests ---
class PlanetAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a sample planet for testing.
        self.planet = Planet.objects.create(
            name="Tatooine",
            population="200000",
            terrains="desert",
            climates="arid"
        )
    
    def test_get_planets_list(self):
        # Tests GET /api/planets/
        url = reverse('planet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure at least one planet is returned.
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_planet_detail(self):
        # Tests GET /api/planets/<id>/
        url = reverse('planet-detail', kwargs={'pk': self.planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Tatooine")

    def test_create_planet(self):
        # Tests POST /api/planets/
        url = reverse('planet-list')
        data = {
            "name": "Dagobah",
            "population": "unknown",
            "terrains": "swamp",
            "climates": "murky"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Dagobah")

    def test_update_planet(self):
        # Tests PUT /api/planets/<id>/
        url = reverse('planet-detail', kwargs={'pk': self.planet.pk})
        data = {
            "name": "Tatooine Updated",
            "population": "250000",
            "terrains": "desert",
            "climates": "arid"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.name, "Tatooine Updated")

    def test_partial_update_planet(self):
        # Tests PATCH /api/planets/<id>/
        url = reverse('planet-detail', kwargs={'pk': self.planet.pk})
        data = {"population": "300000"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.population, "300000")

    def test_delete_planet(self):
        # Tests DELETE /api/planets/<id>/
        url = reverse('planet-detail', kwargs={'pk': self.planet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Planet.DoesNotExist):
            Planet.objects.get(pk=self.planet.pk)

# --- Management Command Test ---
class ImportPlanetsCommandTest(TestCase):
    @patch('planets.management.commands.import_planets.requests.post')
    def test_import_planets_command(self, mock_post):
        # Define a fake JSON response simulating data from the GraphQL API.
        fake_response_data = {
            "data": {
                "allPlanets": {
                    "planets": [
                        {
                            "name": "Hoth",
                            "population": "unknown",
                            "terrains": ["tundra", "ice caves", "mountain ranges"],
                            "climates": ["frozen"]
                        },
                        {
                            "name": "Endor",
                            "population": "30000000",
                            "terrains": ["forest"],
                            "climates": ["temperate"]
                        }
                    ]
                }
            }
        }
        # Configure the fake response.
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = fake_response_data
        mock_post.return_value = fake_response

        # Capture the output of the command.
        out = StringIO()
        call_command('import_planets', stdout=out)
        output = out.getvalue()
        # Check that the command output indicates that the planets were created.
        self.assertIn("Created planet: Hoth", output)
        self.assertIn("Created planet: Endor", output)
        # Verify the planets have been stored in the database.
        self.assertEqual(Planet.objects.count(), 2)
        hoth = Planet.objects.get(name="Hoth")
        self.assertEqual(hoth.population, "unknown")
