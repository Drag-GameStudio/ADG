import os
import requests
from autodocgenerator.manage import Manager


def main():
    api_key = os.getenv("ADG_API_TOKEN")
    default_server_url = os.getenv("DEFAULT_SERVER_URL")

    with open(".auto_doc_cache_file.json", "r", encoding="utf-8") as f:
        cache_data = f.read()

        result = requests.post(
            f"{default_server_url}/docs/{os.getenv('REPO_ID')}/push", 
        headers={"Authorization": f"Bearer {api_key}"},
        json={"content": cache_data}
    )
    result.raise_for_status()
    data = result.json()
    curr_doc_id = data["data"]["doc_id"]

    print(f"Received data: {data}")
    print(f"Current document ID: {curr_doc_id}")

    with open(".auto_doc_cache/output_doc.md", "r", encoding="utf-8") as f:
        output_doc_content = f.read()
    

    result = f"""
### 🚀 Powered by ADG System
The original version of this document offers a superior layout and faster navigation. 
**Check it out here:** [Full Documentation Interface](https://draggame-adg-frontend.hf.space/docs/{curr_doc_id})
---

{output_doc_content}
    """
    with open(".auto_doc_cache/output_doc.md", "w", encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    main()