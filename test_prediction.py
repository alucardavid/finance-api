"""
Script de teste para verificar as melhorias na predição de categorias
"""
import requests
import json

# URL da API
API_URL = "http://localhost:8000/monthly-expenses/category-predict"

# Exemplos de despesas para testar
test_cases = [
    {"description": "Uber Uber *Trip Help.U", "expected_category": "Transporte"},
    {"description": "Amazonprimebr", "expected_category": "Streaming"},
    {"description": "Ebn *Crunchyroll", "expected_category": "Transporte/Combustível"}
]

print("="*80)
print("TESTE DE PREDIÇÃO DE CATEGORIAS - MODELO MELHORADO")
print("="*80)
print()

for i, test_case in enumerate(test_cases, 1):
    try:
        response = requests.post(
            API_URL,
            json={
                "description": test_case["description"],
                "place": "",
                "amount": 0,
                "date": "2026-01-25",
                "total_plots": 1,
                "current_plot": 1,
                "due_date": "2026-01-25",
                "status": "Pendente",
                "form_of_payment_id": 1,
                "expense_category_id": 24,  # 24 = Desconhecido
                "balance_id": 1
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            confidence = result.get('confidence', 0) * 100
            category_id = result.get('category_id')
            below_threshold = result.get('predicted_below_threshold', False)
            
            status_icon = "✓" if not below_threshold else "⚠"
            confidence_color = "ALTA" if confidence >= 80 else "MÉDIA" if confidence >= 60 else "BAIXA"
            
            print(f"{status_icon} Teste {i}: {test_case['description']}")
            print(f"   Categoria prevista: {category_id}")
            print(f"   Confiança: {confidence:.1f}% ({confidence_color})")
            if below_threshold:
                print(f"   ⚠ Confiança abaixo do threshold - retornou 'Desconhecido'")
            print()
        else:
            print(f"✗ Teste {i}: Erro {response.status_code}")
            print(f"   {response.text}")
            print()
            
    except Exception as e:
        print(f"✗ Teste {i}: Erro na requisição - {str(e)}")
        print()

print("="*80)
print("Teste completo!")
print("="*80)
