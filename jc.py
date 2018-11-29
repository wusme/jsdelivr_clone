import requests
import json
import os
import sys
import multiprocessing

class Proxy_Util():
    """
    ------------------------
    代理工具类
    Proxy_Util
    Proxy_Util.get(): return proxy
    Proxy_Util.delete(proxy): delete proxy from proxy_pool
    ------------------------
    """
    @staticmethod
    def get():
        return requests.get('http://127.0.0.1:5010/get').text
    @staticmethod
    def delete(proxy):
        requests.get('http://127.0.0.1:5010/delete?proxy={proxy}'.format(proxy=proxy))

class Proxy_Requests():
    """
    ------------------------
    代理请求类
    Proxy_Requests
    Proxy_Requests.get(args): requests.get with proxy
    ------------------------
    """
    @staticmethod
    def get(url, content=False):
        while True:
            proxy = Proxy_Util.get()
            proxies = {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy,
            }
            try:
                response = requests.get(url + '?client_id=3089d9053557ad5b7fe3&client_secret=0e3959b4749534a0f36ea09da0a57ec01d40d8b1', proxies, timeout=10)
                if response.status_code == 200:
                    if content == True:
                        return response.content
                    return response.text
                else:
                    print('Status_code: ' + str(response.status_code))
                    continue
            except requests.exceptions.RequestException:
                Proxy_Util.delete(proxy)

if len(sys.argv) != 3:
    print(r"""
    usage: python jc.py github-repo dir_name
    """)
    exit()
github_url = sys.argv[1]
dir_ = sys.argv[2]
# github_url = 'https://github.com/9bie/bilibili-video-downloader'
# dir_ = 'testtest'
github_api1 = 'https://api.github.com/repos/{}'.format(github_url[19:])
response = Proxy_Requests.get(github_api1)
repo_id = json.loads(response)['id']
github_api0 = 'https://api.github.com/repositories/{}/contents'.format(repo_id)
finall_result = []
def filetree(url=None, nexts=None, dirs=[]):
    github_api2 = 'https://api.github.com/repositories/{}/contents'.format(repo_id)
    if nexts:
        github_api2 = url + '/' + nexts
    # time.sleep(2)
    repo_contents = json.loads(Proxy_Requests.get(github_api2))
    for file_content in repo_contents:
        if not isinstance(file_content, dict):
            print(file_content)
            exit(0)
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
        this.write(Proxy_Requests.get(url, True))

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
    filetree()
    pool = multiprocessing.Pool(8)
    for result in finall_result:
        # main(result)
        pool.apply_async(main, args=(result,))
    pool.close()
    pool.join()
    print('Done!')
