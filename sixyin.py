import time

import requests

from down import verify_file

search_sleep = 1
getlink_sleep = 1

# sixyin_proxies = {
#     'http': 'http://localhost:7890',
#     'https': 'http://localhost:7890',
# }

sixyin_proxies = {
    'http': '',
    'https': '',
}

def search(song_info):
    if 'sixyin_song_id' in song_info.keys():
        return

    song_search_kw1 = '{0} {1} {2}'.format(song_info['songname'], song_info['signernames'].replace("|", " "),
                                          song_info['albumname'])
    song_search_kw2 = '{0} {1} {2}'.format(song_info['songname'], song_info['signernames'].split("|")[0], song_info['albumname'])
    song_search_kw3 = '{0} {1}'.format(song_info['songname'], song_info['signernames'].replace("|", " "))
    song_search_kw4 = '{0} {1}'.format(song_info['songname'], song_info['albumname'])
    song_search_kw5 = '{0}'.format(song_info['songname'])

    kk = 0;
    for word in [song_search_kw1,song_search_kw2,song_search_kw3,song_search_kw4,song_search_kw5]:
        url = "https://api.itooi.cn/tencent/search"
        headers = {}
        params = {"type": "song",
                  # "keyword": "听见下雨的声音 魏如昀 听见下雨的声音 电影原声带"}
                  "keyword": word,
                  "format": "1",
                  "page": "0",
                  "pageSize": "20"}

        time.sleep(search_sleep)
        response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
        result = response.json()
        kk = kk+1
        if len(result['data']['list']) == 0 and kk == 5:
            return kk
        elif len(result['data']['list']) == 0:
            continue
        else:
            break;

    song_id = result['data']['list'][0]['id']
    song_name = result['data']['list'][0]['name']
    song_singer = str.join('|', [signer for signer in result['data']['list'][0]['singers']])
    song_album = result['data']['list'][0]['albumName']

    song_info['sixyin_song_id'] = song_id
    song_info['sixyin_song_name'] = song_name
    song_info['sixyin_song_singer'] = song_singer
    song_info['sixyin_song_album'] = song_album

def search_one(song_info,length):
    if 'sixyin_song_id' in song_info.keys():
        return

    kk = 0;
    if length==3:
        song_search_kw1 = '{0} {1} {2}'.format(song_info['songname'], song_info['signernames'].replace("|", " "),
                                              song_info['albumname'])
        song_search_kw2 = '{0} {1} {2}'.format(song_info['songname'], song_info['signernames'].split("|")[0], song_info['albumname'])
        song_search_kw3 = '{0} {1}'.format(song_info['songname'], song_info['signernames'].replace("|", " "))
        song_search_kw4 = '{0} {1}'.format(song_info['songname'], song_info['albumname'])
        song_search_kw5 = '{0}'.format(song_info['songname'])
        for word in [song_search_kw1, song_search_kw2, song_search_kw3, song_search_kw4, song_search_kw5]:
            url = "https://api.itooi.cn/tencent/search"
            headers = {}
            params = {"type": "song",
                      # "keyword": "听见下雨的声音 魏如昀 听见下雨的声音 电影原声带"}
                      "keyword": word,
                      "format": "1",
                      "page": "0",
                      "pageSize": "20"}

            time.sleep(search_sleep)
            response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
            result = response.json()
            kk = kk + 1
            if len(result['data']['list']) == 0 and kk == 5:
                return kk
            elif len(result['data']['list']) == 0:
                continue
            else:
                break;
    elif length==2:
        song_search_kw3 = '{0} {1}'.format(song_info['songname'], song_info['signernames'].replace("|", " "))
        song_search_kw5 = '{0}'.format(song_info['songname'])
        for word in [song_search_kw3, song_search_kw5]:
            url = "https://api.itooi.cn/tencent/search"
            headers = {}
            params = {"type": "song",
                      # "keyword": "听见下雨的声音 魏如昀 听见下雨的声音 电影原声带"}
                      "keyword": word,
                      "format": "1",
                      "page": "0",
                      "pageSize": "20"}

            time.sleep(search_sleep)
            response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
            result = response.json()
            kk = kk + 1
            if len(result['data']['list']) == 0 and kk == 2:
                return kk
            elif len(result['data']['list']) == 0:
                continue
            else:
                break;
    else:
        song_search_kw5 = '{0}'.format(song_info['songname'])
        for word in [song_search_kw5]:
            url = "https://api.itooi.cn/tencent/search"
            headers = {}
            params = {"type": "song",
                      # "keyword": "听见下雨的声音 魏如昀 听见下雨的声音 电影原声带"}
                      "keyword": word,
                      "format": "1",
                      "page": "0",
                      "pageSize": "20"}

            time.sleep(search_sleep)
            response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
            result = response.json()
            kk = kk + 1
            if len(result['data']['list']) == 0 :
                return kk
            else:
                break;

    song_id = result['data']['list'][0]['id']
    song_name = result['data']['list'][0]['name']
    song_singer = str.join('|', [signer for signer in result['data']['list'][0]['singers']])
    song_album = result['data']['list'][0]['albumName']

    song_info['sixyin_song_id'] = song_id
    song_info['sixyin_song_name'] = song_name
    song_info['sixyin_song_singer'] = song_singer
    song_info['sixyin_song_album'] = song_album


