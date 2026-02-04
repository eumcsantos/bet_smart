from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from .services import BettingEngine

class MatchViewSet(viewsets.ModelViewSet):
    """
    ViewSet para lidar com a lógica da API de Partidas.
    POST: Recebe dados, calcula predições via Engine e salva.
    GET: Retorna a lista de análises para o Dashboard.
    """
    # Esta linha garante que APENAS usuários com Token JWT válido acessem os dados
    permission_classes = [IsAuthenticated]
    
    queryset = Match.objects.all().order_by('-created_at')
    serializer_class = MatchSerializer

    def perform_create(self, serializer):
        """
        Sobrescreve a criação para injetar a lógica da BettingEngine
        antes de salvar no banco de dados.
        """
        # 1. Recupera os dados validados do formulário/JSON
        data = serializer.validated_data
        
        # 2. Prepara o dicionário para o Orquestrador da Engine
        # Mapeamos os nomes do banco para o que a Engine espera
        match_info = {
            'league': data.get('league'),
            'is_away': data.get('is_away'),
            'fav_goals_history': data.get('fav_goals_history'),
            'fav_shots_h1_history': data.get('fav_shots_h1_history'),
            'fav_corners_h1_history': data.get('fav_corners_h1_history'),
            # Note: A engine usa as listas de 'conceded' (sofridos) do underdog
            'dog_goals_conceded_history': data.get('underdog_goals_conceded_history'),
            'dog_shots_conceded_h1_history': data.get('underdog_shots_conceded_h1_history'),
            'dog_corners_conceded_h1_history': data.get('underdog_corners_conceded_h1_history'),
        }

        # 3. Executa o Orquestrador (Engine Matemática)
        results = BettingEngine.run_full_analysis(match_info)

        # 4. Salva o registro no banco incluindo os resultados calculados
        serializer.save(
            prediction_goals=results['prediction_goals'],
            prediction_shots_h1=results['prediction_shots_h1'],
            prediction_corners_h1=results['prediction_corners_h1']
        )