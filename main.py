import os

import requests
from requests.adapters import HTTPAdapter, Retry


from sixyin import verify_key
from one import done
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
unlock_keyInput = 'F7B3' # 需通过flac.life官网免费获取解锁码
#1:sizeflac,2:size320,3:size128
songTypeInput = '3'
playlist_id = '8544120534'

parent_directory = os.path.dirname(os.getcwd())
cache_dir = parent_directory + '\\QMuDownLoadCache\\cache'
music_dir = parent_directory + '\\QMuDownLoadCache\\music'
export_dir = parent_directory + '\\QMuDownLoadCache\\' + playlist_id + '-export'
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
stat = verify_key(unlock_keyInput)
print('key verify: ', stat)
if stat is False:
    raise Exception()

if downTypeInput == '2':
    done()
elif downTypeInput == '1':
    dones(playlist_id,paylist_raw_json_path,paylist_info_json_path,songTypeInput,music_dir,cache_dir,export_dir,unlock_keyInput)



