import os
import requests

def main():
    api_key = os.getenv("ADG_API_TOKEN")
    default_server_url = os.getenv("DEFAULT_SERVER_URL")
    
    if not api_key:
        print("Error: ADG_API_TOKEN is not set")
        exit(1)
    
    if not default_server_url:
        print("Error: DEFAULT_SERVER_URL is not set")
        exit(1)

    url = f"{default_server_url}/github/get_api_keys" 
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "success":
            raise Exception(f"API returned error status: {data.get('message', 'No message provided')}")

        github_token = data.get("github_token")
        google_token = data.get("google_token")

        # Записываем в специальный файл GitHub Env, чтобы следующие шаги видели эти ключи
        env_file = os.getenv('GITHUB_ENV')
        print(github_token, google_token, env_file)
        if env_file:
            with open(env_file, "a") as f:
                f.write(f"MODELS_API_KEYS={github_token}\n")
                f.write(f"GOOGLE_EMBEDDING_API_KEY={google_token}\n")
                f.write(f"TYPE_OF_MODEL=git\n") 
            print("Keys successfully written to GITHUB_ENV")
        else:
            print(f"Local result: MODELS_API_KEYS={github_token}, GOOGLE_EMBEDDING_API_KEY={google_token}")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()