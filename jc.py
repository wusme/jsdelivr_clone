import requests
import json
import os
import sys
import multiprocessing
from config import client_id, client_secret

if len(client_id) == 0 or len(client_secret) == 0:
    print('Please check config.py.')
    exit(0)
if len(sys.argv) != 3:
    print(r"""
    usage: python jc.py github-repo dir_name
    """)
    exit(0)
github_url = sys.argv[1]
dir_ = sys.argv[2]
github_key = '?client_id={}&client_secret={}'.format(client_id, client_secret)
github_api1 = 'https://api.github.com/repos/{}'.format(github_url[19:])
while True:
    try:
        response = requests.get(github_api1 + github_key)
        break
    except Exception:
        continue
repo_id = json.loads(response.text)['id']
github_api0 = 'https://api.github.com/repositories/{}/contents'.format(repo_id)
finall_result = []
def filetree(url=None, nexts=None, dirs=[]):
    github_api2 = 'https://api.github.com/repositories/{}/contents'.format(repo_id)
    if nexts:
        github_api2 = url + '/' + nexts
    while True:
        try:
            repo_contents = json.loads(requests.get(github_api2 + github_key).text)
            break
        except Exception:
            continue
    for file_content in repo_contents:
        if file_content['type'] != 'file':
            dirc = dirs.copy()
            dirc.append(file_content['name'])
            filetree(github_api2, file_content['name'], dirc)
        else:
            finall_result.append({'dir_list': dirs, 'file_name': file_content['name']})

def dirhandler1(dir_list):
    for dir_name in dir_list:
        if os.path.exists(dir_name):
            os.chdir(dir_name)
        else:
            os.mkdir(dir_name)
            os.chdir(dir_name)

def dirhandler2(dir_deep):
    for y in range(dir_deep):
        os.chdir('..')

def download(dir_list, file_name):
    url = 'https://cdn.jsdelivr.net/gh/{}'.format(github_url[19:])
    for dir_name in dir_list:
        url += '/' + dir_name
    url += '/' + file_name
    print(url)
    with open(file_name, 'wb+') as this:
        while True:
            try:
                response = requests.get(url).content
                break
            except Exception:
                continue
        this.write(response)

def main(result):
    dirhandler1(result['dir_list'])
    download(result['dir_list'], result['file_name'])
    dirhandler2(len(result['dir_list']))

if __name__ == '__main__':
    if os.path.exists(dir_):
        os.chdir(dir_)
    else:
        os.mkdir(dir_)
        os.chdir(dir_)
    print('Please wait...')
    filetree()
    pool = multiprocessing.Pool()
    for result in finall_result:
        pool.apply_async(main, args=(result,))
    pool.close()
    pool.join()
    print('Done!')
