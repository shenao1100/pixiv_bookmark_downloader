#-*- coding:utf-8 -*-
#CREATER: ShenAo

import os
import NTG_base
import json
import time
from urllib.parse import unquote, quote




class PixivAccount:
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie
        self.userid = False
        self.bookmarks_list = []
        pass

    def get_bookmarks(self, lines: int):
        if not self.userid:
            return False

        headers = {
            'Cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
            'x-userid': self.userid,
        }
        url = 'https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit=100&rest=show&lang=zh'.format(str(self.userid), str(lines))
        result = NTG_base.get(url=url, header=headers, proxy=proxy)['text']
        if result:
            result = unquote(result)
            p_json = json.loads(result)
            return {'list': p_json["body"]["works"], 'total': p_json["body"]["total"]}
        else:
            return False
    
    def get_temp(self):
        return self.bookmarks_list

    def get_all_bookmarks(self):
        count = 0
        while True:
            print('[', int(time.time()), '] 正在获取 offset', count, end='\r')
            result = self.get_bookmarks(count)['list']
            count += 100
            if result == []:
                break
            else:
                self.bookmarks_list += result
        return len(self.bookmarks_list)

    def get_user_id(self):
        url = 'https://www.pixiv.net/ajax/user/extra?lang=zh'
        headers = {
            'Cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
        }
        result = NTG_base.get(url=url, header=headers, proxy=proxy)['headers']
        if result:
            self.userid = result['x-userid']
            return self.userid
        else:
            return False
    
    def download_pic(self, url, path, count, header):
        print('[', int(time.time()), ']         开始下载', count, '个')
        path = os.path.join(path, str(count) + '.jpg')

        for i in range(5):
            try:
                with open(path,'wb') as f:
                    f.write(NTG_base.get(url, header=header, proxy=proxy)['content'])
                return True
            except:
                continue
        return False

    def analyse_pic(self, author_id, pic_id, file_info):
        #creat download dirs
        save_path = os.path.join(down_path, str(author_id), str(pic_id))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        #insert pic information
        json_path = os.path.join(save_path, 'info.json')
        NTG_base.write_file(json_path, json.dumps(file_info))
        #get resources url
        print('[', int(time.time()), '] 开始获取', pic_id)
        url = 'https://www.pixiv.net/ajax/illust/' + str(pic_id) + '/pages?lang=zh'
        headers = {
            'authority': 'www.pixiv.net',
            'method': 'GET',
            'path': '/ajax/illust/' + str(pic_id) + '/pages?lang=zh',
            'scheme': 'https',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': self.cookie,
            'referer': 'https://www.pixiv.net/artworks/' + str(pic_id),
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57',
            'x-user-id': self.userid,
        }
        photo_urls = NTG_base.get(url, header=headers, proxy=proxy)['text']
        headers = {
            'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://www.pixiv.net/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71',
            'authority': 'i.pximg.net',
            'method': 'GET',
            #'path: /img-original/img/2022/07/26/00/04/34/99996934_p0.png',
            'scheme': 'https',
        }
        if photo_urls:
            photo_urls = json.loads(photo_urls)['body']
            print('[', int(time.time()), ']         获取', pic_id, '完毕，共', len(photo_urls), '个')
            count = 0
            for url in photo_urls:
                count += 1
                self.download_pic(url['urls']['original'], save_path, str(count), headers)
                print('[', int(time.time()), ']         下载第', count, '个完毕')
        else:
            return False


        
    
if __name__ == '__main__':
    # 在此处添加您的cookie
    cookie = ''
    # 在此处设置下载路径
    down_path = 'D:\\pixiv_bm\\'
    # 在此处设置代理
    proxy = {
        'http': '127.0.0.1:10809',
        'https': '127.0.0.1:10809',
    }
    #proxy = ''     #若不需要代理请取消注释此条信息
    error_msg = ''
    pj_pixiv = PixivAccount(cookie)
    print('[', int(time.time()), '] 用户ID:', pj_pixiv.get_user_id())
    print('[', int(time.time()), '] 已找到Bookmarks:', pj_pixiv.get_all_bookmarks(), '个')
    print('=' * 20)
    count_total = 0
    for pic_infos in pj_pixiv.get_temp():
        count_total += 1
        print('[', int(time.time()), '] 正在下载第', count_total, '个(共', len(pj_pixiv.get_temp()), '个, ID', pic_infos['id'])
        result = pj_pixiv.analyse_pic(pic_infos['userId'], pic_infos['id'], pic_infos)
        if not result:
            error_msg += json.dumps(pic_infos) + '\n'
    if error_msg != '':
        NTG_base.write_file(os.path.join(down_path, 'error.json'), error_msg)
        print('[', int(time.time()), '] 发生错误，未下载成功的图片信息已保存至下载根目录的error.json')

        
