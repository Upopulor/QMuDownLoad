import os
import shutil
import time

import requests
from requests.adapters import HTTPAdapter, Retry

from down import download_file
from get_list import merge_songs_info, get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link
from songs_proc import check_fail, verify_file, check_duplicate, export_files

# playlist_id = '3222851321'
playlist_idInput = input("请输入列表id：")
unlock_keyInput = input("请输入列表token：")
songTypeInput = input("请输入音质格式(sizeflac,size320,size128)参数：")
if(songTypeInput != 'sizeflac' and songTypeInput != 'size320' and songTypeInput != 'size128'):
    raise Exception('音质格式输入错误')
#1
playlist_id = '8544120534'
unlock_key = '7E61'  # 需通过flac.life官网免费获取解锁码
songType = 'size320'
#2
playlist_id = playlist_idInput
unlock_key = unlock_keyInput
songType = songTypeInput
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
cache_dir = parent_directory+'\\QMuDownLoadCache\\cache'
music_dir = parent_directory+'\\QMuDownLoadCache\\music'
export_dir = parent_directory+'\\QMuDownLoadCache\\'+playlist_id+'-export'
start_at_index = 0
paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))

if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

if not os.path.exists(music_dir):
    os.makedirs(music_dir)

session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

# 需通过flac.life官网免费获取解锁码
stat = verify_key(unlock_key)
print('key verify: ', stat)
if stat is False:
    raise Exception()

# 加载播放列表原始文件
playlist_raw = get_list(playlist_id)
store_json(paylist_raw_json_path, playlist_raw)
# playlist_raw = load_json(paylist_raw_json_path)

# 解析播放列表
songs_info = parse_list(playlist_raw,songTypeInput)

# 若旧歌单存在则合并
if os.path.exists(paylist_info_json_path):
    old_songs_info = load_json(paylist_info_json_path)
    merge_songs_info(songs_info, old_songs_info)

store_json(paylist_info_json_path, songs_info)
# songs_info = load_json(paylist_info_json_path)

# for song_info in songs_info:
#     print(song_info)
# print(songs_info[0])
print('歌曲数量:', len(songs_info))
lenStart = len(songs_info)
cuowu = 0
# reset_verify_failed_songs_info(songs_info)
# store_json(paylist_info_json_path, songs_info)

for i, song_info in enumerate(songs_info):
    if i>=lenStart-cuowu:
        break
    if i < start_at_index:
        print('{0}/{1}: JUMP'.format(i + 1, len(songs_info)))
        continue

    # 搜索歌曲
    print('{0}/{1}: SEARCH {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    kk = search(song_info)
    if(kk==5):
        songs_info.remove(song_info)
        print('歌曲数量-1,更新为:', len(songs_info))
        cuowu = cuowu+1

    # 获取歌曲链接
    print('{0}/{1}: GETLINK {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    get_download_link(song_info, music_dir, unlock_key)
    #print(song_info)

    print('{0}/{1}: DOWNLOAD {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
    download_file(song_info, music_dir)
    store_json(paylist_info_json_path, songs_info)

    print('{0}/{1}: SUCCESS {2}'.format(i + 1, len(songs_info), song_info))

#重命名
map_info_json_path = os.path.join(cache_dir, 'map.{0}.json'.format(playlist_id))
check_fail(songs_info)
for i in songs_info:
    verify = verify_file(music_dir, i)
    if not verify:
        print('VERIFY FAILED :{0}-{1}'.format(i['signernames'], i['songname']))
check_duplicate(songs_info)
export_files(export_dir, music_dir, songs_info, map_info_json_path)
shutil.rmtree(music_dir)