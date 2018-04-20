#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@auth: alcorzheng<alcor.zheng@gmail.com>
@file: datamodels.py
@time: 2018/4/1816:42
@desc: 赛思BI数据模型（事实表维表）爬取工具，支持下钻目录
@func: 
"""

from requests_html import HTMLSession
import xlsxwriter


class SpiderConf:
    szbi_host = "http://172.16.4.242"
    szbi_srvname = "bidevp"
    szbi_user = "zhengx"
    szbi_password = "top@1018"
    szbi_projectname = "TOPSYJDSJFX"
    szbi_customurl = "FACT"
    out_filepath = r'E:\湖北数据处理中心\98.个人目录\郑雄\食药大数据\ '
    out_factexeclname = '事实表模型整理.xls'
    out_dimexeclname = '维表模型整理.xls'


class SpiderBIDM:
    def __init__(self, session):
        self.session = session
        self.factexecl = None
        self.dimexecl = None

    def spider_model(self, page_url, drilllevel):
        """"爬取事实表维表清单"""
        ml_response = self.session.get(page_url)
        ml_content = ml_response.html.find('div.sz-commons-simplelist-content', first=True)
        md_list = ml_content.find('tr.sz-commons-simplelist-tr')
        for md in md_list:
            md_url = md.find('td:nth-of-type(2)', first=True).find('a', first=True).attrs['href']
            md_name = md.find('td:nth-of-type(2)', first=True).text.strip()
            md_code = md.find('td:nth-of-type(3)', first=True).text.strip()
            md_code = md_code[:md_code.index('\n')]
            md_type = md.find('td:nth-of-type(4)', first=True).text.strip()
            if md_type == '目录' and drilllevel != 0:
                self.spider_model(SpiderConf.szbi_host + md_url, drilllevel - 1)
            elif md_type == '事实表':
                self.spider_factcontent(md_code, md_name, SpiderConf.szbi_host + md_url)
            elif md_type == '维表':
                self.spider_dimcontent(md_code, md_name, SpiderConf.szbi_host + md_url)
            else:
                pass
        if self.factexecl is not None:
            self.factexecl.close()
        if self.dimexecl is not None:
            self.dimexecl.close()

    def spider_mdproperties(self, properties_url):
        """爬取事实表维表对应的物理表名称"""
        mdp_response = self.session.get(properties_url)
        properties = dict()
        properties['tblname'] = mdp_response.html.find('input#dbtable-resinput', first=True).attrs['value']
        tblname_path = mdp_response.html.find('input#dbtable-resinput', first=True).attrs['title']
        tblname_path = tblname_path[tblname_path.index('/') + 1:]
        tblname_path = tblname_path[:tblname_path.index('/')] + ':' + tblname_path[tblname_path.index('/') + 1:]
        properties['tblname_path'] = tblname_path
        properties['tblname_full'] = properties['tblname'] + '(' + properties['tblname_path'] + ')'
        return properties

    def spider_dimcontent(self, dim_code, dim_name, dim_url):
        """爬取维表内容"""
        if self.factexecl is None:
            self.factexecl = DMExecl(SpiderConf.out_filepath.strip() + SpiderConf.out_dimexeclname.strip(), 'FACT')
        print("")

    def spider_factcontent(self, fact_code, fact_name, fact_url):
        """"爬取事实表内容"""
        if self.dimexecl is None:
            self.dimexecl = DMExecl(SpiderConf.out_filepath.strip() + SpiderConf.out_factexeclname.strip(), 'DIM')
        fact_response = self.session.get(fact_url)
        fact_content = fact_response.html.find('div.sz-commons-simplelist-content', first=True)
        properties_path = fact_response.html.find('li#properties', first=True).find('a', first=True).attrs['href']
        fact_properties = self.spider_mdproperties(self.get_url(properties_path))
        column_list = fact_content.find('tr.sz-commons-simplelist-tr')
        dmsheet = DMSheet(self.factexecl, 'FACT', fact_name, fact_code, fact_properties)
        for column in column_list:
            code_ = column.find('td:nth-of-type(2)', first=True).text.strip()
            name_ = column.find('td:nth-of-type(3)', first=True).text.strip()
            type_bdim = ''
            type_bmeasure = ''
            if column.find('span.sz-bi-dw-icons-dim', first=True) is not None:
                type_bdim = '√'
            elif column.find('span.sz-bi-dw-icons-vdim', first=True) is not None:
                type_bdim = '虚拟'
            if column.find('span.sz-bi-dw-icons-measure', first=True) is not None:
                type_bmeasure = '√'
            elif column.find('span.sz-bi-dw-icons-vmeasure', first=True) is not None:
                type_bmeasure = '虚拟'
            filed_ = column.find('td:nth-of-type(4)', first=True).text.strip()
            dbtype_ = column.find('td:nth-of-type(6)', first=True).text.strip()
            dim_obj = column.find('td:nth-of-type(8)', first=True).find('a', first=True)
            dim_name = dim_obj.text.strip() if dim_obj is not None else ''
            dim_path = dim_obj.attrs['path'] if dim_obj is not None else ''
            dim_url = self.get_url(dim_obj.attrs['href']) if dim_obj is not None else ''
            dmsheet.writecontent(code_,
                                 name_,
                                 filed_,
                                 dbtype_,
                                 type_bdim,
                                 type_bmeasure,
                                 dim_name,
                                 [dim_path, dim_url],
                                 ''
                                 )
        self.factexecl.addindexsheet('',
                                     [fact_name, "internal:'" + fact_name + "'!A1"],
                                     [self.get_biurl(fact_url[fact_url.find('/datamodels'):]), fact_url],
                                     fact_properties['tblname'],
                                     fact_properties['tblname_path'],
                                     '')

    @staticmethod
    def get_url(path):
        return SpiderConf.szbi_host + path

    @staticmethod
    def get_biurl(path):
        return SpiderConf.szbi_projectname + ':' + path

    @staticmethod
    def get_szbimodelurl():
        """获取赛思BI模型界面URL"""
        mdurl = SpiderConf.szbi_host
        mdurl = mdurl + '/' + SpiderConf.szbi_srvname
        mdurl = mdurl + '/meta/' + SpiderConf.szbi_projectname
        mdurl = mdurl + '/datamodels'
        if SpiderConf.szbi_customurl is not None:
            mdurl = mdurl + '/' + SpiderConf.szbi_customurl
        mdverifyurlparam = 'user=' + SpiderConf.szbi_user + '&password=' + SpiderConf.szbi_password
        if SpiderConf.szbi_customurl is not None and SpiderConf.szbi_customurl.find('?') >= 0:
            mdurl = mdurl + '&' + mdverifyurlparam
        else:
            mdurl = mdurl + '?' + mdverifyurlparam
        return mdurl


