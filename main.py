from logger_config import logger
from EconomyNewsletterSystem import EconomicNewsletterSystem

# Função principal
def main():
    """Função principal para executar o sistema"""
    print("=" * 60)
    print("🤖 SISTEMA DE NEWSLETTER AUTOMÁTICO DE ECONOMIA - MULTI-AGENTE")
    print("=" * 60)
    print("\n📋 Iniciando sistema com 7 agentes especializados...\n")

    # Inicializar sistema
    system = EconomicNewsletterSystem()

    # Executar pipeline
    print("🚀 Executando pipeline completo...\n")
    result = system.run_pipeline()

    if result['status'] == 'success':
        print("\n✅ Newsletter gerado com sucesso!")
        print(f"📊 Estatísticas: {result['stats']['news_processed']} notícias processadas")
        print(f"📈 Tópicos aprovados: {result['stats']['topics_approved']}")
        print(f"🎯 Confiança das predições: {result['stats']['predictions_confidence']:.1%}")
        print(f"\n📧 Newsletter salvo em: outputs/{result['newsletter']}")
    else:
        print(f"\n❌ Erro ao gerar newsletter: {result.get('error', 'Erro desconhecido')}")

    print("\n" + "="*60)

# Executar se for o script principal
if __name__ == "__main__":
    main()