from sixyin import search_one,get_download_link_one
from down import download_file_one

def done(songInput,music_dirr, unlock_keyy,songTypeInput):
    # 搜索歌曲
    songInputs = songInput.split("-");
    if len(songInputs) == 3:
        song_info_one = {'songname': songInputs[0], 'signernames': songInputs[1], 'albumname': songInputs[2]}
    elif len(songInputs) == 2:
        song_info_one = {'songname': songInputs[0], 'signernames': songInputs[1]}
    elif len(songInputs) == 1:
        song_info_one = {'songname': songInputs[0]}
    else:
        print('输入歌曲信息非法' + songInput)



    print('SEARCH --' + songInput)
    kk = search_one(song_info_one,len(songInputs))
    if (kk == len(songInputs)):
        print('没有搜索到歌曲:')

    # 获取歌曲链接
    print('GETLINK {0}'.format( song_info_one['songname']))
    get_download_link_one(song_info_one, music_dirr, unlock_keyy,songTypeInput)
    # print(song_info)

    print('DOWNLOAD {0}'.format( song_info_one['songname']))
    download_file_one(song_info_one, music_dirr)

    print('SUCCESS {0}'.format(song_info_one['songname']))
    print('歌曲已下载至 {0}'.format(music_dirr))


