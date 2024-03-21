import os
import shutil
import time
import threading

from down import download_file
from get_list import merge_songs_info, get_list, parse_list
from json_oper import store_json, load_json
from sixyin import search, verify_key, get_download_link
from songs_proc import check_fail, verify_file, check_duplicate, export_files

def dones(playlist_raw,idxx,cache_dirr,music_dirr,export_dirr,playlist_idd,songTypeInput,unlock_key):
    start_at_index = 0
    cache_dircur = cache_dirr + '\\' + str(idxx)
    music_dircur = music_dirr + '\\' + str(idxx)
    playlist_idcur = playlist_idd + '-' + str(idxx)
    export_dircur = export_dirr +'\\'+str(idxx)
    if not os.path.exists(cache_dircur):
        os.makedirs(cache_dircur)
    if not os.path.exists(music_dircur):
        os.makedirs(music_dircur)
    paylist_raw_json_path = os.path.join(cache_dircur, 'playlist.{0}.raw.json'.format(playlist_idcur))
    paylist_info_json_path = os.path.join(cache_dircur, 'playlist.{0}.json'.format(playlist_idcur))
    store_json(paylist_raw_json_path, playlist_raw)
    songs_info = parse_list(playlist_raw, songTypeInput)
    store_json(paylist_info_json_path, songs_info)

    thread_name = threading.current_thread().name
    print(thread_name+'---'+'歌曲数量:', len(songs_info))
    lenStart = len(songs_info)
    cuowu = 0
    # reset_verify_failed_songs_info(songs_info)
    # store_json(paylist_info_json_path, songs_info)

    for i, song_info in enumerate(songs_info):
        if i >= lenStart - cuowu:
            break
        if i < start_at_index:
            print(thread_name+'---'+'{0}/{1}: JUMP'.format(i + 1, len(songs_info)))
            continue

        # 搜索歌曲
        print(thread_name+'---'+'{0}/{1}: SEARCH {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        kk = search(song_info)
        if (kk == 5):
            songs_info.remove(song_info)
            print(thread_name+'---'+'歌曲数量-1,更新为:', len(songs_info))
            cuowu = cuowu + 1
        #time.sleep(10)
        # 获取歌曲链接
        print(thread_name+'---'+'{0}/{1}: GETLINK {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        get_download_link(song_info, music_dircur, unlock_key)
        # print(song_info)

        print(thread_name+'---'+'{0}/{1}: DOWNLOAD {2}-{3}'.format(i + 1, len(songs_info), song_info['signernames'], song_info['songname']))
        download_file(song_info, music_dircur)
        store_json(paylist_info_json_path, songs_info)

        print(thread_name+'---'+'{0}/{1}: SUCCESS {2}'.format(i + 1, len(songs_info), song_info))

    # 重命名
    map_info_json_path = os.path.join(cache_dircur, 'map.{0}.json'.format(playlist_idcur))
    check_fail(songs_info)
    for i in songs_info:
        if 'download_done' in song_info:
            if song_info['download_done']==True:
                verify = verify_file(music_dircur, i)
                if not verify:
                    print(thread_name+'---'+'VERIFY FAILED :{0}-{1}'.format(i['signernames'], i['songname']))
    check_duplicate(songs_info)
    export_files(export_dircur, music_dircur, songs_info, map_info_json_path)
    shutil.rmtree(music_dircur)