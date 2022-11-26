import requests
from fake_useragent import UserAgent
from lxml import etree


ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_url(url):
    proxy = "socks5://127.0.0.1:6532"
    proxies = {
        "HTTP": proxy,
        "https": proxy
    }
    session = requests.session()
    response = session.get(url, headers=headers, proxies=proxies)
    # print(response.status_code)
    # print(response.text)
    response_html = response.text
    return response_html


def get_etree(response_html):
    tree = etree.HTML(response_html)
    links = tree.xpath('/html/body/div/div/div/div/div/div/a[1]/@href')
    titles = tree.xpath('/html/body/div/div/div/div/div/div/a/h3/text()')
    for link, title in zip(links, titles):
        if "/mp/" in link:
            link = "https://www.hong.ke" + link
        print("\033[32m"+link+"\033[0m"+" ----- " + "\033[31m"+title+" \033[0m")


if __name__ == '__main__':
    search = input("请输入您要搜索的内容>>>")
    search = requests.utils.quote(search)
    for i in range(10):
        if i != 0:
            url = "https://www.hong.ke/search?query="+search+"&page=" + str(i)
            print("\033[1;35m正在爬取第{}页面".format(i)+"\n爬取的URL："+url+" \033[0m")
            try:
                try:
                    response_html = get_url(url)
                    get_etree(response_html)
                except requests.exceptions.SSLError:
                    print("socks request error!")
                except Exception as e:
                    print("error!")
            except KeyboardInterrupt:
                print("you shutdown the Procedure")
                break






