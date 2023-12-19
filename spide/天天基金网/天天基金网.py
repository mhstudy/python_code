# -*- coding: utf-8 -*-
import csv
import json
import datetime
import requests
from bs4 import BeautifulSoup


# 天天基金网 https://fund.eastmoney.com/
class EastMoneySpider:
    def __init__(self, timeout=10, proxies=None):
        """
        初始化 EastMoneySpider 对象。

        Args:
            timeout (int, optional): 请求超时时间，单位为秒。默认为 10。
            proxies (dict, optional): 代理服务器设置。默认为 None。
        """
        # 设置默认请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        }
        # 创建 requests.Session 对象
        self.session = requests.Session()
        # 更新默认请求头和 session 的请求头
        self.session.headers.update(self.headers)
        # 设置超时时间
        self.session.timeout = timeout
        # 设置代理服务器
        self.session.proxies = proxies

    # 基金排行
    def fund_rank(self, ft='all', sd=None, ed=None, pi=1, pn=50):
        """
        :param ft: all:全部 gp:股票型 hh:混合型 zq:债券型 zs:指数型 qdii:QDII fof:FOF
        :param sd: 结束时间。默认为当天
        :param ed: 开始时间。默认为去年这天
        :return: 基金排名信息字典
        """
        url = 'http://fund.eastmoney.com/data/rankhandler.aspx'
        # 没有值 则获取当天时间
        if ed is None:
            ed = datetime.datetime.now().strftime("%Y-%m-%d")
            ed_dt = datetime.datetime.strptime(ed, "%Y-%m-%d")  # 将字符串转换为 datetime 对象
            sd_dt = ed_dt - datetime.timedelta(days=365)  # 计算一年前的日期
            sd = sd_dt.strftime("%Y-%m-%d")  # 将 datetime 对象转换为字符串

        params = {
            'op': 'ph',
            'dt': 'kf',
            'ft': ft,
            'rs': '',
            'gs': '0',
            'sc': '1nzf',
            'st': 'desc',
            'sd': sd,
            'ed': ed,
            'qdii': '',
            'tabSubtype': ',,,,,',
            'pi': pi,
            'pn': pn,
            'dx': '1',
            'v': '0.8993439077155316',
        }
        response = self.session.get(url=url, params=params)
        response.encoding = response.apparent_encoding

        str1 = response.text

        datas_list = json.loads(str1[str1.index('['):str1.rindex(']') + 1])

        fund_list = []
        for data in datas_list:
            fund_details = data.split(',')
            fund_dict = {
                '取数日期': ed,
                '日期': fund_details[3],
                '基金代码': fund_details[0],
                '基金简称': fund_details[1],
                '英文代码': fund_details[2],
                '单位净值': fund_details[4],
                '累计净值': fund_details[5],
                '日增长率': fund_details[6] + '%' if fund_details[6] != '' else '',
                '近1周': fund_details[7] + '%' if fund_details[7] != '' else '',
                '近1月': fund_details[8] + '%' if fund_details[8] != '' else '',
                '近3月': fund_details[9] + '%' if fund_details[9] != '' else '',
                '近6月': fund_details[10] + '%' if fund_details[10] != '' else '',
                '近1年': fund_details[11] + '%' if fund_details[11] != '' else '',
                '近2年': fund_details[12] + '%' if fund_details[12] != '' else '',
                '近3年': fund_details[13] + '%' if fund_details[13] != '' else '',
                '近5年': fund_details[24] + '%' if fund_details[24] != '' else '',
                '今年来': fund_details[14] + '%' if fund_details[14] != '' else '',
                '成立来': fund_details[15] + '%' if fund_details[15] != '' else '',
                '成立日期': fund_details[16],
                # '1': fund_details[17],
                f'{sd}到{ed}': fund_details[18] + '%' if fund_details[15] != '' else '',
                '购买手续费': fund_details[19],
                '购买手续费1折': fund_details[20],
                # '1': fund_details[21],
                # '购买手续费1折': fund_details[22],
                # '1': fund_details[23],

            }
            fund_list.append(fund_dict)
        return fund_list

    # 基金净值
    def jjjz(self, fund_code, pageIndex=1, pageSize=30):
        """
        查询单个基金的历史净值信息
        :param fund_code: 基金代码
        :param pageIndex: 页码
        :param pageSize: 每页大小
        :return: 基金历史净值
        """
        url = 'http://api.fund.eastmoney.com/f10/lsjz'
        params = {
            'fundCode': fund_code,
            'pageIndex': pageIndex,
            'pageSize': pageSize,
        }
        response = self.session.get(url, params=params)
        str1 = response.text
        datas_list = json.loads(str1[str1.index('['):str1.rindex(']') + 1])

        fund_networth = []
        for data in datas_list:
            data_dict = {
                '净值日期': data['FSRQ'],
                '单位净值': data['DWJZ'],
                '累计净值': data['LJJZ'],
                '日增长率': data['JZZZL'] + '%' if data['JZZZL'] != '' else '',
            }
            fund_networth.append(data_dict)

        return fund_networth

    # 基金代码查询基金名称
    def fundcode_search(self, fund_code):
        url = 'http://fund.eastmoney.com/js/fundcode_search.js'
        response = self.session.get(url)
        response.encoding = response.apparent_encoding

        str1 = response.text
        # 所有基金信息
        datas_list = json.loads(str1[str1.index('['):str1.rindex(']') + 1])

        fund_data = []

        for datas in datas_list:
            datas_dic = {
                "基金代码": datas[0],
                "基金名称": datas[2],
                "基金类型": datas[3],
            }
            fund_data.append(datas_dic)

        # 遍历列表
        for item in fund_data:
            if fund_code == int(item["基金代码"]):
                # 找到了对应的字典，输出信息
                print(item)
                break  # 可以加上 break 语句，找到第一个就不再继续查找了


class DataUtils:
    @staticmethod
    def write_to_csv(dict_list, file_name='test.csv', mode='w'):
        """
        将字典列表写入 CSV 文件。

        Args:
            dict_list (List[Dict[str, Any]]): 包含要写入的数据的字典列表。
            file_name (str): CSV 文件路径。默认为 'test.csv'。
            mode (str): 写入模式。默认为写入模式（'w'），也可以指定为追加模式（'a'）。
        """
        # 获取字典列表中第一个字典的键名列表
        keys = dict_list[0].keys()

        # 打开指定的 CSV 文件，指定写入模式和换行符参数
        with open(file_name, mode=mode, encoding='utf-8', newline='') as csv_file:
            # 创建一个 DictWriter 对象，指定字段名为 keys
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            if mode == 'w':
                # 写入 CSV 文件的表头（即字段名）
                writer.writeheader()
            # 遍历字典列表中的每个字典，将其写入 CSV 文件
            for row in dict_list:
                writer.writerow(row)


if __name__ == '__main__':
    east_money = EastMoneySpider()

    result_list_dic = []
    for pi in range(1, 274 + 1):
        fund_rank_data = east_money.fund_rank(pi=pi)
        result_list_dic.extend(fund_rank_data)

    DataUtils.write_to_csv(result_list_dic, file_name=result_list_dic[0]["取数日期"] + '基金排行.csv', mode='w')

    # EastMoneySpider.fundcode_search(fund_code=162102)

    # fund_networth = east_money.jjjz('161725')
    # DataUtils.write_to_csv(fund_networth, file_name='基金历史净值.csv', mode='w')

    pass
