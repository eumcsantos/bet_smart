from rest_framework import serializers
from .models import Match
from .services import BettingEngine

class MatchSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Match.
    Lida com a conversão entre o banco de dados e o formato JSON.
    """
    class Meta:
        model = Match
        # Listamos todos os campos que queremos enviar/receber da API
        fields = [
            'id', 'home_team', 'away_team', 'favorite_team', 
            'league', 'match_date', 'is_away',
            'fav_goals_history', 'fav_shots_h1_history', 'fav_corners_h1_history',
            'underdog_goals_conceded_history', 'underdog_shots_conceded_h1_history', 
            'underdog_corners_conceded_h1_history',
            'prediction_goals', 'prediction_shots_h1', 'prediction_corners_h1',
            'created_at'
        ]
        # Campos de leitura apenas (o frontend não envia, o backend gera)
        read_only_fields = [
            'id', 'prediction_goals', 'prediction_shots_h1', 
            'prediction_corners_h1', 'created_at'
        ]

    def validate(self, data):
        """
        Validação customizada: garante que todas as listas tenham 5 elementos.
        """
        history_fields = [
            'fav_goals_history', 'fav_shots_h1_history', 'fav_corners_h1_history',
            'underdog_goals_conceded_history', 'underdog_shots_conceded_h1_history',
            'underdog_corners_conceded_h1_history'
        ]

        for field in history_fields:
            if field in data and len(data[field]) != 5:
                raise serializers.ValidationError({
                    field: "É necessário fornecer exatamente 5 partidas para o histórico."
                })
        
        return data