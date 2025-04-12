import requests
import logging
from django.core.management.base import BaseCommand
from planets.models import Planet

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import planets from SWAPI GraphQL endpoint'

    def handle(self, *args, **kwargs):
        url = "https://swapi-graphql.netlify.app/graphql"
        query = """
        query {
          allPlanets {
            planets {
              name
              population
              terrains
              climates
            }
          }
        }
        """
        try:
            response = requests.post(url, json={'query': query})
            response.raise_for_status()  # This will raise HTTPError for bad responses
        except requests.RequestException as e:
            logger.error("Error fetching data from SWAPI: %s", e)
            self.stderr.write("Failed to fetch data from SWAPI GraphQL endpoint")
            return

        try:
            data = response.json()
        except ValueError as e:
            logger.error("Error parsing JSON response: %s", e)
            self.stderr.write("Invalid JSON response received from SWAPI")
            return

        planets_data = data.get('data', {}).get('allPlanets', {}).get('planets', [])
        if not planets_data:
            logger.warning("No planet data found in response.")
            self.stdout.write("No planets found to import.")
            return

        for planet_data in planets_data:
            # Use default values if missing
            planet, created = Planet.objects.update_or_create(
                name=planet_data.get('name'),
                defaults={
                    'population': planet_data.get('population') or 'unknown',
                    'terrains': ', '.join(planet_data.get('terrains') or []),
                    'climates': ', '.join(planet_data.get('climates') or []),
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} planet: {planet.name}")
