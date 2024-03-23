import os

import requests
from requests.adapters import HTTPAdapter, Retry
from get_list import  get_list,list_split
from sixyin import verify_key
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from ones import dones
from one import done

print('本项目用于个人QQ音乐批量下载歌单的无损格式音乐')
print('⚠: 仅支持研究用途，严禁用于商业用途，请于24小时内删除通过本项目下载的音乐，有意向获取无损音乐请购买实体专辑。')
print('--------------------------------------')
inputstr = 'y'
unlock_key = ''
while inputstr == 'y':
    # 1输入
    downTypeInput = input("请输入下载方式(1:列表下载 2:单曲下载)：")
    if downTypeInput == '2':
        songInput = input("请输入歌曲信息(歌曲名-歌手-专辑)：")
        if unlock_key == '':
            unlock_keyItt = input("请输入下载token(关注微信公众号-黑话君,输入‘音乐密码’获取)：")
            unlock_key = unlock_keyItt
        songTypeInput = input("请输入下载格式(1:sizeflac,2:size320,3:size128)：")
        parent_directory = os.path.dirname(os.getcwd())
        #parent_directory = os.getcwd()
        music_dir = parent_directory + '\\MuiscDownLoadFile\music'
    else:
        playlist_idInput = input("请输入列表id(分享QQ音乐歌单,查看分享链接中的id就是)：")
        if unlock_key == '':
            unlock_keyItt = input("请输入下载token(关注微信公众号-黑话君,输入‘音乐密码’获取)：")
            unlock_key = unlock_keyItt
        songTypeInput = input("请输入下载格式(1:sizeflac,2:size320,3:size128)：")
        lineInput = input("请输入下载线程个数(建议最大10)")
        playlist_id = playlist_idInput
        parent_directory = os.path.dirname(os.getcwd())
        #parent_directory = os.getcwd()
        cache_dir = parent_directory + '\\MuiscDownLoadFile\\cache'
        music_dir = parent_directory + '\\MuiscDownLoadFile\\music'
        export_dir = parent_directory + '\\MuiscDownLoadFile\\' + playlist_id + '-export'
        paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
        paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))

    if downTypeInput == '2':
        # 需通过flac.life官网免费获取解锁码
        stat = verify_key(unlock_key)
        #print('key verify: ', stat)
        if stat is False:
            print('下载token错误！！！')
            raise Exception()

        idd = 1;
        music_dirr = music_dir
        while os.path.exists(music_dirr):
            music_dirr = music_dir+str(idd)
            idd = idd+1
        os.makedirs(music_dirr)
        done(songInput,music_dirr,unlock_key,songTypeInput)
    elif downTypeInput == '1':
        #2本地运行
        '''
        downTypeInput = '1'
        unlock_keyInput = '4165' # 需通过flac.life官网免费获取解锁码
        #1:sizeflac,2:size320,3:size128
        songTypeInput = '2'
        playlist_id = '6382603002'
        
        parent_directory = os.path.dirname(os.getcwd())
        cache_dir = parent_directory + '\\QMuDownLoadCache2\\cache'
        music_dir = parent_directory + '\\QMuDownLoadCache2\\music'
        export_dir = parent_directory + '\\QMuDownLoadCache2\\' + playlist_id + '-export'
        paylist_raw_json_path = os.path.join(cache_dir, 'playlist.{0}.raw.json'.format(playlist_id))
        paylist_info_json_path = os.path.join(cache_dir, 'playlist.{0}.json'.format(playlist_id))
        '''
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)

        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        #需通过flac.life官网免费获取解锁码
        stat = verify_key(unlock_key)
        print('key verify: ', stat)
        if stat is False:
            raise Exception()

        playlist_raw = get_list(playlist_id)
        cur = playlist_raw['data']['cdlist'][0]['songlist']
        numone = int(len(cur)/int(lineInput))
        playlist_rawsplit = list_split(playlist_raw['data']['cdlist'][0]['songlist'],numone)
        #跑单个
        #dange = list_split(playlist_rawsplit[5],10)

        ss =len(playlist_rawsplit)
        idxx = 1
        all_task = []
        with ThreadPoolExecutor(max_workers=int(lineInput)) as pool:
            for cnt in playlist_rawsplit:
                all_task.append(pool.submit(dones,cnt,idxx,cache_dir,music_dir,export_dir,playlist_id,songTypeInput,unlock_key))
                idxx = idxx + 1

            # 主线程等待所有子线程完成
            wait(all_task, return_when=ALL_COMPLETED)
            print("----complete-----")
        print('歌曲列表已下载至 {0}'.format(export_dir))

    else:
        print("下载方式输入格式有误")

    inputstr = input("是否继续下载?(y/f)")
    while inputstr != 'y' and inputstr != 'f':
        inputstr = input("输入有误，请重新输入，是否退出?(y/f)")







