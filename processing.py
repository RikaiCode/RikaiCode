import streamlit as st
import os
import io
import zipfile
import requests
import time
import gc
import urllib.parse
from datetime import datetime, timezone

from config import SKIP_EXTENSIONS

def process_uploaded_files(uploaded_files):
    files_dict = {}
    for f in uploaded_files:
        try:
      
            ext = os.path.splitext(f.name)[1].lower()
            if ext in SKIP_EXTENSIONS:
                files_dict[f.name] = ""
            else:
                content = f.read().decode('utf-8')
                files_dict[f.name] = content
     
            del content
        except: pass
    gc.collect() 
    return files_dict

def process_zip_file(zip_file):
    files_dict = {}
    with zipfile.ZipFile(zip_file) as z:
        for filename in z.namelist():
            if filename.endswith('/'): continue
            
            ext = os.path.splitext(filename)[1].lower()
            clean_name = filename.split('/', 1)[-1] if '/' in filename else filename
            
            if ext in SKIP_EXTENSIONS:
                files_dict[clean_name] = "" 
                continue

            try:
                with z.open(filename) as f:
                    content = f.read().decode('utf-8')
                    files_dict[clean_name] = content
                    del content 
            except: pass
    gc.collect() 
    return files_dict

def process_github_url(url):
    files_dict = {}
    repo_meta = {}
    pr_stats = {}
    
    if url.endswith('.git'): url = url[:-4]
    
    try:
        parts = url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
    except:
        st.error("Invalid GitHub URL format.")
        return {}, {}, {}

    api_base = f"https://api.github.com/repos/{owner}/{repo}"
    
    progress_bar = st.progress(0, text="Initializing...")
    
    try:
        progress_bar.progress(10, text="📡 Fetching GitHub metadata...")
        meta_r = requests.get(api_base)
        if meta_r.status_code == 200:
            data = meta_r.json()
            repo_meta['stars'] = data.get('stargazers_count', 0)
            repo_meta['forks'] = data.get('forks_count', 0)
            repo_meta['watchers'] = data.get('subscribers_count', data.get('watchers_count', 0)) 
            repo_meta['open_issues'] = data.get('open_issues_count', 0)
            repo_meta['language'] = data.get('language', 'Unknown')
            repo_meta['archived'] = data.get('archived', False)
            repo_meta['pushed_at'] = data.get('pushed_at', None)
            repo_meta['created_at'] = data.get('created_at', None)
            

        if repo_meta['created_at']:
           
            created = datetime.strptime(repo_meta['created_at'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - created).days
            repo_meta['age_years'] = round(age_days / 365, 1)
        else:
            progress_bar.empty()
            st.error(f"GitHub API Error: {meta_r.status_code}")
            return {}, {}, {}

        
        progress_bar.progress(15, text="📡 Analyzing Pull Requests...")
        try:
            r_open = requests.get(f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:open")
            open_prs = r_open.json().get('total_count', 0) if r_open.status_code == 200 else 0
            
            r_merged = requests.get(f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+is:merged")
            merged_prs = r_merged.json().get('total_count', 0) if r_merged.status_code == 200 else 0
            
            r_closed = requests.get(f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:pr+state:closed")
            closed_total = r_closed.json().get('total_count', 0) if r_closed.status_code == 200 else 0
            
            pr_stats['open'] = open_prs
            pr_stats['merged'] = merged_prs
            pr_stats['closed_rejected'] = max(0, closed_total - merged_prs)
            pr_stats['total_prs'] = open_prs + closed_total
            
            if closed_total > 0:
                pr_stats['merge_rate'] = merged_prs / closed_total
            else:
                pr_stats['merge_rate'] = 0
                
        except Exception as e:
            st.warning(f"Could not fetch detailed PR stats: {e}")

    
        progress_bar.progress(20, text="📡 Fetching commit history...")
        commits_r = requests.get(f"{api_base}/commits?per_page=100")
        commit_dates = []

        repo_meta['commit_datetimes'] = [] 
        
        if commits_r.status_code == 200:
            for c in commits_r.json():
                try:
                    date_str = c['commit']['author']['date']
            
                    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                    repo_meta['commit_datetimes'].append(dt)
                    
                    d = dt.date()
                    commit_dates.append(d)
                except: pass
            repo_meta['commit_dates'] = commit_dates


        archive_url_main = f"{api_base}/zipball/main"
        archive_url_master = f"{api_base}/zipball/master"
        
        progress_bar.progress(30, text="🔍 Checking Main branch...")
        r = requests.get(archive_url_main, stream=True)
        
        if r.status_code == 404:
            progress_bar.progress(40, text="🔍 Main not found. Checking Master...")
            r = requests.get(archive_url_master, stream=True)
        
        if r.status_code != 200:
            progress_bar.empty()
            st.error("Could not fetch repository content.")
            return {}, {}, {}

        total_size = int(r.headers.get('content-length', 0))
        chunk_data = []
        downloaded = 0
        
        progress_bar.progress(50, text=f"⬇️ Downloading ({int(total_size/1024)} KB)...")
        
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                chunk_data.append(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = 50 + int((downloaded / total_size) * 30)
                    progress_bar.progress(pct, text=f"⬇️ Downloading... {int(downloaded/1024)}/{int(total_size/1024)} KB")
        
        progress_bar.progress(80, text="📦 Decompressing...")
        zip_data = io.BytesIO(b''.join(chunk_data))
        
        with zipfile.ZipFile(zip_data) as z:
            file_list = z.namelist()
            total_files = len(file_list)
            processed_count = 0
            
            for filename in file_list:
                if filename.endswith('/'): continue
                
              
                ext = os.path.splitext(filename)[1].lower()
                clean_name = filename.split('/', 1)[-1] if '/' in filename else filename

                if ext in SKIP_EXTENSIONS:
                    files_dict[clean_name] = "" 
                else:
                    try:
                        with z.open(filename) as f:
                            content = f.read().decode('utf-8')
                            files_dict[clean_name] = content
                            del content 
                    except: pass
                
                processed_count += 1
                if total_files > 0:
                    pct = 80 + int((processed_count / total_files) * 20)
                    progress_bar.progress(pct, text=f"⚙️ Processing {processed_count}/{total_files}")
        
        progress_bar.progress(100, text="✔️ Done!")
        time.sleep(0.5)
        progress_bar.empty()
        
        
        del chunk_data
        del zip_data
        gc.collect()
        
    except Exception as e:
        progress_bar.empty()
        st.error("Please make sure the source url is correct.")
        
    return files_dict, repo_meta, pr_stats

def process_gitlab_url(url):
    files_dict = {}
    repo_meta = {}
    pr_stats = {}
    
    if url.endswith('.git'): url = url[:-4]
    
    try:
       
        parts = url.rstrip('/').split('/')
        if 'gitlab.com' not in parts:
            st.error("Invalid GitLab URL. Must contain gitlab.com")
            return {}, {}, {}
            
        idx = parts.index('gitlab.com')
        path_parts = parts[idx+1:]
        if len(path_parts) < 1:
             st.error("Invalid GitLab URL: No project path found.")
             return {}, {}, {}
        
        path = '/'.join(path_parts)
        
    except Exception as e:
        st.error(f"Invalid GitLab URL format: {e}")
        return {}, {}, {}


    encoded_path = urllib.parse.quote_plus(path)
    api_base = f"https://gitlab.com/api/v4/projects/{encoded_path}"
    
    progress_bar = st.progress(0, text="Initializing GitLab Fetch...")
    
    try:
        progress_bar.progress(10, text="📡 Fetching GitLab metadata...")
        meta_r = requests.get(api_base)
        
        if meta_r.status_code == 200:
            data = meta_r.json()
            repo_meta['stars'] = data.get('star_count', 0)
            repo_meta['forks'] = data.get('forks_count', 0)
            repo_meta['watchers'] = data.get('star_count', 0) 
            repo_meta['open_issues'] = data.get('open_issues_count', 0)
            repo_meta['archived'] = data.get('archived', False)
            
       
            repo_meta['language'] = 'N/A'
            try:
                lang_r = requests.get(f"{api_base}/languages")
                if lang_r.status_code == 200:
                    langs = lang_r.json()
                    if langs:
             
                        main_lang = max(langs, key=langs.get)
                        repo_meta['language'] = main_lang
            except: pass
            
         
            repo_meta['pushed_at'] = data.get('last_activity_at')
            repo_meta['created_at'] = data.get('created_at')
            
            if repo_meta['created_at']:
              
                created_str = repo_meta['created_at'].replace('Z', '+00:00')
                created = datetime.fromisoformat(created_str)
                age_days = (datetime.now(created.tzinfo) - created).days
                repo_meta['age_years'] = round(age_days / 365, 1)
                
            default_branch = data.get('default_branch', 'main')
        else:
            progress_bar.empty()
            st.error(f"GitLab API Error: {meta_r.status_code} - Project might be private or URL incorrect.")
            return {}, {}, {}

      
        progress_bar.progress(20, text="📡 Fetching commit history...")
        commits_r = requests.get(f"{api_base}/repository/commits?per_page=100")
        commit_dates = []
        repo_meta['commit_datetimes'] = []
        
        if commits_r.status_code == 200:
            for c in commits_r.json():
                try:
                    date_str = c['created_at']
    
                    d = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
                    commit_dates.append(d)
                    
                    
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    repo_meta['commit_datetimes'].append(dt)
                except: pass
            repo_meta['commit_dates'] = commit_dates
            
  
        progress_bar.progress(30, text="📡 Analyzing Merge Requests...")
        try:
  
            def get_total_mr_count(state):
        
                r = requests.get(f"{api_base}/merge_requests?state={state}&per_page=1")
                if r.status_code == 200:
                   
                    total = r.headers.get('X-Total')
                    if total:
                        return int(total)
                    
                    
                    count = 0
                    page = 1
                    while True:
                        r_page = requests.get(f"{api_base}/merge_requests?state={state}&per_page=100&page={page}")
                        if r_page.status_code != 200: break
                        items = r_page.json()
                        count += len(items)
                        if len(items) < 100: break
                        page += 1
                    return count
                return 0

            open_count = get_total_mr_count('opened')
            merged_count = get_total_mr_count('merged')
            closed_count = get_total_mr_count('closed')
            
            pr_stats['open'] = open_count
            pr_stats['merged'] = merged_count
            pr_stats['closed_rejected'] = closed_count
            
            total_finalized = merged_count + closed_count
            if total_finalized > 0:
                pr_stats['merge_rate'] = merged_count / total_finalized
            else:
                pr_stats['merge_rate'] = 0
            
            pr_stats['total_prs'] = open_count + merged_count + closed_count
                
        except Exception as e:
            st.warning(f"Could not fetch MR stats: {e}")


        progress_bar.progress(40, text="⬇️ Downloading archive...")
        archive_url = f"{api_base}/repository/archive.zip?sha={default_branch}"
        
        r = requests.get(archive_url, stream=True)
        if r.status_code != 200:

            archive_url = f"{api_base}/repository/archive.zip?sha=master"
            r = requests.get(archive_url, stream=True)
            
        if r.status_code != 200:
            progress_bar.empty()
            st.error("Could not fetch repository content. Check if project is public.")
            return {}, {}, {}

        total_size = int(r.headers.get('content-length', 0))
        chunk_data = []
        downloaded = 0
        
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                chunk_data.append(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = 50 + int((downloaded / total_size) * 30)
                    progress_bar.progress(pct, text=f"⬇️ Downloading... {int(downloaded/1024)}/{int(total_size/1024)} KB")
        
        progress_bar.progress(80, text="📦 Decompressing...")
        zip_data = io.BytesIO(b''.join(chunk_data))
        
        with zipfile.ZipFile(zip_data) as z:
            file_list = z.namelist()
            total_files = len(file_list)
            processed_count = 0
            
            for filename in file_list:
                if filename.endswith('/'): continue
                
                ext = os.path.splitext(filename)[1].lower()
               
                clean_name = filename.split('/', 1)[-1] if '/' in filename else filename

                if ext in SKIP_EXTENSIONS:
                    files_dict[clean_name] = "" 
                else:
                    try:
                        with z.open(filename) as f:
                            content = f.read().decode('utf-8')
                            files_dict[clean_name] = content
                            del content 
                    except: pass
                
                processed_count += 1
                if total_files > 0:
                    pct = 80 + int((processed_count / total_files) * 20)
                    progress_bar.progress(pct, text=f"⚙️ Processing {processed_count}/{total_files}")
        
        progress_bar.progress(100, text="✔️ Done!")
        time.sleep(0.5)
        progress_bar.empty()
        
        del chunk_data
        del zip_data
        gc.collect()
        
    except Exception as e:
        progress_bar.empty()
        st.error("Please make sure the source url is correct.")
        
    return files_dict, repo_meta, pr_stats