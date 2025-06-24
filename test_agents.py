#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o erro de importação circular foi resolvido
"""

print("=== TESTE DE IMPORTAÇÃO - NEWSLETTER ECONÔMICO ===\n")

try:
    print("1. Testando importação do logger_config...")
    from logger_config import logger
    print("   ✅ logger_config importado com sucesso")

    print("\n2. Testando importação do EconomicNewsletterAgent...")
    from EconomicNewsletterAgent import EconomicNewsletterAgent
    print("   ✅ EconomicNewsletterAgent importado com sucesso")

    print("\n3. Testando importação do CNNBrasilScraper...")
    from CNNBrasilScrapper import CNNBrasilScraper
    print("   ✅ CNNBrasilScraper importado com sucesso")

    print("\n4. Testando importação do EconomicNewsletterSystem...")
    from EconomyNewsletterSystem import EconomicNewsletterSystem
    print("   ✅ EconomicNewsletterSystem importado com sucesso")

    print("\n5. Testando inicialização do sistema...")
    system = EconomicNewsletterSystem()
    print("   ✅ Sistema inicializado com sucesso")

    print("\n🎉 TODOS OS TESTES PASSARAM!")
    print("\nO erro de importação circular foi RESOLVIDO!")

except Exception as e:
    print(f"\n❌ ERRO DURANTE O TESTE: {str(e)}")
    print("\nPor favor, verifique os arquivos corrigidos.")

print("\n" + "="*50)