def verify_key(key):
    url = "https://api.itooi.cn/unlock/" + key
    headers = {}
    params = {}

    response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
    result = response.json()
    # print(result['code'])
    # print(result['msg'])
    return True if result['code'] == 200 else False


def get_download_link(song_info, music_dir, key):
    if 'sixyin_song_id' not in song_info.keys():
        return None

    verify = verify_file(music_dir, song_info)
    if verify:
        return song_info['download_link']

    url = "https://api.itooi.cn/tencent/url"
    headers = {'Unlockcode': key}
    params = {'id': song_info['sixyin_song_id'],
              'quality': song_info['songtype'],
              'isRedirect': '0'}  # 是否直接下载

    time.sleep(getlink_sleep)
    response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
    result = response.json()

    if result['code'] == 400:
        return None
    else:
        song_info['download_link'] = result['data'][0]

        return song_info['download_link']


def reset_verify_failed_songs_info(songs_info):
    for song_info in songs_info:
        if ('download_verify' in song_info.keys() and not song_info['download_verify']) \
                or ('download_done' in song_info.keys() and not song_info['download_done']):
            if 'sixyin_song_id' in song_info.keys():
                del song_info['sixyin_song_id']
            if 'sixyin_song_name' in song_info.keys():
                del song_info['sixyin_song_name']
            if 'sixyin_song_singer' in song_info.keys():
                del song_info['sixyin_song_singer']
            if 'sixyin_song_album' in song_info.keys():
                del song_info['sixyin_song_album']
            if 'download_link' in song_info.keys():
                del song_info['download_link']
            if 'download_path' in song_info.keys():
                del song_info['download_path']
            song_info['download_done'] = False
            if 'download_verify' in song_info.keys():
                del song_info['download_verify']

def get_download_link_one(song_info, music_dir, key,songTypeInput):
    if 'sixyin_song_id' not in song_info.keys():
        return None

    verify = verify_file(music_dir, song_info)
    if verify:
        return song_info['download_link']

    if songTypeInput != '':
        if songTypeInput == '1':
            song_info['songtype'] = 'flac'
        elif songTypeInput == '2':
            song_info['songtype'] = '320'
        elif songTypeInput == '3':
            song_info['songtype'] = '128'
        else:
            print('输入下载格式错误,将按照128默认格式下载')
            song_info['songtype'] = '128'

    url = "https://api.itooi.cn/tencent/url"
    headers = {'Unlockcode': key}
    params = {'id': song_info['sixyin_song_id'],
              'quality': song_info['songtype'],
              'isRedirect': '0'}  # 是否直接下载
    time.sleep(getlink_sleep)
    response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
    result = response.json()

    if result['code'] == 400:
        songTypeInputs = ['flac','320','128']
        for tp in songTypeInputs:
            params = {'id': song_info['sixyin_song_id'],
                      'quality': tp,
                      'isRedirect': '0'}  # 是否直接下载
            time.sleep(getlink_sleep)
            response = requests.get(url, headers=headers, params=params, proxies=sixyin_proxies)
            result = response.json()
            if result['code'] == 400:
                continue
            else:
                print('未找到指定格式音乐，将按照'+tp+'格式下载')
                song_info['download_link'] = result['data'][0]
                return song_info['download_link']
        return None
    else:
        song_info['download_link'] = result['data'][0]
        return song_info['download_link']
