import requests

FIREBASE_URL = "https://fortnite-tracker-elementais-default-rtdb.firebaseio.com"
resposta = requests.put(f"{FIREBASE_URL}/colecao.json", json={})

if resposta.status_code == 200:
    print("🔥 O buraco negro engoliu tudo! Contas deletadas com sucesso.")
else:
    print("Erro ao tentar resetar.")