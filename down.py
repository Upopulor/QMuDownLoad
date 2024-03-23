import os

import requests
from tqdm import tqdm
import threading

download_proxies = {
    'http': '',
    'https': '',
}


def extract_filename(url):
    return os.path.basename(url.split('?')[0])


def download_file(songs_info, download_dir):
    if 'download_link' not in songs_info.keys():
        songs_info['download_done'] = False
        return False

    # 若文件存在且校验通过则跳过下载
    if verify_file(download_dir, songs_info):
        print('存在歌曲，已跳过下载')
        return True

    filename = songs_info['strMediaMid']
    r = requests.get(songs_info['download_link'], proxies=download_proxies, stream=True)
    totalSize = int(r.headers.get('content-length', 0))
    thread_name = threading.current_thread().name
    progressBar = tqdm(total=totalSize, unit='B', unit_scale=True, desc=songs_info['songname'])
    song_path = os.path.join(download_dir, filename)
    with open(song_path, 'wb') as f:
        for chunk in r.iter_content(3000):
            if chunk:
                f.write(chunk)
                progressBar.update(len(chunk))

    f.close()
    progressBar.close()

    songs_info['download_path'] = filename
    songs_info['download_done'] = True

    verify = verify_file(download_dir, songs_info)
    songs_info['download_verify'] = verify
    return verify


def verify_file(down_dir, songs_info):
    if 'download_path' not in songs_info.keys():
        return False
    song_path = os.path.join(down_dir, songs_info['download_path'])
    if not os.path.exists(song_path):
        return False
    size = os.path.getsize(song_path)
    if size != songs_info['filesize']:
        return False
    else:
        return True

def download_file_one(song_info, download_dir):
    if 'download_link' not in song_info.keys():
        song_info['download_done'] = False
        return False

    # 若文件存在且校验通过则跳过下载
    if verify_file(download_dir, song_info):
        print('存在歌曲，已跳过下载')
        return True

    fileext = ('.flac' if song_info['songtype'] == 'flac' else '.mp3')
    filename = song_info['songname']+'-'+song_info['sixyin_song_singer']+fileext
    r = requests.get(song_info['download_link'], proxies=download_proxies,stream=True)
    totalSize = int(r.headers.get('content-length',0))
    progressBar = tqdm(total=totalSize,unit='B',unit_scale=True)
    song_path = os.path.join(download_dir, filename)
    with open(song_path, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
                progressBar.update(len(chunk))

    f.close()
    progressBar.close()

    song_info['download_path'] = filename
    song_info['download_done'] = True

    #verify = verify_file(download_dir, song_info)
    #song_info['download_verify'] = verify
    return
