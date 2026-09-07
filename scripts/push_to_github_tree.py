import os
import json
import base64
import urllib.request
from pathlib import Path

# Load from env or fallback
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN")
REPO_OWNER = "Shalom165"
REPO_NAME = "COEPROJECTEE"
BRANCH = "main"
BASE_DIR = Path("d:/AI Immersion")

def github_api(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/{endpoint}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Tree-Uploader"
    }
    encoded_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode('utf-8')}")
        return None

def main():
    print(f"Starting Batch Tree Commit to https://github.com/{REPO_OWNER}/{REPO_NAME}...")

    # 1. Get latest commit SHA on main branch
    ref_data = github_api(f"git/ref/heads/{BRANCH}")
    if not ref_data:
        print("Failed to get branch ref.")
        return
    
    commit_sha = ref_data["object"]["sha"]
    print(f"Latest commit SHA: {commit_sha}")

    # 2. Get base tree SHA
    commit_data = github_api(f"git/commits/{commit_sha}")
    tree_sha = commit_data["tree"]["sha"]
    print(f"Base tree SHA: {tree_sha}")

    # 3. Create blobs for all project files
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache", "scratch"}
    tree_nodes = []

    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if f.endswith(".db") or f.endswith(".sqlite") or f.endswith(".pyc"):
                continue
            full_p = Path(root) / f
            rel_p = full_p.relative_to(BASE_DIR).as_posix()
            
            try:
                with open(full_p, "rb") as file_handle:
                    raw_bytes = file_handle.read()
                    # Sanitize token from file if present to avoid secret scanning trigger
                    if b"YOUR_GITHUB_TOKEN" in raw_bytes:
                        raw_bytes = raw_bytes.replace(b"YOUR_GITHUB_TOKEN", b"YOUR_GITHUB_TOKEN")
                    b64_content = base64.b64encode(raw_bytes).decode("utf-8")
                
                # Create blob
                blob_data = github_api("git/blobs", method="POST", data={
                    "content": b64_content,
                    "encoding": "base64"
                })
                
                if blob_data and "sha" in blob_data:
                    tree_nodes.append({
                        "path": rel_p,
                        "mode": "100644",
                        "type": "blob",
                        "sha": blob_data["sha"]
                    })
                    print(f"  [BLOB] {rel_p}")
            except Exception as e:
                print(f"  [ERROR] {rel_p}: {e}")

    # 4. Create new tree
    print(f"Creating new git tree with {len(tree_nodes)} items...")
    new_tree = github_api("git/trees", method="POST", data={
        "base_tree": tree_sha,
        "tree": tree_nodes
    })
    
    if not new_tree or "sha" not in new_tree:
        print("Failed to create new tree.")
        return

    new_tree_sha = new_tree["sha"]
    print(f"New tree SHA: {new_tree_sha}")

    # 5. Create new commit
    new_commit = github_api("git/commits", method="POST", data={
        "message": "Add Evidence-Ranked Enterprise Search Tool codebase and upload script",
        "tree": new_tree_sha,
        "parents": [commit_sha]
    })
    
    if not new_commit or "sha" not in new_commit:
        print("Failed to create commit.")
        return

    new_commit_sha = new_commit["sha"]
    print(f"New commit SHA: {new_commit_sha}")

    # 6. Update reference
    ref_update = github_api(f"git/refs/heads/{BRANCH}", method="PATCH", data={
        "sha": new_commit_sha,
        "force": True
    })

    if ref_update:
        print(f"\nSUCCESS! Entire project uploaded to https://github.com/{REPO_OWNER}/{REPO_NAME}")
    else:
        print("\nFailed to update branch reference.")

if __name__ == "__main__":
    main()
