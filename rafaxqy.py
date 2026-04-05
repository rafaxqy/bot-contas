import requests
import capsolver
import json
import random
from dotenv import load_dotenv
import os

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

def registrar_conta(site):
    telefone = gerar_telefone()
    senha = gerar_senha()

    print(f"\nRegistrando: {telefone}")
    print("Resolvendo captcha...")

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
        print(f"✅ Conta criada! Telefone: {telefone} | Senha: {senha} | Key: {key}")
        with open("contas.txt", "a") as f:
            f.write(f"{telefone}:{senha}:{key}:{uid}\n")
    else:
        print(f"❌ Falhou: {resultado}")

# Início
site = boas_vindas()
quantidade = int(input("Quantas contas criar? "))

for i in range(quantidade):
    print(f"\n--- Conta {i+1}/{quantidade} ---")
    registrar_conta(site)

print("\nConcluído! Contas salvas em contas.txt")