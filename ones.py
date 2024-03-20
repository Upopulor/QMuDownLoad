import os
import shutil
import time

from down import download_file
from get_list import merge_songs_info, get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link
from songs_proc import check_fail, verify_file, check_duplicate, export_files

def dones(playlist_id,paylist_raw_json_path,paylist_info_json_path,songTypeInput,music_dir,cache_dir,export_dir,unlock_key):
    start_at_index = 0
    # 加载播放列表原始文件
    playlist_raw = get_list(playlist_id)
    store_json(paylist_raw_json_path, playlist_raw)
    # playlist_raw = load_json(paylist_raw_json_path)

    # 解析播放列表
    songs_info = parse_list(playlist_raw, songTypeInput)

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
        if i >= lenStart - cuowu:
            break
        if i < start_at_index:
            print('{0}/{1}: JUMP'.format(i + 1, len(songs_info)))
            continue

        # 搜索歌曲
        print('{0}/{1}: SEARCH {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        kk = search(song_info)
        if (kk == 5):
            songs_info.remove(song_info)
            print('歌曲数量-1,更新为:', len(songs_info))
            cuowu = cuowu + 1

        # 获取歌曲链接
        print('{0}/{1}: GETLINK {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        get_download_link(song_info, music_dir, unlock_key)
        # print(song_info)

        print('{0}/{1}: DOWNLOAD {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        download_file(song_info, music_dir)
        store_json(paylist_info_json_path, songs_info)

        print('{0}/{1}: SUCCESS {2}'.format(i + 1, len(songs_info), song_info))

    # 重命名
    map_info_json_path = os.path.join(cache_dir, 'map.{0}.json'.format(playlist_id))
    check_fail(songs_info)
    for i in songs_info:
        verify = verify_file(music_dir, i)
        if not verify:
            print('VERIFY FAILED :{0}-{1}'.format(i['signernames'], i['songname']))
    check_duplicate(songs_info)
    export_files(export_dir, music_dir, songs_info, map_info_json_path)
    shutil.rmtree(music_dir)