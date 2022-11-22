import os, json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import requests
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .models import *


# 控制页面滑动
def scrob(driver):
    time.sleep(2)
    try:
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
        # print("以滑动")
    except:
        print("滑动失败")


# 获取全文内容
def get_all_text(driver, elem):
    try:
        # 判断是否有“全文内容”，若有则将内容存储在weibo_content中
        href = elem.find_element_by_link_text('全文').get_attribute('href')
        driver.execute_script('window.open("{}")'.format(href))
        driver.switch_to.window(driver.window_handles[1])
        weibo_content = driver.find_element_by_class_name('weibo-text').text
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        weibo_content = elem.find_elements_by_css_selector('div.weibo-text')[0].text
    return weibo_content


def getemojy(elem, xpath, istest=False):
    """
    实现判断元素是否存在
    :param elem: 浏览器对象
    :param xpath: xpath表达式
    :param istest: 如果为True,如果元素存在返回内容将为元素文本内容
    """
    try:
        target = elem.find_element_by_xpath(xpath)
    except exceptions.NoSuchElementException:
        # print("表情没找到")
        return ''
    else:
        if istest:
            return target.get_attribute('alt')


def iselement(elem, css_sel, istest=False):
    """
    实现判断元素是否存在
    :param elem: 浏览器对象
    :param css_sel: css_selector表达式
    :param istest: 如果为True,如果元素存在返回内容将为元素对象
    """
    try:
        target = elem.find_element_by_css_selector(css_sel)
    except exceptions.NoSuchElementException:
        return ''
        pass
    else:
        if istest:
            # print("获取到多条回复")
            return target
        else:
            return ''


# 获取评论
def get_comments(driver, elem, num, art_id):
    try:
        # time.sleep(2)
        # # 解决评论被屏蔽
        # driver.refresh()
        time.sleep(3)
        # # 根据评论数进行滑动并再获取0
        for i in range(int(num / 20)):
            scrob(driver)
        # 页面跳转

        pinluns_qu = driver.find_elements_by_css_selector('div.comment-content')  # 获取评论区
        # print(pinluns_qu)
        pinluns = pinluns_qu[0].find_elements_by_css_selector('div.m-text-box')  # 获取每个评论
        try:
            i = 0
            # print("进入评论区了")
            for pinlun in pinluns:
                user = pinlun.find_element_by_css_selector('h4').text
                pp = pinlun.find_element_by_css_selector('h3')  # 评论
                # 获取到评论先根据帖子ID 写进第二张表，然后返回第二张表的ID
                # 获取到评论的回复之后再进行切割。获取第二张表的ID绑定 写入第三张表

                emojoy = getemojy(pp, 'span[1]/img', True)  # 获取表情
                comment = pp.text + emojoy
                # 评论去重
                if WeiboFirstComment.objects.filter(username=user, context=comment):
                    first_id = WeiboFirstComment.objects.filter(username=user, context=comment).first().pk
                    pass
                else:
                    first_id = insert_first(user, comment, art_id)
                # 获取评论回复
                comment_reply = iselement(pinlun, 'div.cmt-sub-txt', True)  # 返回一个对象
                if comment_reply:
                    # 找得到无法点击，因为不在屏幕上，要滑动窗口，那么如何自己判断呢？使用js
                    # 那如果出现多个怎么办？先拿到全部的个数再进行i计数，dao
                    botton = 'document.getElementsByClassName("cmt-sub-txt")[%d].click();' % i
                    driver.execute_script(botton)
                    # driver.execute_script("window.scrollBy(0,document.body.scrollHeight/5)", "")
                    # time.sleep(2)
                    # comment_reply.click()
                    rply = driver.find_elements_by_css_selector('div.card.m-avatar-box.lite-page-list.list-bg')
                    # print("评论回复有%d条：如下" % len(rply))
                    for rp in rply:
                        rply_user = rp.find_element_by_css_selector('h4').text
                        rply_cont = rp.find_element_by_css_selector('h3').text
                        # print(rply_user, rply_cont)
                        # 评论回复去重
                        queryset = WeiboSecondComment.objects.filter(username=rply_user, context=rply_cont).first()
                        if queryset:
                            pass
                        else:
                            insert_sec(rply_user, rply_cont, first_id, art_id)
                    i += 1
                    time.sleep(1)
                    botton = 'document.getElementsByClassName("m-font-arrow-left")[0].click();'
                    driver.execute_script(botton)
                    time.sleep(2)
        except Exception as e:
            print(e)
            pass
        # 返回按钮
        btn = driver.find_element_by_css_selector("i.m-font.m-font-arrow-left")
        btn.click()
        time.sleep(3)

    except:
        pass


