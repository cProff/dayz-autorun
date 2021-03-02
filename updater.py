import requests
import os
import sys
updated_path = os.path.join(os.path.abspath("."), 'updated.exe')
replaceCMD = 'timeout 2 > NUL && del {0} && move {1} {0} && {0}'


def get_release(repo, r_tag):
    data = requests.get(f'https://api.github.com/repos/{repo}/releases/latest').json()
    if data['tag_name'] != r_tag:
        assets = requests.get(data['assets_url']).json()
        return assets[0]['browser_download_url']
    else:
        return False


def last_release_tag(repo):
    data = requests.get(f'https://api.github.com/repos/{repo}/releases/latest').json()
    return data['tag_name']


def have2update(repo, r_tag):
    if repo is None:
        return False
    exename = sys.argv[0]
    try:
        newVer = r_tag != last_release_tag(repo)
    except Exception:
        newVer = False
    return not exename.endswith('py') and newVer


def download_release(repo, r_tag):
    exename = sys.argv[0]
    if exename.endswith('py'):
        return False, None
    try:
        url = get_release(repo, r_tag)
        if url:
            data = requests.get(url)
            f = open(updated_path, 'wb')
            f.write(data.content)
            f.close()
            return True, replaceCMD.format(exename, updated_path)
    except Exception as e:
        print(e)
        return False, None
