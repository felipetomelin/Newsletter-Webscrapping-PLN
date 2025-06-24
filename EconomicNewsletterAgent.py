import warnings
from datetime import datetime
from logger_config import logger

warnings.filterwarnings('ignore')

class EconomicNewsletterAgent:
    # Classe base para todos os agentes

    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.processed_count = 0

    def log_activity(self, message: str) -> None:
        # Registra atividade do agente no log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{self.agent_id}] {self.name}: {message}")
        print(f"[{timestamp}] {self.name}: {message}")

print("\n=== SISTEMA COMPLETO DE 7 AGENTES PRONTO ===")