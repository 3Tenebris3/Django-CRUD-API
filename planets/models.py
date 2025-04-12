from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=200)
    population = models.CharField(max_length=50)  # Handles large numbers or "unknown"
    terrains = models.TextField()  # Store as plain text; consider JSON or Array for advanced use
    climates = models.TextField()  # Same as terrains

    def __str__(self):
        return self.name