# 获取图片链接
def get_pic(elem):
    links = ""
    try:
        # 获取该条微博中的图片元素,之后遍历每个图片元素，获取图片链接并下载图片
        # 如果是多张图片
        if elem.find_elements_by_css_selector('div > div > article > div > div:nth-child(2) > div > ul > li') != []:
            pic_links = elem.find_elements_by_css_selector(
                'div > div > article > div > div:nth-child(2) > div > ul > li')
            for pic_link in pic_links:
                pic_link = pic_link.find_element_by_css_selector('div > img').get_attribute('src')
                links = pic_link + ";"
        # 如果图片只有一张
        else:
            pic_link = elem.find_element_by_css_selector(
                'div > div > article > div > div:nth-child(2) > div > div > img').get_attribute('src')
            links = pic_link + ";"
    except Exception as e:
        # print(e)
        pass
    return links


# 1.用于将cookie字符串转换为对象，因为后面add_cookie需要传字典进去
def ParseCookiestr(cookie_str):
    cookielist = []
    cookie_str = cookie_str.strip()
    for item in cookie_str.split(';'):
        temp = item.split('=')
        cookie = {}
        # 注意前导空格，不去除会unable to set cookie
        item_name = item.split('=')[0].strip()
        item_value = ""
        for i in range(1, len(temp)):
            item_value += temp[i]
        cookie['name'] = item_name
        # 将url上一堆转码的东西转回原始
        # cookie['value'] = urllib.parse.unquote(item_value)
        cookie['value'] = item_value
        cookielist.append(cookie)
    # print(cookielist)
    return cookielist


def saveCookie(mode, cookies_file, webdriver):
    """

    :param mode: 使用的模式，selenium,pickle,json
    :param cookies_file: 存放cookies的文件路径
    :param webdriver: selenium的浏览器driver
    :return:
    """
    if mode == 'selenium':
        # 2,直接储存selenium
        with open(cookies_file, 'w') as f:
            json.dump(webdriver.get_cookies(), f)


def useCookie(mode, cookies_file, webdriver):
    """
    mode : 使用的模式，brower,selenium,pickle,json
    cookies_file : 存放cookies的文件路径
    webdriver : selenium的浏览器driver
    :return:
    """
    # 删除原先所以cookies
    webdriver.delete_all_cookies()
    # 3，从浏览器复制的cookie转化使用
    if mode == 'brower':
        with open(cookies_file, 'r') as f:
            cookielist = ParseCookiestr(f.read())
            for i in cookielist:
                cookie = {}
                # 3.对于使用add_cookie来说，参考其函数源码注释，需要有name,value字段来表示一条cookie，有点生硬
                cookie['name'] = i['name']
                cookie['value'] = i['value']
                # 4.这里需要先删掉之前那次访问时的同名cookie，不然自己设置的cookie会失效
                webdriver.delete_cookie(i['name'])
                # 添加自己的cookie
                webdriver.add_cookie(cookie)
    elif mode == 'selenium':
        # # 从selenium保存的cookie使用
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cook in cookies:
                webdriver.add_cookie(cook)


def insert_weibo(user_name, weibo_content, likes, comments, shares, tim, links_text, art_links):
    WeiboArticle.objects.create(
        username=user_name,
        article=weibo_content,
        likes_num=int(likes),
        comment_num=int(comments),
        transmit_num=int(shares),
        c_time=tim,
        pic_links=links_text,
        art_links=art_links
    )
    pk = WeiboArticle.objects.get(username=user_name, article=weibo_content).pk
    return pk


