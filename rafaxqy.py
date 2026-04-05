import requests
import capsolver
import json
import random
from dotenv import load_dotenv
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
capsolver.api_key = os.getenv("CAPSOLVER_API_KEY")

SITES = {
    "1": {
        "nome": "9G.bet",
        "url": "https://www.9g7.vip",
        "api": "https://api-br.9gapi.com/global/v5_oeiwjd/register.php",
        "captcha_id": "d8186cb6256e78b0a8ff5f412911477e"
    }
}

lock = threading.Lock()
sucesso = 0
falha = 0

def boas_vindas():
    print("=" * 40)
    print("   Bem vindo Rafaxqy! 👋")
    print("=" * 40)
    print("\nSites disponíveis:")
    for key, site in SITES.items():
        print(f"  [{key}] {site['nome']}")
    escolha = input("\nQual site deseja usar? ")
    if escolha not in SITES:
        print("❌ Site inválido!")
        exit()
    return SITES[escolha]

def gerar_telefone():
    ddd = random.choice(["11","21","31","32","41","44","47","51","55","61","71","81","91","27","48"])
    numero = "99" + "".join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{ddd}{numero}"

def gerar_senha():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "Aa1@" + "".join(random.choices(chars, k=8))

def registrar_conta(site, numero):
    global sucesso, falha
    telefone = gerar_telefone()
    senha = gerar_senha()

    print(f"[{numero}] Registrando: {telefone} | Resolvendo captcha...")

    try:
        solution = capsolver.solve({
            "type": "GeeTestTaskProxyLess",
            "websiteURL": site["url"],
            "captchaId": site["captcha_id"]
        })

        captcha_content = json.dumps({
            "captcha_id": solution["captcha_id"],
            "lot_number": solution["lot_number"],
            "pass_token": solution["pass_token"],
            "gen_time": solution["gen_time"],
            "captcha_output": solution["captcha_output"]
        })

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": site["url"],
            "Referer": site["url"] + "/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        }

        payload = {
            "phone": "55" + telefone,
            "pd": senha,
            "captcha_k": "",
            "captcha_v": "",
            "version": "v43",
            "cpf": "",
            "is_new": "1",
            "captcha_version": "1",
            "captcha_content": captcha_content,
            "pid": "share"
        }

        response = requests.post(site["api"], headers=headers, data=payload)
        resultado = response.json()

        if resultado.get("res") == 0:
            key = resultado.get("key", "")
            uid = resultado.get("uid", "")
            with lock:
                sucesso += 1
                print(f"[{numero}] ✅ Conta criada! {telefone} | Senha: {senha} | Key: {key}")
                with open("contas.txt", "a") as f:
                    f.write(f"{telefone}:{senha}:{key}:{uid}\n")
        else:
            with lock:
                falha += 1
                print(f"[{numero}] ❌ Falhou: {resultado}")

    except Exception as e:
        with lock:
            falha += 1
            print(f"[{numero}] ❌ Erro: {e}")

# Início
site = boas_vindas()
quantidade = int(input("Quantas contas criar? "))
threads = int(input("Quantas simultâneas? (recomendado: 3-5) "))

print(f"\n🚀 Iniciando {quantidade} contas com {threads} threads simultâneas...\n")

with ThreadPoolExecutor(max_workers=threads) as executor:
    futures = [executor.submit(registrar_conta, site, i+1) for i in range(quantidade)]
    for future in as_completed(futures):
        future.result()

print(f"\n{'='*40}")
print(f"✅ Sucesso: {sucesso} | ❌ Falha: {falha}")
print(f"Contas salvas em contas.txt")
print(f"{'='*40}")

#Agora ele cria várias contas ao mesmo tempo! Recomendo usar **3-5 threads** para não sobrecarregar a API do CapSolver.