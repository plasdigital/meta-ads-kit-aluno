#!/usr/bin/env python3
"""
Meta Ads - Install Wizard
Verifica dependencias, token e conectividade com a API.

Uso: python3 scripts/setup.py
"""

import os
import sys
import shutil

GRAPH_VERSION = os.environ.get("META_GRAPH_VERSION", "v25.0")
REQUIRED_AD_PERMISSIONS = ("ads_read", "ads_management")


def load_env_file():
    """Load .env from the skill/project folder without requiring python-dotenv."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # A pasta atual primeiro (o aluno costuma rodar da raiz do kit), depois a raiz do kit.
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(base_dir, ".env"),
    ]

    seen = set()
    for env_path in candidates:
        env_path = os.path.abspath(env_path)
        if env_path in seen:
            continue
        seen.add(env_path)

        if not os.path.isfile(env_path):
            continue

        with open(env_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[7:]
                if "=" not in line:
                    continue

                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and not os.environ.get(key):
                    os.environ[key] = value

        return env_path

    return None


def check_python():
    v = sys.version_info
    ok = v.major >= 3 and v.minor >= 8
    status = "OK" if ok else "FALHOU"
    print(f"  [{status}] Python {v.major}.{v.minor}.{v.micro} (minimo: 3.8)")
    return ok


def check_sdk():
    try:
        import facebook_business
        version = getattr(facebook_business, '__version__', '?')
        print(f"  [OK] facebook-business SDK v{version}")
        return True
    except ImportError:
        print("  [FALHOU] facebook-business SDK nao instalado")
        print("           Instale com: pip3 install facebook-business")
        return False


def check_requests():
    try:
        import requests
        print(f"  [OK] requests v{requests.__version__}")
        return True
    except ImportError:
        print("  [FALHOU] requests nao instalado")
        print("           Instale com: pip3 install requests")
        return False


def check_permissions():
    token = os.environ.get("META_ADS_TOKEN")
    if not token:
        print("  [PULOU] Permissoes (sem token)")
        return False

    try:
        import requests
    except ImportError:
        print("  [PULOU] Permissoes (sem requests)")
        return False

    try:
        url = f"https://graph.facebook.com/{GRAPH_VERSION}/me/permissions"
        response = requests.get(url, params={"access_token": token}, timeout=20)
        response.raise_for_status()
        data = response.json().get("data", [])
    except Exception as e:
        print(f"  [FALHOU] Nao foi possivel ler permissoes: {e}")
        return False

    granted = {item.get("permission") for item in data if item.get("status") == "granted"}
    missing = [perm for perm in REQUIRED_AD_PERMISSIONS if perm not in granted]

    if missing:
        print("  [FALHOU] Token sem permissoes de Meta Ads")
        print(f"           Faltando: {', '.join(missing)}")
        print("           Gere um novo token com ads_read e ads_management")
        return False

    print("  [OK] Permissoes ads_read e ads_management concedidas")
    return True


def check_token():
    token = os.environ.get("META_ADS_TOKEN")
    if not token:
        print("  [FALHOU] META_ADS_TOKEN nao definida")
        print("           Copie o .env.exemplo para .env, na raiz do kit, e preencha:")
        print('           META_ADS_TOKEN="seu-token-aqui"')
        return False
    masked = token[:10] + "..." + token[-5:]
    print(f"  [OK] META_ADS_TOKEN definida ({masked})")
    return True


def check_account():
    account = os.environ.get("META_AD_ACCOUNT_ID")
    if not account:
        print("  [AVISO] META_AD_ACCOUNT_ID nao definida (opcional)")
        print("          Voce pode definir uma conta padrao no .env:")
        print('          META_AD_ACCOUNT_ID="act_123456789"')
        return True  # Optional, not a failure
    print(f"  [OK] META_AD_ACCOUNT_ID = {account}")
    return True


def check_api_connection():
    token = os.environ.get("META_ADS_TOKEN")
    if not token:
        print("  [PULOU] Teste de API (sem token)")
        return False

    try:
        import facebook_business
    except ImportError:
        print("  [PULOU] Teste de API (sem SDK)")
        return False

    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.user import User

    try:
        FacebookAdsApi.init(access_token=token)
        me = User(fbid="me")
        me.api_get(fields=["name", "id"])
        name = me.get("name", "?")
        uid = me.get("id", "?")
        print(f"  [OK] Conectado como: {name} (ID: {uid})")
        return True
    except Exception as e:
        print(f"  [FALHOU] Erro ao conectar na API: {e}")
        return False


def check_ad_accounts():
    token = os.environ.get("META_ADS_TOKEN")
    if not token:
        return False

    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.user import User
        FacebookAdsApi.init(access_token=token)
        me = User(fbid="me")
        accounts = me.get_ad_accounts(fields=["name", "id", "account_status"])
        acct_list = list(accounts)
        print(f"  [OK] {len(acct_list)} conta(s) de anuncio encontrada(s):")
        for acct in acct_list[:10]:
            status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW", 101: "CLOSED"}
            status = status_map.get(acct.get("account_status"), str(acct.get("account_status", "?")))
            print(f"       - {acct.get('name', '?')} ({acct.get('id')}) [{status}]")
        if len(acct_list) > 10:
            print(f"       ... e mais {len(acct_list) - 10}")
        if not acct_list:
            print("       Nenhuma conta acessivel para este token.")
            print("       No Business Manager, atribua a conta de anuncio a este System User.")
            return False
        return True
    except Exception as e:
        print(f"  [FALHOU] Erro ao listar contas: {e}")
        return False


def main():
    print("=" * 55)
    print("  Meta Ads - Install Wizard")
    print("=" * 55)

    env_file = load_env_file()
    if env_file:
        print(f"\n.env carregado: {env_file}")

    print("\n1. Dependencias:")
    py_ok = check_python()
    sdk_ok = check_sdk()
    req_ok = check_requests()

    print("\n2. Autenticacao:")
    token_ok = check_token()
    perms_ok = check_permissions() if token_ok else False
    account_ok = check_account()

    print("\n3. Conectividade:")
    accounts_ok = False
    if sdk_ok and token_ok:
        api_ok = check_api_connection()
        if api_ok and perms_ok:
            accounts_ok = check_ad_accounts()
        elif api_ok:
            print("  [PULOU] Listagem de contas (faltam permissoes de Ads)")
    else:
        print("  [PULOU] Resolva dependencias e token primeiro")
        api_ok = False

    # Summary
    print("\n" + "=" * 55)
    all_ok = py_ok and sdk_ok and req_ok and token_ok and perms_ok and account_ok
    if all_ok and api_ok and accounts_ok:
        print("  TUDO PRONTO! Skill meta-ads configurada.")
        print("  Use via Claude Code com linguagem natural")
        print("  ou invoque /meta-ads")
    elif py_ok and sdk_ok and req_ok and token_ok and api_ok:
        print("  QUASE LA! Token valido, mas ainda nao acessa contas de anuncio.")
        print("  Gere um token com ads_read/ads_management e vincule a conta ao Business.")
    else:
        print("  PENDENCIAS encontradas. Resolva os itens [FALHOU]")
        print("  e rode novamente: python3 scripts/setup.py")
    print("=" * 55)

    sys.exit(0 if (all_ok and api_ok and accounts_ok) else 1)


if __name__ == "__main__":
    main()