def insert_first(user, comment, art_id):
    WeiboFirstComment.objects.create(
        username=user,
        context=comment,
        art_id=art_id,
    )
    return WeiboFirstComment.objects.get(
        username=user,
        context=comment
    ).pk


def insert_sec(user, reply, fir_id, art_id):
    WeiboSecondComment.objects.create(
        username=user,
        context=reply,
        com_id=fir_id,
        art_id=art_id
    )
    return WeiboSecondComment.objects.get(
        username=user,
        context=reply
    ).pk


def get_code():
    code = ''
    i = 0
    # 超过50秒获取不到就退出循环
    while code == '':
        # print(i)
        code = requests.get('http://vhost43469.80.vrvr.cn/mget.php').text
        # print(type(code))
        # print(code)
        i += 1
        if i > 5:
            break
        time.sleep(10)
    # print(code)
    return code


def code_login(driver, username, password, cookies_file):
    # 加载驱动，使用浏览器打开指定网址

    driver.get("https://passport.weibo.cn/signin/login")
    print("开始自动登陆，若出现验证码手动验证")
    time.sleep(3)

    elem = driver.find_element_by_xpath("//*[@id='loginName']")
    elem.send_keys(username)
    elem = driver.find_element_by_xpath("//*[@id='loginPassword']")
    elem.send_keys(password)
    elem = driver.find_element_by_xpath("//*[@id='loginAction']")
    elem.send_keys(Keys.ENTER)
    # print("暂停20秒，用于验证码验证")
    time.sleep(2)

    # 点击激活
    driver.find_element_by_xpath('//*[@id="protectGuide"]/div/div/div[3]/a').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="vdVerify"]/div[1]/div/div/div[3]/a').click()
    # 先获取一次验证码接口，清除可能存在的旧验证码
    code = requests.get('http://vhost43469.80.vrvr.cn/mget.php').text
    time.sleep(20)
    driver.find_element_by_xpath('//*[@id="verifyCode"]/div[1]/div/div/div[2]/div/div/div/span[1]/input').send_keys(
        get_code())
    # # 点击登录
    driver.find_element_by_xpath('//*[@id="verifyCode"]/div[1]/div/div/div[3]/a').click()
    # 保存cookies
    time.sleep(3)
    saveCookie('selenium', cookies_file, driver)
    print("cookie保存成功")
    # return "登陆成功"


def login(driver, username, password, cookies_file):
    # 如果存在cookies，默认用selenium自身保存的cookies
    if os.path.exists(cookies_file):
        # sz = os.path.getsize(cookies_file)
        # print(sz)
        with open(cookies_file, 'r') as f:
            str = f.read().strip()
        # 若为空文件不执行设置cookies
        if str == "":
            # print(cookies_file, " is empty!启用短信登录")
            code_login(driver, username, password, cookies_file)
        else:
            driver.get(url)
            time.sleep(3)
            useCookie('selenium', cookies_file, driver)
            driver.refresh()
            time.sleep(2)
            # print(driver.get_cookie('MLOGIN')['value'])
            # print(type(driver.get_cookie('MLOGIN')['value']))
            # cookie失效验证
            if driver.get_cookie('MLOGIN')['value'] == '0':
                # print("cookie失效，启用短信登录")
                code_login(driver, username, password, cookies_file)
            time.sleep(2)
    else:
        driver.get(url)
        time.sleep(3)
        useCookie('selenium', cookies_file, driver)
        driver.refresh()
        time.sleep(2)
        # print(driver.get_cookie('MLOGIN')['value'])
        # print(type(driver.get_cookie('MLOGIN')['value']))
        # cookie失效验证
        if driver.get_cookie('MLOGIN')['value'] == '0':
            # print("cookie失效，启用短信登录")
            code_login(driver, username, password, cookies_file)
        time.sleep(2)

