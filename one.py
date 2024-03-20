

def done():
    # 搜索歌曲
    songInputs = songInput.split("-");
    song_info_one = {'songname': songInputs[0], 'signernames': songInputs[1], 'albumname': songInputs[2]}


    song_info_one['songtype'] = '128'
    print('SEARCH --' + songInput)
    kk = search(song_info_one)
    if (kk == 5):
        print('没有搜索到歌曲:')

    # 获取歌曲链接
    print('GETLINK {0}-{1}'.format(song_info_one['signernames'], song_info_one['songname']))
    get_download_link(song_info_one, music_dir, unlock_key)
    # print(song_info)

    print('DOWNLOAD {0}-{1}'.format(song_info_one['signernames'], song_info_one['songname']))
    download_file(song_info_one, music_dir)
    store_json(paylist_info_json_path, song_info_one)

    print('SUCCESS {0}'.format(song_info_one['signernames']))
