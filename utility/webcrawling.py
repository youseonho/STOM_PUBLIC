import random
import requests
import matplotlib
import pandas as pd
from urllib import request
from threading import Timer
from bs4 import BeautifulSoup
from utility.setting import ui_num
from utility.static import thread_decorator


class WebCrawling:
    def __init__(self, qlist):
        """
        windowQ, soundQ, queryQ, teleQ, chartQ, hogaQ, webcQ, backQ, creceivQ, ctraderQ,  cstgQ, liveQ, kimpQ, wdzservQ
           0        1       2      3       4      5      6      7       8         9         10     11    12      13
        """
        self.windowQ   = qlist[0]
        self.webcQ     = qlist[6]
        self.backQ     = qlist[7]
        self.cmap      = matplotlib.colormaps['hsv']
        self.treemap   = False
        self.imagelist1 = None
        self.imagelist2 = None
        self.Start()

    def Start(self):
        while True:
            data = self.webcQ.get()
            self.Crawling(data)

    def Crawling(self, data):
        cmd, data = data
        if cmd == '기업정보':
            self.GugyCrawling(data)
            self.GugsCrawling(data)
            self.JmnsCrawling(data)
            self.JmjpCrawling(data)
        elif cmd == '트리맵':
            self.treemap = True
            self.UjTmCrawling()
        elif cmd == '트리맵1':
            self.UjTmCrawlingDetail(data, 1)
        elif cmd == '트리맵2':
            self.UjTmCrawlingDetail(data, 2)
        elif cmd == '트리맵중단':
            self.treemap = False
        elif cmd == '지수차트':
            self.JisuCrawling(data)
        elif cmd == '풍경사진요청':
            self.GetImage()

    @thread_decorator
    def GetImage(self):
        try:
            if self.imagelist1 is None:
                url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EA%B3%A0%ED%99%94%EC%A7%88%ED%92%8D%EA%B2%BD%EA%B0%80%EB%A1%9C%EC%82%AC%EC%A7%84&oquery=%EA%B3%A0%ED%99%94%EC%A7%88%ED%92%8D%EA%B2%BD%EA%B0%80%EB%A1%9C%EC%82%AC%EC%A7%84&tqi=iAM7jwqVN8VsslwnmiossssstI4-416434'
                self.imagelist1 = requests.get(url).text.split('viewerThumb:"')[1:]
                self.imagelist1 = [x.split('.jpg')[0] + '.jpg' for x in self.imagelist1]
                self.imagelist1 = [x for x in self.imagelist1 if 'lensThumb' not in x]
            if self.imagelist2 is None:
                url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EA%B3%A0%ED%99%94%EC%A7%88%ED%92%8D%EA%B2%BD%EC%84%B8%EB%A1%9C%EC%82%AC%EC%A7%84&oquery=%EA%B3%A0%ED%99%94%EC%A7%88%ED%92%8D%EA%B2%BD%EA%B0%80%EB%A1%9C%EC%82%AC%EC%A7%84&tqi=iAM7OdqVOsVssAwVjfossssstwd-182384'
                self.imagelist2 = requests.get(url).text.split('viewerThumb:"')[1:]
                self.imagelist2 = [x.split('.jpg')[0] + '.jpg' for x in self.imagelist2]
                self.imagelist2 = [x for x in self.imagelist2 if 'lensThumb' not in x]
            webimage1 = request.urlopen(random.choice(self.imagelist1)).read()
            webimage2 = request.urlopen(random.choice(self.imagelist2)).read()
            self.windowQ.put((ui_num['풍경사진'], webimage1, webimage2))
        except:
            pass

    @thread_decorator
    def GugyCrawling(self, code):
        url    = f'https://finance.naver.com/item/coinfo.nhn?code={code}'
        source = requests.get(url).text
        html   = BeautifulSoup(source, 'lxml')
        gugy_result = ''
        titles = html.select('.summary_info > p')
        for title in titles:
            title = title.get_text().replace('.', '. ')
            if title != '':
                gugy_result += title
        self.windowQ.put((ui_num['기업개요'], gugy_result))

    @thread_decorator
    def GugsCrawling(self, code):
        date_list, jbjg_list, gygs_list, link_list = [], [], [], []
        for i in (1, 2):
            url    = f'https://finance.naver.com/item/news_notice.nhn?code={code}&page={i}'
            source = requests.get(url).text
            html   = BeautifulSoup(source, 'lxml')
            dates  = html.select('.date')
            if len(dates) != 0:
                date_list += [date.get_text() for date in dates]
                infos      = html.select('.info')
                jbjg_list += [info.get_text() for info in infos]
                titles     = html.select('.title')
                for title in titles:
                    try:
                        link_list.append('https://finance.naver.com' + title.find('a')['href'])
                        title = title.get_text().strip()
                        if title != '':
                            gygs_list.append(title)
                    except:
                        pass
        df = pd.DataFrame({'일자': date_list, '정보제공': jbjg_list, '공시': gygs_list, '링크': link_list})
        self.windowQ.put((ui_num['기업공시'], df))

    @thread_decorator
    def JmnsCrawling(self, code):
        date_list, title_list, ulsa_list, link_list = [], [], [], []
        for i in (1, 2):
            url    = f'https://finance.naver.com/item/news_news.nhn?code={code}&page={i}'
            source = requests.get(url).text
            html   = BeautifulSoup(source, 'lxml')
            dates  = html.select('.date')
            if len(dates) != 0:
                date_list += [date.get_text() for date in dates]
                infos      = html.select('.info')
                ulsa_list += [info.get_text() for info in infos]
                titles     = html.select('.title')
                for title in titles:
                    try:
                        link_list.append('https://finance.naver.com' + title.find('a')['href'])
                        title = title.get_text().strip()
                        if title != '':
                            title_list.append(title)
                    except:
                        pass
        df = pd.DataFrame({'일자 및 시간': date_list, '언론사': ulsa_list, '제목': title_list, '링크': link_list})
        self.windowQ.put((ui_num['기업뉴스'], df))

    @thread_decorator
    def JmjpCrawling(self, code):
        url      = f'https://finance.naver.com/item/main.nhn?code={code}'
        source   = requests.get(url).text
        html     = BeautifulSoup(source, 'lxml').select('div.section.cop_analysis div.sub_section')[0]
        txt_list = [item.get_text().strip() for item in html.select('th')]
        num_list = [item.get_text().strip() for item in html.select('td')][:130]
        columns1 = ['구분'] + txt_list[3:7]
        columns2 = txt_list[7:13]
        data1    = [txt_list[-16:-3], [num_list[j] for j in range(0, 130, 10)], [num_list[j] for j in range(1, 130, 10)], [num_list[j] for j in range(2, 130, 10)], [num_list[j] for j in range(3, 130, 10)]]
        data2    = [[num_list[j] for j in range(4, 130, 10)], [num_list[j] for j in range(5, 130, 10)], [num_list[j] for j in range(6, 130, 10)], [num_list[j] for j in range(7, 130, 10)], [num_list[j] for j in range(8, 130, 10)], [num_list[j] for j in range(9, 130, 10)]]
        df1      = pd.DataFrame(dict(zip(columns1, data1)))
        df2      = pd.DataFrame(dict(zip(columns2, data2)))
        self.windowQ.put((ui_num['재무년도'], df1))
        self.windowQ.put((ui_num['재무분기'], df2))

    @thread_decorator
    def UjTmCrawling(self):
        url        = 'https://finance.naver.com/sise/sise_group.naver?type=upjong'
        source     = requests.get(url).text
        html       = BeautifulSoup(source, 'lxml')
        url_list1  = ['https://finance.naver.com' + item['href'] for item in html.select('td > a')]
        name_list1 = [item.get_text().strip() for item in html.select('td > a')]
        per_list1  = [float(item.get_text().strip().replace('%', '')) for item in html.select('.number > span')]

        url        = 'https://finance.naver.com/sise/theme.naver?&page=1'
        source     = requests.get(url).text
        html       = BeautifulSoup(source, 'lxml')
        url_list2  = ['https://finance.naver.com' + item['href'] for item in html.select('.col_type1 > a')[1:]]
        name_list2 = [item.get_text().strip() for item in html.select('.col_type1 > a')[1:]]
        per_list2  = [float(item.get_text().strip().replace('%', '')) for item in html.select('.col_type2 > span')]

        df1 = pd.DataFrame({'업종명': name_list1[:len(per_list1)], '등락율': per_list1, 'url': url_list1[:len(per_list1)]})
        df1 = df1[df1['등락율'] > 0]
        if len(df1) > 30:
            df1 = df1[:30]
        df1['등락율%'] = df1['등락율'].apply(lambda x: str(x) + '%')
        minimum = df1['등락율'].min()
        maximum = df1['등락율'].max()
        df1['컬러맵'] = df1['등락율'].apply(lambda x: abs(x - maximum))
        maximum += (maximum - minimum) * 5
        norm1 = matplotlib.colors.Normalize(vmin=minimum, vmax=maximum)
        cl1 = [self.cmap(norm1(value)) for value in df1['컬러맵']]

        df2 = pd.DataFrame({'테마명': name_list2[:len(per_list2)], '등락율': per_list2, 'url': url_list2[:len(per_list2)]})
        df2 = df2[df2['등락율'] > 0]
        if len(df2) > 30:
            df2 = df2[:30]
        df2['등락율%'] = df2['등락율'].apply(lambda x: str(x) + '%')
        minimum = df2['등락율'].min()
        maximum = df2['등락율'].max()
        df2['컬러맵'] = df2['등락율'].apply(lambda x: abs(x - maximum))
        maximum += (maximum - minimum) * 5
        norm2 = matplotlib.colors.Normalize(vmin=minimum, vmax=maximum)
        cl2 = [self.cmap(norm2(value)) for value in df2['컬러맵']]

        self.windowQ.put((ui_num['트리맵'], df1, df2, cl1, cl2))
        if self.treemap:
            Timer(10, self.UjTmCrawling).start()

    @thread_decorator
    def UjTmCrawlingDetail(self, url, gubun):
        source    = requests.get(url).text
        html      = BeautifulSoup(source, 'lxml')
        name_list = [item.get_text().strip() for item in html.select('.name_area')]
        per_list  = [float(item.get_text().strip().replace('%', '')) for i, item in enumerate(html.select('.number > span')[1:]) if i % 2 != 0]

        df = pd.DataFrame({'종목명': name_list[:len(per_list)], '등락율': per_list})
        df = df[df['등락율'] > 0][:20]
        df['등락율%'] = df['등락율'].apply(lambda x: f'{x}%')
        minimum, maximum = df['등락율'].min(), df['등락율'].max()
        df['컬러맵'] = df['등락율'].apply(lambda x: abs(x - maximum))
        maximum += (maximum - minimum) * 5
        norm = matplotlib.colors.Normalize(vmin=minimum, vmax=maximum)
        color_list = [self.cmap(norm(value)) for value in df['컬러맵']]

        if gubun == 1:
            self.windowQ.put((ui_num['트리맵1'], df, '', color_list, ''))
        else:
            self.windowQ.put((ui_num['트리맵2'], '', df, '', color_list))

    @thread_decorator
    def JisuCrawling(self, startday):
        self.windowQ.put((ui_num['백테엔진'], '지수차트 웹크롤링 시작'))

        def crawl_index(code):
            page = 1
            df   = []
            while True:
                url        = f'https://finance.naver.com/sise/sise_index_day.nhn?code={code}&page={page}'
                source     = requests.get(url).text
                html       = BeautifulSoup(source, 'lxml')
                day_list   = [item.get_text().replace('.', '') for item in html.select('.date')]
                close_list = [float(item.get_text().replace(',', '')) for i, item in enumerate(html.select('.number_1')) if i % 4 == 0]
                df.append(pd.DataFrame(dict(zip(['index', '종가'], [day_list, close_list]))))
                page += 1
                if int(day_list[-1]) < startday:
                    break
            df = pd.concat(df)
            df = df[df['index'] >= str(startday)][::-1]
            return df

        df_kp = crawl_index('KOSPI')
        df_kd = crawl_index('KOSDAQ')
        self.windowQ.put((ui_num['백테엔진'], '코스피 지수차트 웹크롤링 완료'))
        self.windowQ.put((ui_num['백테엔진'], '코스닥 지수차트 웹크롤링 완료'))
        self.backQ.put((df_kp, df_kd))
