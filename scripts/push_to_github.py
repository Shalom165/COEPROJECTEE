import os
import json
import base64
import urllib.request
from pathlib import Path

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REPO_OWNER = "Shalom165"
REPO_NAME = "COEPROJECTEE"
BRANCH = "main"
BASE_DIR = Path("d:/AI Immersion")

def github_api_request(url, method="GET", data=None):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-GitHub-Uploader"
    }
    encoded_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} for {url}: {error_body}")
        return None

def get_file_sha(path_in_repo):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path_in_repo}?ref={BRANCH}"
    res = github_api_request(url, method="GET")
    if res and isinstance(res, dict) and "sha" in res:
        return res["sha"]
    return None

def upload_file_to_github(local_file_path):
    rel_path = local_file_path.relative_to(BASE_DIR).as_posix()
    
    # Read file content
    try:
        with open(local_file_path, "rb") as f:
            content_bytes = f.read()
    except Exception as e:
        print(f"Skipping {rel_path} (Read error: {e})")
        return False

    # Base64 encode content
    b64_content = base64.b64encode(content_bytes).decode("utf-8")
    
    # Check if file already exists in repo to obtain its sha
    sha = get_file_sha(rel_path)
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}"
    payload = {
        "message": f"Upload {rel_path} via automated agent pipeline",
        "content": b64_content,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha
        
    res = github_api_request(url, method="PUT", data=payload)
    if res and "content" in res:
        print(f"  [SUCCESS] Uploaded {rel_path}")
        return True
    else:
        print(f"  [FAILED] Uploading {rel_path}")
        return False

def main():
    print(f"Uploading project to https://github.com/{REPO_OWNER}/{REPO_NAME}...")
    
    # List of files to upload
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "scratch"}
    files_to_upload = []

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            # Skip large sqlite database binaries if present
            if f.endswith(".db") or f.endswith(".sqlite") or f.endswith(".pyc"):
                continue
            full_p = Path(root) / f
            files_to_upload.append(full_p)

    print(f"Found {len(files_to_upload)} files to upload to GitHub repository...")
    
    success_count = 0
    for file_path in files_to_upload:
        if upload_file_to_github(file_path):
            success_count += 1
            
    print(f"\nUpload complete! Successfully uploaded {success_count}/{len(files_to_upload)} files to https://github.com/{REPO_OWNER}/{REPO_NAME}")

if __name__ == "__main__":
    main()