class DMExecl:
    """模型Execl页对象"""
    def __init__(self, filepath, execltype):
        self.filepath = filepath
        self.execltype = execltype
        self.execlbook = xlsxwriter.Workbook(filepath)
        self.content_rowidx = 0
        if execltype == 'FACT':
            self.__init_factexecl__()

    def __init_factexecl__(self):
        # 定义样式表
        self.style_title_center = self.execlbook.add_format(
            {'bold': True, 'border': 1, 'align': 'center', 'font_size': 12})
        self.style_title_left = self.execlbook.add_format(
            {'bold': True, 'border': 1, 'align': 'left', 'font_size': 12})
        self.style_title_right = self.execlbook.add_format(
            {'bold': True, 'border': 1, 'align': 'right', 'font_size': 12})
        self.style_content_center = self.execlbook.add_format(
            {'border': 1, 'align': 'center', 'font_size': 11})
        self.style_content_left = self.execlbook.add_format(
            {'border': 1, 'align': 'left', 'font_size': 11})
        self.style_content_right = self.execlbook.add_format(
            {'border': 1, 'align': 'right', 'font_size': 11})
        # 创建主页面
        self.indexsheet = self.execlbook.add_worksheet('事实表汇总')
        self.__init_factindexsheet__()

    def __init_dimexecl__(self):
        self.__init_factindexsheet__()

    def __init_factindexsheet__(self):
        self.indexsheet.set_column(0, 0, 15, self.style_content_left)
        self.indexsheet.set_column(1, 1, 20, self.style_content_left)
        self.indexsheet.set_column(2, 2, 45, self.style_content_left)
        self.indexsheet.set_column(3, 3, 20, self.style_content_left)
        self.indexsheet.set_column(4, 4, 20, self.style_content_left)
        self.indexsheet.set_column(5, 5, 20, self.style_content_left)
        self.indexsheet.write(0, 0, '模块', self.style_title_center)
        self.indexsheet.write(0, 1, '事实表名称', self.style_title_center)
        self.indexsheet.write(0, 2, '事实表路径', self.style_title_center)
        self.indexsheet.write(0, 3, '物理表', self.style_title_center)
        self.indexsheet.write(0, 4, '物理表路径', self.style_title_center)
        self.indexsheet.write(0, 5, '说明', self.style_title_center)
        self.content_rowidx = 1

    def addindexsheet(self, *args):
        colnum = 0
        for obj in args:
            if isinstance(obj, list):
                self.indexsheet.write_url(
                    self.content_rowidx, colnum, obj[1], self.style_content_left, obj[0])
            else:
                self.indexsheet.write(self.content_rowidx, colnum, obj)
            colnum = colnum + 1
        self.content_rowidx = self.content_rowidx + 1

    def close(self):
        if self.execlbook is not None:
            self.execlbook.close()


