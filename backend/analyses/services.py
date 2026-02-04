import numpy as np
import math

class BettingEngine:
    """
    Engine de processamento utilizando NumPy.
    Ordem dos dados: [Mais Recente -> Mais Antigo]
    Classe responsável pelos cálculos matemáticos do Bet Smart.
    Foco: Precisão estatística em séries temporais curtas.
    """

    # Constantes com as Médias Gerais por Campeonato
    LEAGUE_MEANS = {
        'Bundesliga': {'goals': 3.20, 'corners_h1': 4.41, 'shots_h1': 5.8},
        'Saudi_Pro_League': {'goals': 2.96, 'corners_h1': 4.85, 'shots_h1': 4.2},
        'Jupiler_League': {'goals': 2.52, 'corners_h1': 4.48, 'shots_h1': 4.6},
        'Brasileirao': {'goals': 3.00, 'corners_h1': 5.00, 'shots_h1': 4.5},
        'La_Liga': {'goals': 2.62, 'corners_h1': 4.69, 'shots_h1': 5.1},
        'Ligue_1': {'goals': 2.85, 'corners_h1': 4.32, 'shots_h1': 5.2},
        'Premier_League': {'goals': 2.79, 'corners_h1': 4.63, 'shots_h1': 5.9},
        'Championship': {'goals': 2.58, 'corners_h1': 4.73, 'shots_h1': 4.9},
        'Serie_A': {'goals': 2.40, 'corners_h1': 4.02, 'shots_h1': 5.0},
        'Eredivisie': {'goals': 3.24, 'corners_h1': 4.95, 'shots_h1': 5.4},
        'Liga_Portugal': {'goals': 2.77, 'corners_h1': 4.39, 'shots_h1': 4.4},
        'Super_Lig': {'goals': 2.61, 'corners_h1': 4.44, 'shots_h1': 4.8},
    }

    # Fatores multiplicadores para Favorito jogando FORA
    AWAY_MULTIPLIERS = {
        'goals': 0.82,
        'corners_h1': 0.88,
        'shots_h1': 0.90
    }

    @staticmethod
    def calculate_weighted_mean(data_list):
        """
        Calcula a média ponderada de uma lista de 5 elementos.
        Ordem esperada: [Mais Recente, Jogo 2, Jogo 3, Jogo 4, Mais Antigo]
        """
        # 1. Validação: O sistema exige exatamente 5 jogos para manter o peso 1-5
        if not data_list or len(data_list) != 5:
            return 0
        
        # 2. Conversão para Array NumPy (Otimização de memória e performance)
        values = np.array(data_list)
        
        # 3. Definição dos pesos (Atribuindo maior importância ao índice 0)
        weights = np.array([5, 4, 3, 2, 1])
        
        # 4. Cálculo da Média Ponderada
        # np.average realiza a soma dos produtos e divide pela soma dos pesos automaticamente
        weighted_avg = np.average(values, weights=weights)
        
        return float(weighted_avg)

    @staticmethod
    def calculate_safety_line(data_list):
        """
        Analisa a consistência dos dados e gera um valor conservador.
        Fórmula: média_ponderada - (0.5 * desvio_padrão)
        """
        # 1. Validação mínima para cálculo de desvio padrão amostral
        if not data_list or len(data_list) < 2:
            return 0
        
        # 2. Transformação em Array NumPy
        values = np.array(data_list)
        
        # 3. Recuperação da Média Ponderada (da Subetapa 3.2)
        mean_w = BettingEngine.calculate_weighted_mean(data_list)
        
        # 4. Cálculo do Desvio Padrão Amostral
        # Desvio padrão populacional (ddof=0) ou amostral (ddof=1)
        # Usaremos ddof=1 para maior rigor com amostras pequenas
        # ddof=1 (Delta Degrees of Freedom) é usado para amostras, tornando o cálculo mais preciso para um conjunto pequeno de 5 partidas.
        std_dev = np.std(values, ddof=1)
        
        # 5. Cálculo da Linha de Segurança
        safety_line = mean_w - (0.5 * std_dev)
        
        # 6. Retorno garantindo que o valor não seja negativo (clipping)
        # Se o desvio for muito alto, a conta poderia resultar em algo menor que zero.
        return max(0.0, float(safety_line))

    @staticmethod
    def calculate_lambda(fav_history, dog_history, league_name, event_type, is_away=False):
        """
        Calcula o Lambda (expectativa) usando Força Relativa e Fator Multiplicador.
        Fórmula: ((média_fav + média_dog) / média_league) * fator (se away)
        """
        # 1. Obter médias ponderadas
        mean_fav = BettingEngine.calculate_weighted_mean(fav_history)
        mean_dog = BettingEngine.calculate_weighted_mean(dog_history)
        
        # 2. Obter média da liga para o evento específico
        league_avg = BettingEngine.LEAGUE_MEANS.get(league_name, {}).get(event_type, 1.0)
        
        # 3. Cálculo da expectativa base (Força Relativa)
        # Se a soma dos times for maior que a da liga, o lambda será > 1
        expectation = (mean_fav * mean_dog) / league_avg
        
        # 4. Aplicar fator multiplicador se o favorito for visitante
        if is_away:
            multiplier = BettingEngine.AWAY_MULTIPLIERS.get(event_type, 1.0)
            expectation *= multiplier
            
        return max(0.01, expectation) # Lambda não pode ser zero para Poisson

    @staticmethod
    def poisson_probability(lambda_val, k):
        """Distribuição de Poisson para probabilidade de exatamente k eventos."""
        return (math.exp(-lambda_val) * (lambda_val**k)) / math.factorial(k)

    @staticmethod
    def run_full_analysis(match_data):
        """
        Orquestra todos os cálculos: Gols, Finalizações e Escanteios.
        Recebe um dicionário com históricos e informações da liga.
        """
        league = match_data.get('league')
        is_away = match_data.get('is_away', False)

        # --- 1. PREVISÃO DE GOLS ---
        lambda_goals = BettingEngine.calculate_lambda(
            match_data['fav_goals_history'],
            match_data['dog_goals_conceded_history'],
            league, 'goals', is_away
        )
        # O resultado final da expectativa é o próprio Lambda ajustado
        prediction_goals = round(lambda_goals, 2)

        # --- 2. PREVISÃO DE FINALIZAÇÕES (1T) ---
        lambda_shots = BettingEngine.calculate_lambda(
            match_data['fav_shots_h1_history'],
            match_data['dog_shots_conceded_h1_history'],
            league, 'shots_h1', is_away
        )
        prediction_shots = round(lambda_shots, 2)

        # --- 3. PREVISÃO DE ESCANTEIOS (1T) ---
        lambda_corners = BettingEngine.calculate_lambda(
            match_data['fav_corners_h1_history'],
            match_data['dog_corners_conceded_h1_history'],
            league, 'corners_h1', is_away
        )
        prediction_corners = round(lambda_corners, 2)

        # Retornamos um dicionário formatado para ser salvo no Model
        return {
            'prediction_goals': prediction_goals,
            'prediction_shots_h1': prediction_shots,
            'prediction_corners_h1': prediction_corners,
        }  