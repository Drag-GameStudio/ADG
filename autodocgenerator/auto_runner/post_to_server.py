import os
import requests

def main():
    api_key = os.getenv("ADG_API_TOKEN")
    default_server_url = os.getenv("DEFAULT_SERVER_URL")

    with open(".auto_doc_cache_file.json", "r", encoding="utf-8") as f:
        cache_data = f.read()

        result = requests.post(
            f"{default_server_url}/docs/{os.getenv('REPO_ID')}/push", 
        headers={"Authorization": f"Bearer {api_key}"},
        data={"content": cache_data}
    )
    result.raise_for_status()
    data = result.json()
    print(f"Received data: {data}")

if __name__ == "__main__":
    main()