class DMSheet:
    """模型Sheet页对象"""
    def __init__(self, dmexecl, sheettype, obj_name, obj_code, obj_properties):
        self.dmexecl = dmexecl
        self.sheettype = sheettype
        self.obj_name = obj_name
        self.obj_code = obj_code
        self.obj_properties = obj_properties
        self.sheet = self.dmexecl.execlbook.add_worksheet(obj_name)
        self.content_rowidx = 0
        if sheettype == 'FACT':
            self.__init_column_style_fact__()
            self.__init_writetitle_fact__()
        elif sheettype == 'DIM':
            self.__init_column_style_dim__()
            self.__init_writetitle_dim__()
        else:
            pass

    def __init_writetitle_fact__(self):
        """写表头"""
        # 第一行
        self.sheet.merge_range(0, 0, 0, 8, self.obj_name, self.dmexecl.style_title_center)
        # 第二行
        self.sheet.write(1, 0, '编码', self.dmexecl.style_title_center)
        self.sheet.merge_range(1, 1, 1, 2, self.obj_code, self.dmexecl.style_title_center)
        self.sheet.write(1, 3, '物理表', self.dmexecl.style_title_center)
        self.sheet.merge_range(1, 4, 1, 8, self.obj_properties['tblname_full'], self.dmexecl.style_title_left)
        self.sheet.write_url(1, 4,
                             "internal:'事实表汇总'!B" + str(self.dmexecl.content_rowidx + 1),
                             self.dmexecl.style_title_left,
                             self.obj_properties['tblname_full'])
        # 第三行
        self.sheet.write(2, 0, '名称', self.dmexecl.style_title_center)
        self.sheet.write(2, 1, '标题', self.dmexecl.style_title_center)
        self.sheet.write(2, 2, '字段', self.dmexecl.style_title_center)
        self.sheet.write(2, 3, '类型', self.dmexecl.style_title_center)
        self.sheet.write(2, 4, '维键', self.dmexecl.style_title_center)
        self.sheet.write(2, 5, '度量', self.dmexecl.style_title_center)
        self.sheet.write(2, 6, '维表', self.dmexecl.style_title_center)
        self.sheet.write(2, 7, '维表路径', self.dmexecl.style_title_center)
        self.sheet.write(2, 8, '备注', self.dmexecl.style_title_center)
        self.content_rowidx = 3

    def __init_writetitle_dim__(self):
        """写表头"""

    def __init_column_style_fact__(self):
        """定义列宽"""
        self.sheet.set_column(0, 0, 15, self.dmexecl.style_content_left)
        self.sheet.set_column(1, 1, 20, self.dmexecl.style_content_left)
        self.sheet.set_column(2, 2, 20, self.dmexecl.style_content_left)
        self.sheet.set_column(3, 3, 15, self.dmexecl.style_content_left)
        self.sheet.set_column(4, 4, 5, self.dmexecl.style_content_center)
        self.sheet.set_column(5, 5, 5, self.dmexecl.style_content_center)
        self.sheet.set_column(6, 6, 15, self.dmexecl.style_content_left)
        self.sheet.set_column(7, 7, 15, self.dmexecl.style_content_left)
        self.sheet.set_column(8, 8, 30, self.dmexecl.style_content_left)

    def __init_column_style_dim__(self):
        """定义列宽"""

    def writecontent(self, *args):
        """写内容"""
        colnum = 0
        for obj in args:
            if isinstance(obj, list):
                self.sheet.write_url(
                    self.content_rowidx, colnum, obj[1], self.dmexecl.style_content_left, obj[0])
            else:
                self.sheet.write(self.content_rowidx, colnum, obj)
            colnum = colnum + 1
        self.content_rowidx = self.content_rowidx + 1


if __name__ == '__main__':
    spiderdm = SpiderBIDM(HTMLSession())
    spiderdm.spider_model(spiderdm.get_szbimodelurl(), 0)