def spider(driver, num):
    try:
        driver.get(url)
        # 登录状态每页17个
        # 先抓全文，用户等，再根据是否有评论再去抓评论
        for i in range(0, num):
            # 在里面加srcb就会进不了评论区
            print("次数：" + str(i))
            if (i >= 17):
                for j in range(0, int(i / 17)):
                    scrob(driver)
            time.sleep(3)
            try:
                elem = driver.find_elements_by_css_selector('div.card.m-panel.card9')[i]
                # 获取时间
                tim = elem.find_element_by_css_selector("span.time").text
                # print(tim)
                # print(driver.page_source)
                user_name = elem.find_elements_by_css_selector('h3.m-text-cut')[0].text
                # 微博内容
                # 点击“全文”，获取完整的微博文字内容
                weibo_content = get_all_text(driver, elem)
                # 获取图片链接
                links_text = get_pic(elem)
                # if links_text:
                #     print(links_text)
                # 获取分享数，评论数和点赞数
                shares = elem.find_elements_by_css_selector('i.m-font.m-font-forward + h4')[0].text
                if shares == '转发':
                    shares = '0'
                likes = elem.find_elements_by_css_selector('i.m-icon.m-icon-like + h4')[0].text
                if likes == '赞':
                    likes = '0'
                comments = elem.find_elements_by_css_selector('i.m-font.m-font-comment + h4')[0].text
                # print(comments)
                if comments == '评论':
                    comments = '0'
                # 获取文章链接并进入评论区
                wait = WebDriverWait(elem, timeout=10)
                wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, "div.weibo-text")))
                # elem.find_elements_by_css_selector('div.weibo-text')[0].click()
                botton = 'document.getElementsByClassName("weibo-text")[%d].click();' % i
                driver.execute_script(botton)
                time.sleep(2)
                driver.refresh()
                current_url = driver.current_url
                # print(driver.current_url)
                print("用户名：{}，内容：{}，点赞：{}，评论：{}，转发：{}".format(user_name, weibo_content, likes, comments, shares))
                # 先写入第一张表，返回一个ID，传给评论获取
                # 去重：
                queryset = WeiboArticle.objects.filter(username=user_name, article=weibo_content).first()
                if queryset:
                    if int(queryset.comment_num) == int(comments):
                        # wait = WebDriverWait(driver, timeout=10)
                        # wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, "i.m-font.m-font-arrow-left")))
                        # 当评论无更新要记得返回
                        # botton = 'document.getElementsByClassName("m-font-arrow-left")[0].click();'
                        # driver.execute_script(botton)
                        # time.sleep(2)
                        # btn = driver.find_element_by_css_selector("i.m-font.m-font-arrow-left")
                        btn = iselement(driver, "i.m-font.m-font-arrow-left", True)
                        j = 0
                        while (btn == ''):
                            driver.refresh()
                            time.sleep(5)
                            j += 1
                            if j > 3:
                                # 网络问题
                                continue
                                # break # 触发反爬机制
                        btn.click()
                        time.sleep(3)
                    else:
                        get_comments(driver, elem, int(comments), queryset.pk)
                else:
                    art_id = insert_weibo(user_name, weibo_content, likes, comments, shares, tim, links_text,
                                          current_url)
                    # print("已写入文章")
                    get_comments(driver, elem, int(comments), art_id)
                # 延迟抓取，避免触发反爬机制
                time.sleep(25)
            except:
                pass
    except:
        pass


url = 'https://m.weibo.cn/p/index?containerid=100808165ef5c505a4b4f59142bc0a0f0aafae&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BD%9B%E5%B1%B1%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2'


def run():
    # chrome版本大于88
    opt = Options()
    opt.add_argument("--disable-blink-features=AutomationControlled")
    opt.add_argument("--disable-gpu")
    opt.add_argument('--headless')
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    opt.add_argument("user-agent=" + ua)
    # driver = webdriver.Chrome(options=opt)  # 本地 你的chromedriver的地址
    driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=opt)# 服务器设置
    # 爬取
    username = '19965440781'
    password = 'buzhi123456'
    # username = '19304914193'
    # password = '123456buzhi'
    driver.get('https://m.weibo.cn')
    driver.implicitly_wait(2)  # 隐式等待2秒
    login(driver, username, password, 'apps/monitor/wb_cookie.txt')
    spider(driver, 100)
    driver.quit()
