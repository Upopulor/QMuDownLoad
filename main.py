import os

import requests
from requests.adapters import HTTPAdapter, Retry
from get_list import  get_list,list_split
from sixyin import verify_key
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from ones import dones

# 1输入
# downTypeInput = input("请输入下载方式(1:列表下载 2:单曲下载)：")
# if downTypeInput == '2':
#     songInput = input("请输入歌曲信息(歌曲名-歌手-专辑)：")
#     parent_directory = os.path.dirname(os.getcwd())
#     cache_dir = parent_directory + '\\QMuDownLoadCache\\cache'
#     music_dir = parent_directory + '\\QMuDownLoadCache\\music'
#     export_dir = parent_directory + '\\QMuDownLoadCache\\' + songInput + '-export'
#     paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(songInput))
#     paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(songInput))
# else:
#     playlist_idInput = input("请输入列表id：")
#     playlist_id = playlist_idInput
#     parent_directory = os.path.dirname(os.getcwd())
#     cache_dir = parent_directory + '\\QMuDownLoadCache\\cache'
#     music_dir = parent_directory + '\\QMuDownLoadCache\\music'
#     export_dir = parent_directory + '\\QMuDownLoadCache\\' + playlist_id + '-export'
#     paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
#     paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))

#本地运行
downTypeInput = '1'
unlock_keyInput = '0076' # 需通过flac.life官网免费获取解锁码
#1:sizeflac,2:size320,3:size128
songTypeInput = '2'
playlist_id = '9109342223'

parent_directory = os.path.dirname(os.getcwd())
cache_dir = parent_directory + '\\QMuDownLoadCache2\\cache'
music_dir = parent_directory + '\\QMuDownLoadCache2\\music'
export_dir = parent_directory + '\\QMuDownLoadCache2\\' + playlist_id + '-export'
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

#需通过flac.life官网免费获取解锁码
stat = verify_key(unlock_keyInput)
print('key verify: ', stat)
if stat is False:
    raise Exception()



playlist_raw = get_list(playlist_id)
cur = playlist_raw['data']['cdlist'][0]['songlist']
playlist_rawsplit = list_split(playlist_raw['data']['cdlist'][0]['songlist'],5)

ss =len(playlist_rawsplit)
idxx = 1
all_task = []
with ThreadPoolExecutor(max_workers=10) as pool:
    for cnt in playlist_rawsplit:
        all_task.append(pool.submit(dones,cnt,idxx,cache_dir,music_dir,export_dir,playlist_id,songTypeInput,unlock_keyInput))
        idxx = idxx + 1

    # 主线程等待所有子线程完成
    wait(all_task, return_when=ALL_COMPLETED)
    print("----complete-----")




