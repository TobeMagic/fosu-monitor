from lxml import etree  # 导入所需模块
import requests, re
from .models import *
import logging

logger = logging.getLogger(__name__)
root_url = "https://tieba.baidu.com"

headers = {
    'Cookie': 'BIDUPSID=866898E0946D426E2BA942EB7E04C238; PSTM=1654829584; BAIDUID=0E6F92F82F5D8E3F52E549557D0A109C:FG=1; ZFY=K:BRPd7PUk:BsUx0mfzRxaSamFwoKIqdbikE3VGJ:AzUZM:C; BAIDUID_BFESS=638FC4CC79A838E35D7F163F12574F2E:FG=1; delPer=0; PSINO=7; ZD_ENTRY=bing; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1659403217; st_key_id=17; BAIDU_WISE_UID=wapp_1659403219065_126; USER_JUMP=-1; wise_device=0; H_BDCLCKID_SF_BFESS=tJIH_CI-JKP3e5rFMRrWq4tehHRjaqO9WDTm_Do5LC52sI3ebU553qLDjPbjKMn82NQZ-pPKBMoMfxI934TWBUoWKRnB5-PL3mkjbInyfn02OP5P245T3-4syP4eKMRnWTbJKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCFKhD8GjT02j6PW5ptXhtjBHD7yWCkMWhbcOR5Jj65Cjq4PXt6RWJcNbCbuBD3zb4_MeCJ43MA-BPC8bUrZBM5a5jvhoRQR0bvOsq0x05ole-bQypoaLho7QIOMahkb5h7xO-nmQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3tjjISKx-_J68ftJRP; BCLID_BFESS=11544490163026275597; BDSFRCVID_BFESS=0KDOJeC62R5_IMJDNyRuhMj7Mur4f0rTH6_negiJKFbfwf1fSCkkEG0P5U8g0KubWQHTogKK3gOTHxtF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; 5815417608_FRSVideoUploadTip=1; video_bubble5815417608=1; BAIDU_SSP_lcr=http://localhost:8888/; baidu_broswer_setup_D19287875834=0; RT="z=1&dm=baidu.com&si=zkzpbq5eng&ss=l6hmwiy0&sl=8&tt=6rn&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=gv9c&ul=gw8c&hd=gw8p"; video_bubble0=1; H_PS_PSSID=36838_36542_36625_36726_37110_36413_36847_36955_36165_36918_36570_36776_37011_36746_37055_26350_36866_36930; BA_HECTOR=ah000h018l00ag8ga5ake68e1heso3f17; BDUSS=0piMEw1cDVhNWJ5fnJVcWtZaVJaYzBnRGRad1B4M1Y2dEdUeXpDVFRNRVA5UlZqSVFBQUFBJCQAAAAAAQAAAAEAAAAIO6BaRDE5Mjg3ODc1ODM0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9o7mIPaO5ia; BDUSS_BFESS=0piMEw1cDVhNWJ5fnJVcWtZaVJaYzBnRGRad1B4M1Y2dEdUeXpDVFRNRVA5UlZqSVFBQUFBJCQAAAAAAQAAAAEAAAAIO6BaRDE5Mjg3ODc1ODM0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9o7mIPaO5ia; STOKEN=bd0ff5ed0a43a269e82eced8f9f71129d57d19b5db63ce997a21e67c27e2d072; ab_sr=1.0.1_ODNmNjdkYWU3NmI0MDJhYmEyNmU4MDlmYzQwZDNiZjdmNzZkNThhZjcxMjFlM2M1YjQ2NmRkMWI3MTUyYjg5YmM4YjQ4NjUyZDgwYzI5M2NlYTk5M2I2N2MyMTJlM2IzYWI4M2ZlZDYxNTg1OWI1MTcxMjg2MDQ2N2UzZWZhZDg3ZWE5NmE3ZmI0ZGFjY2U3MDI5YWM0NGZmNDY3MmNkOWNmMjFkMmViMjMyOTQyOGMyZDJjNmM2OTJhNGVlODlk; st_data=eb92fe587fb052c0d2d96715f9ae75ef05129347dcdb07077c5e5b3bd9e3e69299b0d28bbe0bdd201e38784743e5db905ead200a2408bbcbdbadd1a27629e458ffc2f16608e94a49b8766d40a2e8a9902b7eebf0e6c6e859940571be947ca2f0; st_sign=d49319cc; tb_as_data=a73396ee5554a84966767c767c75643a6523d7ed65e89f100ee8c4d5ae86d20676cf78a08cc6103c66d9aa9b5bc9e0c175175b3fa9c7fb9b3bc4c8a8ea33c7da0e0e92e0ef3be197ccc39da937cc8dbd5c6b38f3b1f676cf424bfdb11786492f07068392aa1a6fca2491bccbc1e5f40b; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1659791400',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

# 二级评论参数
second_page = 1  # 默认只爬取第一页
param_second = {
    'pn': str(second_page)
}


# @register_job(scheduler, 'interval', id='baidu', minutes=1)
def async_collect_baidu():
    """
    爬取百度贴吧帖子，一级评论
    :param :None
    Returns:
         HttpRedirect
    """
    # 获取帖吧内容
    page_first = 0  # 第一页
    while page_first < 5:  # 默认爬取五页
        resp = requests.get('https://tieba.baidu.com/f?kw=佛山科学技术学院&ie=utf-8' + f'&pn={page_first * 50}',
                            headers=headers)
        html_baidu = resp.content.decode('utf-8')  # 手动解码  text默认返回猜测的解码方式
        # 根路由
        tree_baidu = etree.HTML(html_baidu)
        divs_baidu = tree_baidu.xpath('//*[@id="thread_list"]/li')

        # 获取帖子字典
        for div in divs_baidu:
            dict_temp = {}
            if bool(div.xpath('./div/div[2]/div[1]/div[1]/a/@href')):
                dict_temp['id'] = re.sub(r'/p/', '', div.xpath('./div/div[2]/div[1]/div[1]/a/@href')[0])
                dict_temp['comment'] = div.xpath('./div/div[2]/div[1]/div[1]/a/text()')
                dict_temp['href'] = root_url + div.xpath('./div/div[2]/div[1]/div[1]/a/@href')[0]
                dict_temp['img'] = div.xpath(
                    f'//*[@id="fm{re.sub(r"/p/", "", div.xpath("./div/div[2]/div[1]/div[1]/a/@href")[0])}"]/li/a/img/@data-original')
                #  保存帖子到数据库
                if not BaiduPost.objects.filter(post_id=dict_temp['id']).first():
                    baidu_post = BaiduPost.objects.create(
                        post_id=dict_temp['id'],
                        title=dict_temp['comment'][0],
                        url=dict_temp['href'],
                        img_url=dict_temp['img']
                    )
                    baidu_post.save()

                    resp_second = requests.get(url=dict_temp['href'], params=param_second)  # 获取响应
                    second_html = resp_second.content.decode('utf-8')  # 获取源码
                    second_tree = etree.HTML(second_html)  # 解析源代码
                    second_root = second_tree.xpath('//*[@id="j_p_postlist"]/div')  # 获取节点树

                    second_comments = []  # 收集所有二级评论
                    second_comment_dict = {}
                    for comment in second_root:
                        if comment.xpath('./div[2]/ul/li[3]/a/@href'):  # 空字符串是广告

                            second_comment_dict = {
                                'user': comment.xpath('./div[2]/ul/li[3]/a/text()'),  # 用户名
                                'user_url': root_url + comment.xpath('./div[2]/ul/li[3]/a/@href')[0],  # 用户主页
                                'comment': comment.xpath('./div[3]/div[1]/cc/div[2]')[0].xpath("string(.)").strip()
                            }  # 评论内容
                        if second_comment_dict not in second_comments:  # 去重
                            second_comments.append(second_comment_dict)
                            #  保存到用户和一级评论数据库
                            if not bool(BaiduUser.objects.filter(url=second_comment_dict['user_url']).first()) and \
                                    second_comment_dict['user'] is not None:
                                baidu_user = BaiduUser.objects.create(
                                    username=second_comment_dict['user'][0],
                                    url=second_comment_dict['user_url']
                                )
                                baidu_user.save()
                                baidu_comment = BaiduComment.objects.create(
                                    BaiduUser=baidu_user,
                                    comment=second_comment_dict['comment'],
                                    BaiduPost=baidu_post
                                )
                                baidu_comment.save()

                    logger.info('帖子id: {},标题：{},帖子地址:{},图片:{},评论数：{}'.format(dict_temp['id'],
                                                                             dict_temp['comment'],
                                                                             dict_temp['href'],
                                                                             dict_temp['img'],
                                                                             len(second_comments)))
        page_first += 1  # 贴吧页数

    logger.info('贴吧爬取完毕!')
