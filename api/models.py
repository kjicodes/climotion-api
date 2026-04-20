from django.db import models

class SearchedCity(models.Model):
    city_name = models.CharField(max_length=100, blank=False)

    class Meta:
        verbose_name = "Searched City"
        verbose_name_plural = "Searched Cities"

    def __str__(self):
        return self.city_name.capitalize()


class SavedWorkout(models.Model):
    exercise_type = models.CharField(max_length=100, blank=False)
    difficulty = models.CharField(max_length=100, blank=False)
    workout = models.JSONField(blank=False)
    workout_reflection_before = models.TextField(max_length=250, blank=True)
    workout_reflection_after = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Saved Workout"
        verbose_name_plural = "Saved Workouts"

    def __str__(self):
        return f"Saved workout {self.id}"


