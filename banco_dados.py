import requests
import os

FIREBASE_URL = "https://fortnite-tracker-elementais-default-rtdb.firebaseio.com"
ARQUIVO_SESSAO = "sessao_login.txt" 

def carregar_banco():
    try:
        response = requests.get(f"{FIREBASE_URL}/colecao.json", timeout=3)
        if response.status_code == 200 and response.json():
            data = response.json()
            for user, vals in data.items():
                if not isinstance(vals, dict):
                    data[user] = {
                        "senha": "", "avatar": "", "musica": "hud.mp3",
                        "vbucks": 0, "avatares_comprados": [], "musicas_compradas": [],
                        "colecao": {}
                    }
                else:
                    if "senha" not in vals: vals["senha"] = "" 
                    if "avatar" not in vals: vals["avatar"] = "" 
                    if "musica" not in vals: vals["musica"] = "hud.mp3"
                    if "vbucks" not in vals: vals["vbucks"] = 0 
                    if "avatares_comprados" not in vals: vals["avatares_comprados"] = []
                    if "musicas_compradas" not in vals: vals["musicas_compradas"] = []
                    if "colecao" not in vals: vals["colecao"] = {}
            return data
    except Exception:
        print("Aviso: Sem conexão com o Firebase (Modo Offline).")
    return {} 
    

def salvar_banco(dados):
    try:
        response = requests.put(f"{FIREBASE_URL}/colecao.json", json=dados, timeout=3)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

def deletar_conta(usuario):
    banco = carregar_banco()
    if usuario in banco:
        del banco[usuario]
        if salvar_banco(banco):
            limpar_sessao()
            return True
    return False

def ler_sessao():
    if os.path.exists(ARQUIVO_SESSAO):
        with open(ARQUIVO_SESSAO, "r") as f:
            return f.read().strip()
    return None

def salvar_sessao(usuario):
    with open(ARQUIVO_SESSAO, "w") as f:
        f.write(usuario)

def limpar_sessao():
    if os.path.exists(ARQUIVO_SESSAO):
        os.remove(ARQUIVO_SESSAO)

def carregar_elementais():
    try:
        response = requests.get(f"{FIREBASE_URL}/catalog.json", timeout=3)
        if response.status_code == 200 and response.json():
            return response.json()
    except Exception:
        pass
    return [{"nome": f"Elemental {i}", "arquivo": f"elemental_{i}.jpg"} for i in range(1, 37)]

def carregar_avatars():
    return ["avatar_1.jpg", "avatar_2.jpg", "avatar_3.jpg", "avatar_4.jpg", "avatar_5.jpg", "avatar_6","avatar_8","avatar_9","avatar_10","avatar_13","avatar_12"]

def carregar_avatars():
    # Retorna apenas as skins "Comuns" para a tela de registro de novos recrutas
    loja = carregar_loja_avatars()
    return [item["arquivo"] for item in loja if item["raridade"] == "comum"]

def carregar_loja_avatars():
    return [
        # --- OS SEUS AVATARES ATUAIS ---
        {"arquivo": "avatar_1.jpg", "nome": "O Ceifador", "raridade": "lendario", "preco": 500, "tag": ""},
        {"arquivo": "avatar_2.jpg", "nome": "Rapina", "raridade": "lendario", "preco": 500, "tag": "Main do Henrique"},
        {"arquivo": "avatar_3.jpg", "nome": "Foco", "raridade": "epico", "preco": 200, "tag": "A Braba da Emanuelly"},
        {"arquivo": "avatar_4.jpg", "nome": "Hera Venenosa", "raridade": "raro", "preco": 150, "tag": "Escolha do Talisson"},
        {"arquivo": "avatar_5.jpg", "nome": "Arlequina", "raridade": "incomum", "preco": 100, "tag": "Clássica do Jessé"},

        # --- OS 46 AVATARES NOVOS ---
        {"arquivo": "avatar_6.jpg", "nome": "Fabi Furtiva", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_7.jpg", "nome": "lil tecca", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_8.jpg", "nome": "mulher gato", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_9.jpg", "nome": "Ben 10", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_10.jpg", "nome": "Gwen", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_11.jpg", "nome": "Laufey", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_12.jpg", "nome": "Sintese", "raridade": "lendario", "preco": 500, "tag": ""},
        {"arquivo": "avatar_13.jpg", "nome": "Hoshimachi Suisei", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_14.jpg", "nome": "Grace", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_15.jpg", "nome": "Chappel Roan", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_16.jpg", "nome": "Zoey Golden", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_17.jpg", "nome": "Roan D'arc", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_18.jpg", "nome": "KizunaAI", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_19.jpg", "nome": "Coringa", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_20.jpg", "nome": "Kim Kardashian", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_21.jpg", "nome": "Gogo Yubari", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_22.jpg", "nome": "Lisa", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_23.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_24.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_25.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_26.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_27.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_28.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_29.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_30.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_31.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_32.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_33.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_34.jpg", "nome": "Skin Aleatória", "raridade": "comum", "preco": 10, "tag": ""},
        {"arquivo": "avatar_35.jpg", "nome": "velma", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_36.jpg", "nome": "fred", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_37.jpg", "nome": "scooby", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_38.jpg", "nome": "salsicha", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_39.jpg", "nome": "daphine", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_40.jpg", "nome": "zoey", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_41.jpg", "nome": "Rumi", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_42.jpg", "nome": "Mira", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_43.jpg", "nome": "Hana Park", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_44.jpg", "nome": "Tatsumaki", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_45.jpg", "nome": "Genos", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_46.jpg", "nome": "Saitama", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_47.jpg", "nome": "Ranger azul", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_48.jpg", "nome": "Ranger Amarelo", "raridade": "raro", "preco": 150, "tag": ""},
        {"arquivo": "avatar_49.jpg", "nome": "Ranger Vermelho", "raridade": "epico", "preco": 200, "tag": ""},
        {"arquivo": "avatar_50.jpg", "nome": "Ranger Rosa", "raridade": "incomum", "preco": 100, "tag": ""},
        {"arquivo": "avatar_51.jpg", "nome": "Ranger Preto", "raridade": "raro", "preco": 150, "tag": ""},
    ]

def carregar_loja_musicas():
    # Músicas com capas locais para o design em formato de Card
    return [
        {"nome": "Mannie Fresh - Real Big", "arquivo": "realbig.mp3", "capa": "realbig.mp4", "preco": 100},
        {"nome": "BIRDMAN", "arquivo": "birdman.mp3", "capa": "capa_birdman.mp4", "preco": 150},
        {"nome": "FUNK CIRCULATION", "arquivo": "FUNKCIRCULATION.mp3", "capa": "FUNKCIRCULATION.mp4", "preco": 200},
        {"nome": "Crank That", "arquivo": "CrankThat.mp3", "capa": "CrankThat.mp4", "preco": 200},
        {"nome": "Barracuda (1977)", "arquivo": "Barracuda.mp3", "capa": "Barracuda.mp4", "preco": 200},
        {"nome": "Caneta azul", "arquivo": "CanetaAzul.mp3", "capa": "CanetaAzul.mp4", "preco": 200}
    ]