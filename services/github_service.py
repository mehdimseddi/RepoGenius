import os
import streamlit as st
from github import Github
from github.GithubException import GithubException
from functools import lru_cache
import json

def fetch_repo_data(repo_url: str, github_token: str | None = None) -> dict:
    """Fetch repository data with error handling"""
    try:
        # Extract owner/repo from URL
        parts = repo_url.rstrip('/').split('/')[-2:]
        owner, repo_name = parts[0], parts[1]
        
        g = Github(github_token)
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        # Get key files (limit to important ones)
        important_files = []
        contents = repo.get_contents("")
        
        for content_file in contents:
            if content_file.type == "file" and any(content_file.name.endswith(ext) for ext in
                ['.py', '.ipynb', '.js', '.ts', '.java', '.go', '.rb', '.php', '.cs', '.c', '.cpp', '.h', '.hpp', 'requirements.txt', 'package.json']):
                if content_file.size < 100000:  # Skip large files
                    try:
                        file_content_raw = content_file.decoded_content.decode('utf-8')
                        
                        lang = None
                        if content_file.name.endswith('.ipynb'):
                            try:
                                notebook = json.loads(file_content_raw)
                                code_cells = [cell['source'] for cell in notebook['cells'] if cell['cell_type'] == 'code']
                                file_content = "\n".join(["".join(cell) for cell in code_cells])
                                lang = 'Python'
                            except (json.JSONDecodeError, KeyError):
                                file_content = file_content_raw
                        else:
                            file_content = file_content_raw

                        important_files.append({
                            "name": content_file.name,
                            "path": content_file.path,
                            "content": file_content[:4000],
                            "language": lang
                        })
                    except Exception:
                        # Ignore files that can't be decoded or processed
                        pass
        
        repo_lang = repo.language
        if important_files:
            # Determine language from the first file that has one specified
            for f in important_files:
                if f.get('language'):
                    repo_lang = f['language']
                    break

        # Add language to files that don't have it
        for f in important_files:
            if not f.get('language'):
                f['language'] = repo.language

        return {
            "name": repo.name,
            "description": repo.description or "No description available",
            "language": repo_lang,
            "files": important_files[:5],
            "owner": owner
        }
    except GithubException as e:
        if e.status == 401:
            st.error("GitHub API Error: Invalid or expired token. Please check your token in the sidebar.")
        elif e.status == 403:
            st.error("GitHub API Error: Rate limit exceeded. Please provide a token or wait for the limit to reset.")
        else:
            st.error(f"GitHub API Error: {e.data.get('message', 'An unknown error occurred')}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

@lru_cache(maxsize=32)
def fetch_repo_data_cached(repo_url: str, github_token: str | None = None) -> dict:
    """Cached version of repo fetcher"""
    return fetch_repo_data(repo_url, github_token=github_token)
