from django.db import models

class Match(models.Model):
    # --- Informações Básicas da Partida ---
    home_team = models.CharField(max_length=100, verbose_name="Time Mandante")
    away_team = models.CharField(max_length=100, verbose_name="Time Visitante")
    favorite_team = models.CharField(max_length=100, verbose_name="Time Favorito")
    match_date = models.DateField(verbose_name="Data da Partida")
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Dados de Entrada (Últimas 5 Partidas) ---
    # Usamos JSONField para armazenar listas como [1, 0, 2, 1, 3]
    
    # Do Time Favorito (Ataque)
    fav_goals_history = models.JSONField(default=list, verbose_name="Gols feitos (Últimos 5)")
    fav_shots_h1_history = models.JSONField(default=list, verbose_name="Finalizações 1T (Últimos 5)")
    fav_corners_h1_history = models.JSONField(default=list, verbose_name="Escanteios 1T (Últimos 5)")

    # Do Time Zebra (Defesa/Cedidos)
    underdog_goals_conceded_history = models.JSONField(default=list, verbose_name="Gols sofridos (Últimos 5)")
    underdog_shots_conceded_h1_history = models.JSONField(default=list, verbose_name="Finalizações sofridas 1T (Últimos 5)")
    underdog_corners_conceded_h1_history = models.JSONField(default=list, verbose_name="Escanteios sofridos 1T (Últimos 5)")

    # --- Campos de Saída (Resultados do Processamento) ---
    # Estes campos serão preenchidos pela nossa "Engine Matemática" na Etapa 3
    prediction_goals = models.FloatField(null=True, blank=True, verbose_name="Previsão de Gols")
    prediction_shots_h1 = models.FloatField(null=True, blank=True, verbose_name="Previsão Finalizações 1T")
    prediction_corners_h1 = models.FloatField(null=True, blank=True, verbose_name="Previsão Escanteios 1T")

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date}"

    class Meta:
        verbose_name = "Partida"
        verbose_name = "Partidas"
        ordering = ['-match_date']