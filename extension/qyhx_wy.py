import traceback
import numpy as np
import pandas as pd
import json
import pymysql as sql
import re
import sys
from copy import copy
from decimal import Decimal

# sql.install_as_MySQLdb()

class PortraitCal_class():
    def __init__(self):
        self.sum_zd_list = [
            ('sumqh40_rd', 'qd01', 'sumqh51_rd', 'qc05_0', 'qj57', 'qj56', 'qc05_0_gf', 'qd08', 'qd18', 'qj80',
             'sn_qc05_0', 'qc12', 'qb11num', 'sn_qb11num', 'qc226_qy', 'qj73', 'qj79', 'qz001', 'qc02', 'qc05_0_qt',
             'qc41_gy', 'qz001_gy', 'sn_qd01', 'qc51', 'qj90_qy', 'qj33_1', 'qj33_2', 'qj33_3', 'qj33_4', 'qj59',
             'qj61', 'qj79_2_qy', 'qj57_2_qy', 'qj98_1_qy', 'qc11_1', 'qc11', 'qc11_gq', 'qd25', 'qd03', 'sn_qz001',
             'qc05_0_rd5', 'qc05_0_sz', 'qb15_xssqy', 'qc05_rd5'),
            ('q1_2', 'q1_3', 'q1_4', 'q1_5', 'q2_1', 'q2_2', 'q2_3', 'q2_4', 'q2_5', 'q2_6', 'q2_7', 'q2_8', 'q2_9',
             'q3_1', 'q3_5', 'q3_6', 'q4_1', 'q4_2', 'q4_3', 'q4_4', 'q4_5', 'q4_6', 'q4_7', 'q5_2', 'q5_3', 'q5_4',
             'q5_6', 'q5_7')]
        self.zb_js_list = [
            (['q1_2jqdf', 'q1_3jqdf', 'q1_4jqdf', 'q1_5jqdf'], 'q1_yjzb'), (
                ['q2_1jqdf', 'q2_2jqdf', 'q2_3jqdf', 'q2_4jqdf', 'q2_5jqdf', 'q2_6jqdf', 'q2_7jqdf', 'q2_8jqdf',
                 'q2_9jqdf'], 'q2_yjzb'), (['q3_1jqdf', 'q3_5jqdf', 'q3_6jqdf'], 'q3_yjzb'),
            (['q4_1jqdf', 'q4_2jqdf', 'q4_3jqdf', 'q4_4jqdf', 'q4_5jqdf', 'q4_6jqdf', 'q4_7jqdf'], 'q4_yjzb'),
            (['q5_2jqdf', 'q5_3jqdf', 'q5_4jqdf', 'q5_6jqdf', 'q5_7jqdf'], 'q5_yjzb'),
            (['q1_yjzb', 'q2_yjzb', 'q3_yjzb', 'q4_yjzb', 'q5_yjzb'], 'q0_zhdf'), (['q1_3jqdf'], 'q91_yjzb'),
            (['q2_1jqdf', 'q2_2jqdf', 'q2_4jqdf', 'q2_6jqdf', 'q2_8jqdf', 'q2_9jqdf'], 'q92_yjzb'),
            (['q3_6jqdf'], 'q93_yjzb'), (['q5_2jqdf', 'q5_3jqdf', 'q5_4jqdf', 'q5_7jqdf'], 'q95_yjzb'),
            (['q91_yjzb', 'q92_yjzb', 'q93_yjzb', 'q95_yjzb'], 'q90_zhdf')]
        self.gjc_list = []
        self.sum_dict = {'__builtins__': {}}
        self.title_gs_dict = {}
        self.db_fx_dict = {
            'q1_2': '“1.2从业人员中研发人员全时当量数占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q1_3': '“1.3研发经费内部支出占营业收入比例”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q1_4': '“1.4每万人当年发明专利授权数”{:.2f}件，低于总体水平{:.2f}件。；',
            'q1_5': '“1.5当年每千万研发经费支出的发明专利申请数”{:.2f}件，低于总体水平{:.2f}件。；',
            'q2_1': '“2.1营业收入中高技术服务业营收占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q2_2': '“2.2从业人员中本科及以上学历者人员占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q2_3': '“2.3人均技术合同成交额”{:.2f}万元，低于总体水平{:.2f}万元。；', 'q2_4': '“2.4当年净增营业收入”{:.2f}亿元。；',
            'q2_5': '“2.5企业利润率”{:.2f}%，低于总体水平{:.2f}个百分点。；', 'q2_6': '“2.6当年净增高新技术企业数”{:.0f}家。；',
            'q2_7': '“2.7当年获得风险投资的企业数”0家。；', 'q2_8': '“2.8每100亿元营业收入所含有效发明专利数和注册商标数”{:.2f}件，低于总体水平{:.2f}件。；',
            'q2_9': '“2.9企业增加值率”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q3_1': '“3.1单位增加值综合能耗”{:.2f}吨标准煤/万元，高于总体水平{:.2f}吨标准煤/万元。；', 'q3_5': '“3.5当年净增从业人员数”{:.2f}万人。；',
            'q3_6': '“3.6单位增加值中从业人员工资性收入占比”{:.2f}%，低于总体水平{:.2f}个百分点。；', 'q4_1': '“4.1设立境外研发机构的内资控股企业数”{:.0f}家。；',
            'q4_2': '“4.2企业引进技术、消化吸收再创新和境内外产学研合作经费支出额占营业收入比例”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q4_3': '“4.3当年获得境外注册商标或境外发明专利授权的内资控股企业数”{:.0f}家。；', 'q4_4': '“4.4当年新增主导制定国际标准的内资控股企业数”{:.2f}项。；',
            'q4_5': '“4.5出口总额中技术服务出口占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q4_6': '“4.6营业收入中高新技术企业出口额占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q4_7': '“4.7从业人员中外籍常驻人员和留学归国人员占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q5_2': '“5.2全员劳动生产率的增长率”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q5_3': '“5.3营业收入中内部研发投入强度达5%企业的营收合计占比”{:.2f}%，低于总体水平{:.2f}个百分点。；',
            'q5_4': '“5.4营业收入中数字产业相关企业营收合计占比”{:.2f}%，低于总体水平{:.2f}个百分点。；', 'q5_6': '“5.6当年在境内、外上市（不含新三板）企业数”{:.0f}家。；',
            'q5_7': '“5.7当年内部研发投入强度达5%且营业收入超5亿元的企业数”{:.0f}家。；'}
        self.cre_sql = 'CREATE TABLE `portrait_{0}_sc` (`susername` varchar(32) NULL,`sname` varchar(255) NULL,`sbelongwhere` varchar(32) NULL,`library` varchar(16) NULL,`issta` varchar(16) NULL,`yhbz` mediumtext NULL,`q0_zhdf` decimal(24, 6) NULL,`q1_yjzb` decimal(24, 6) NULL,`q2_yjzb` decimal(24, 6) NULL,`q3_yjzb` decimal(24, 6) NULL,`q4_yjzb` decimal(24, 6) NULL,`q5_yjzb` decimal(24, 6) NULL,`q0_dbxs` int NULL,`q0_dbfx` mediumtext NULL,`q90_zhdf` decimal(24, 4) NULL,`q91_yjzb` decimal(24, 6) NULL,`q92_yjzb` decimal(24, 6) NULL,`q93_yjzb` decimal(24, 6) NULL,`q95_yjzb` decimal(24, 6) NULL,`q90_dbxs` decimal(24, 4) NULL,`q90_dbfx` mediumtext NULL,`sumqh40_rd` decimal(24, 4) NULL,`qd01` decimal(24, 4) NULL,`q1_2hsz` decimal(24, 4) NULL,`q1_2gxz` decimal(24, 4) NULL,`q1_2gxl` decimal(24, 4) NULL,`q1_2jqdf` decimal(24, 4) NULL,`sumqh51_rd` decimal(24, 4) NULL,`qc05_0` decimal(24, 4) NULL,`q1_3hsz` decimal(24, 4) NULL,`q1_3gxz` decimal(24, 4) NULL,`q1_3gxl` decimal(24, 4) NULL,`q1_3jqdf` decimal(24, 4) NULL,`qj57` decimal(24, 4) NULL,`q1_4hsz` decimal(24, 4) NULL,`q1_4gxz` decimal(24, 4) NULL,`q1_4gxl` decimal(24, 4) NULL,`q1_4jqdf` decimal(24, 4) NULL,`qj56` decimal(24, 4) NULL,`q1_5hsz` decimal(24, 4) NULL,`q1_5gxz` decimal(24, 4) NULL,`q1_5gxl` decimal(24, 4) NULL,`q1_5jqdf` decimal(24, 4) NULL,`qc05_0_gf` decimal(24, 4) NULL,`q2_1hsz` decimal(24, 4) NULL,`q2_1gxz` decimal(24, 4) NULL,`q2_1gxl` decimal(24, 4) NULL,`q2_1jqdf` decimal(24, 4) NULL,`qd08` decimal(24, 4) NULL,`qd18` decimal(24, 4) NULL,`q2_2hsz` decimal(24, 4) NULL,`q2_2gxz` decimal(24, 4) NULL,`q2_2gxl` decimal(24, 4) NULL,`q2_2jqdf` decimal(24, 4) NULL,`qj80` decimal(24, 4) NULL,`q2_3hsz` decimal(24, 4) NULL,`q2_3gxz` decimal(24, 4) NULL,`q2_3gxl` decimal(24, 4) NULL,`q2_3jqdf` decimal(24, 4) NULL,`sn_qc05_0` decimal(24, 4) NULL,`q2_4hsz` decimal(24, 4) NULL,`q2_4gxz` decimal(24, 4) NULL,`q2_4gxl` decimal(24, 4) NULL,`q2_4jqdf` decimal(24, 4) NULL,`qc12` decimal(24, 4) NULL,`q2_5hsz` decimal(24, 4) NULL,`q2_5gxz` decimal(24, 4) NULL,`q2_5gxl` decimal(24, 4) NULL,`q2_5jqdf` decimal(24, 4) NULL,`qb11num` decimal(24, 4) NULL,`sn_qb11num` decimal(24, 4) NULL,`q2_6hsz` decimal(24, 4) NULL,`q2_6gxz` decimal(24, 4) NULL,`q2_6gxl` decimal(24, 4) NULL,`q2_6jqdf` decimal(24, 4) NULL,`qc226_qy` decimal(24, 4) NULL,`q2_7hsz` decimal(24, 4) NULL,`q2_7gxz` decimal(24, 4) NULL,`q2_7gxl` decimal(24, 4) NULL,`q2_7jqdf` decimal(24, 4) NULL,`qj73` decimal(24, 4) NULL,`qj79` decimal(24, 4) NULL,`q2_8hsz` decimal(24, 4) NULL,`q2_8gxz` decimal(24, 4) NULL,`q2_8gxl` decimal(24, 4) NULL,`q2_8jqdf` decimal(24, 4) NULL,`qz001` decimal(24, 4) NULL,`qc02` decimal(24, 4) NULL,`qc05_0_qt` decimal(24, 4) NULL,`q2_9hsz` decimal(24, 4) NULL,`q2_9gxz` decimal(24, 4) NULL,`q2_9gxl` decimal(24, 4) NULL,`q2_9jqdf` decimal(24, 4) NULL,`qc41_gy` decimal(24, 4) NULL,`qz001_gy` decimal(24, 4) NULL,`q3_1hsz` decimal(24, 4) NULL,`q3_1gxz` decimal(24, 4) NULL,`q3_1gxl` decimal(24, 4) NULL,`q3_1jqdf` decimal(24, 4) NULL,`sn_qd01` decimal(24, 4) NULL,`q3_5hsz` decimal(24, 4) NULL,`q3_5gxz` decimal(24, 4) NULL,`q3_5gxl` decimal(24, 4) NULL,`q3_5jqdf` decimal(24, 4) NULL,`qc51` decimal(24, 4) NULL,`q3_6hsz` decimal(24, 4) NULL,`q3_6gxz` decimal(24, 4) NULL,`q3_6gxl` decimal(24, 4) NULL,`q3_6jqdf` decimal(24, 4) NULL,`qj90_qy` decimal(24, 4) NULL,`q4_1hsz` decimal(24, 4) NULL,`q4_1gxz` decimal(24, 4) NULL,`q4_1gxl` decimal(24, 4) NULL,`q4_1jqdf` decimal(24, 4) NULL,`qj33_1` decimal(24, 4) NULL,`qj33_2` decimal(24, 4) NULL,`qj33_3` decimal(24, 4) NULL,`qj33_4` decimal(24, 4) NULL,`qj59` decimal(24, 4) NULL,`qj61` decimal(24, 4) NULL,`q4_2hsz` decimal(24, 4) NULL,`q4_2gxz` decimal(24, 4) NULL,`q4_2gxl` decimal(24, 4) NULL,`q4_2jqdf` decimal(24, 4) NULL,`qj79_2_qy` decimal(24, 4) NULL,`qj57_2_qy` decimal(24, 4) NULL,`q4_3hsz` decimal(24, 4) NULL,`q4_3gxz` decimal(24, 4) NULL,`q4_3gxl` decimal(24, 4) NULL,`q4_3jqdf` decimal(24, 4) NULL,`qj98_1_qy` decimal(24, 4) NULL,`q4_4hsz` decimal(24, 4) NULL,`q4_4gxz` decimal(24, 4) NULL,`q4_4gxl` decimal(24, 4) NULL,`q4_4jqdf` decimal(24, 4) NULL,`qc11_1` decimal(24, 4) NULL,`qc11` decimal(24, 4) NULL,`q4_5hsz` decimal(24, 4) NULL,`q4_5gxz` decimal(24, 4) NULL,`q4_5gxl` decimal(24, 4) NULL,`q4_5jqdf` decimal(24, 4) NULL,`qc11_gq` decimal(24, 4) NULL,`q4_6hsz` decimal(24, 4) NULL,`q4_6gxz` decimal(24, 4) NULL,`q4_6gxl` decimal(24, 4) NULL,`q4_6jqdf` decimal(24, 4) NULL,`qd25` decimal(24, 4) NULL,`qd03` decimal(24, 4) NULL,`q4_7hsz` decimal(24, 4) NULL,`q4_7gxz` decimal(24, 4) NULL,`q4_7gxl` decimal(24, 4) NULL,`q4_7jqdf` decimal(24, 4) NULL,`sn_qz001` decimal(24, 4) NULL,`q5_2hsz` decimal(24, 4) NULL,`q5_2gxz` decimal(24, 4) NULL,`q5_2gxl` decimal(24, 4) NULL,`q5_2jqdf` decimal(24, 4) NULL,`qc05_0_rd5` decimal(24, 4) NULL,`q5_3hsz` decimal(24, 4) NULL,`q5_3gxz` decimal(24, 4) NULL,`q5_3gxl` decimal(24, 4) NULL,`q5_3jqdf` decimal(24, 4) NULL,`qc05_0_sz` decimal(24, 4) NULL,`q5_4hsz` decimal(24, 4) NULL,`q5_4gxz` decimal(24, 4) NULL,`q5_4gxl` decimal(24, 4) NULL,`q5_4jqdf` decimal(24, 4) NULL,`qb15_xssqy` decimal(24, 4) NULL,`q5_6hsz` decimal(24, 4) NULL,`q5_6gxz` decimal(24, 4) NULL,`q5_6gxl` decimal(24, 4) NULL,`q5_6jqdf` decimal(24, 4) NULL,`qc05_rd5` decimal(24, 4) NULL,`q5_7hsz` decimal(24, 4) NULL,`q5_7gxz` decimal(24, 4) NULL,`q5_7gxl` decimal(24, 4) NULL,`q5_7jqdf` decimal(24, 4) NULL,INDEX `susername`(`susername`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;'
        self.ins_sql = 'INSERT INTO `portrait_{0}_sc` VALUES {1};'
        self.tru_sql = 'truncate table `portrait_{0}_sc`;'
        self.ins_th_str = "('{susername}','{sname}','{sbelongwhere}','{library}','{issta}',NULL,{q0_zhdf},{q1_yjzb},{q2_yjzb},{q3_yjzb},{q4_yjzb},{q5_yjzb},{q0_dbxs},'{q0_dbfx}',{q90_zhdf},{q91_yjzb},{q92_yjzb},{q93_yjzb},{q95_yjzb},NULL,NULL,{sumqh40_rd},{qd01},{q1_2hsz},{q1_2gxz},{q1_2gxl},{q1_2jqdf},{sumqh51_rd},{qc05_0},{q1_3hsz},{q1_3gxz},{q1_3gxl},{q1_3jqdf},{qj57},{q1_4hsz},{q1_4gxz},{q1_4gxl},{q1_4jqdf},{qj56},{q1_5hsz},{q1_5gxz},{q1_5gxl},{q1_5jqdf},{qc05_0_gf},{q2_1hsz},{q2_1gxz},{q2_1gxl},{q2_1jqdf},{qd08},{qd18},{q2_2hsz},{q2_2gxz},{q2_2gxl},{q2_2jqdf},{qj80},{q2_3hsz},{q2_3gxz},{q2_3gxl},{q2_3jqdf},{sn_qc05_0},{q2_4hsz},{q2_4gxz},{q2_4gxl},{q2_4jqdf},{qc12},{q2_5hsz},{q2_5gxz},{q2_5gxl},{q2_5jqdf},{qb11num},{sn_qb11num},{q2_6hsz},{q2_6gxz},{q2_6gxl},{q2_6jqdf},{qc226_qy},{q2_7hsz},{q2_7gxz},{q2_7gxl},{q2_7jqdf},{qj73},{qj79},{q2_8hsz},{q2_8gxz},{q2_8gxl},{q2_8jqdf},{qz001},{qc02},{qc05_0_qt},{q2_9hsz},{q2_9gxz},{q2_9gxl},{q2_9jqdf},{qc41_gy},{qz001_gy},{q3_1hsz},{q3_1gxz},{q3_1gxl},{q3_1jqdf},{sn_qd01},{q3_5hsz},{q3_5gxz},{q3_5gxl},{q3_5jqdf},{qc51},{q3_6hsz},{q3_6gxz},{q3_6gxl},{q3_6jqdf},{qj90_qy},{q4_1hsz},{q4_1gxz},{q4_1gxl},{q4_1jqdf},{qj33_1},{qj33_2},{qj33_3},{qj33_4},{qj59},{qj61},{q4_2hsz},{q4_2gxz},{q4_2gxl},{q4_2jqdf},{qj79_2_qy},{qj57_2_qy},{q4_3hsz},{q4_3gxz},{q4_3gxl},{q4_3jqdf},{qj98_1_qy},{q4_4hsz},{q4_4gxz},{q4_4gxl},{q4_4jqdf},{qc11_1},{qc11},{q4_5hsz},{q4_5gxz},{q4_5gxl},{q4_5jqdf},{qc11_gq},{q4_6hsz},{q4_6gxz},{q4_6gxl},{q4_6jqdf},{qd25},{qd03},{q4_7hsz},{q4_7gxz},{q4_7gxl},{q4_7jqdf},{sn_qz001},{q5_2hsz},{q5_2gxz},{q5_2gxl},{q5_2jqdf},{qc05_0_rd5},{q5_3hsz},{q5_3gxz},{q5_3gxl},{q5_3jqdf},{qc05_0_sz},{q5_4hsz},{q5_4gxz},{q5_4gxl},{q5_4jqdf},{qb15_xssqy},{q5_6hsz},{q5_6gxz},{q5_6gxl},{q5_6jqdf},{qc05_rd5},{q5_7hsz},{q5_7gxz},{q5_7gxl},{q5_7jqdf})"
        self.ins_yh_str = "REPLACE INTO `portrait_yh` (sid,susername,q0_zhdf,q1_yjzb,q2_yjzb,q3_yjzb,q4_yjzb,q5_yjzb,q90_zhdf,q91_yjzb,q92_yjzb,q93_yjzb,q95_yjzb,sumqh40_rd,qd01,q1_2hsz,q1_2jqdf,sumqh51_rd,qc05_0,q1_3hsz,q1_3jqdf,qj57,q1_4hsz,q1_4jqdf,qj56,q1_5hsz,q1_5jqdf,qc05_0_gf,q2_1hsz,q2_1jqdf,qd08,qd18,q2_2hsz,q2_2jqdf,qj80,q2_3hsz,q2_3jqdf,sn_qc05_0,q2_4hsz,q2_4jqdf,qc12,q2_5hsz,q2_5jqdf,qb11num,sn_qb11num,q2_6hsz,q2_6jqdf,qc226_qy,q2_7hsz,q2_7jqdf,qj73,qj79,q2_8hsz,q2_8jqdf,qz001,qc02,qc05_0_qt,q2_9hsz,q2_9jqdf,qc41_gy,qz001_gy,q3_1hsz,q3_1jqdf,sn_qd01,q3_5hsz,q3_5jqdf,qc51,q3_6hsz,q3_6jqdf,qj90_qy,q4_1hsz,q4_1jqdf,qj33_1,qj33_2,qj33_3,qj33_4,qj59,qj61,q4_2hsz,q4_2jqdf,qj79_2_qy,qj57_2_qy,q4_3hsz,q4_3jqdf,qj98_1_qy,q4_4hsz,q4_4jqdf,qc11_1,qc11,q4_5hsz,q4_5jqdf,qc11_gq,q4_6hsz,q4_6jqdf,qd25,qd03,q4_7hsz,q4_7jqdf,sn_qz001,q5_2hsz,q5_2jqdf,qc05_0_rd5,q5_3hsz,q5_3jqdf,qc05_0_sz,q5_4hsz,q5_4jqdf,qb15_xssqy,q5_6hsz,q5_6jqdf,qc05_rd5,q5_7hsz,q5_7jqdf) VALUES ('{sid}','{susername}',{q0_zhdf},{q1_yjzb},{q2_yjzb},{q3_yjzb},{q4_yjzb},{q5_yjzb},{q90_zhdf},{q91_yjzb},{q92_yjzb},{q93_yjzb},{q95_yjzb},{sumqh40_rd},{qd01},{q1_2hsz},{q1_2jqdf},{sumqh51_rd},{qc05_0},{q1_3hsz},{q1_3jqdf},{qj57},{q1_4hsz},{q1_4jqdf},{qj56},{q1_5hsz},{q1_5jqdf},{qc05_0_gf},{q2_1hsz},{q2_1jqdf},{qd08},{qd18},{q2_2hsz},{q2_2jqdf},{qj80},{q2_3hsz},{q2_3jqdf},{sn_qc05_0},{q2_4hsz},{q2_4jqdf},{qc12},{q2_5hsz},{q2_5jqdf},{qb11num},{sn_qb11num},{q2_6hsz},{q2_6jqdf},{qc226_qy},{q2_7hsz},{q2_7jqdf},{qj73},{qj79},{q2_8hsz},{q2_8jqdf},{qz001},{qc02},{qc05_0_qt},{q2_9hsz},{q2_9jqdf},{qc41_gy},{qz001_gy},{q3_1hsz},{q3_1jqdf},{sn_qd01},{q3_5hsz},{q3_5jqdf},{qc51},{q3_6hsz},{q3_6jqdf},{qj90_qy},{q4_1hsz},{q4_1jqdf},{qj33_1},{qj33_2},{qj33_3},{qj33_4},{qj59},{qj61},{q4_2hsz},{q4_2jqdf},{qj79_2_qy},{qj57_2_qy},{q4_3hsz},{q4_3jqdf},{qj98_1_qy},{q4_4hsz},{q4_4jqdf},{qc11_1},{qc11},{q4_5hsz},{q4_5jqdf},{qc11_gq},{q4_6hsz},{q4_6jqdf},{qd25},{qd03},{q4_7hsz},{q4_7jqdf},{sn_qz001},{q5_2hsz},{q5_2jqdf},{qc05_0_rd5},{q5_3hsz},{q5_3jqdf},{qc05_0_sz},{q5_4hsz},{q5_4jqdf},{qb15_xssqy},{q5_6hsz},{q5_6jqdf},{qc05_rd5},{q5_7hsz},{q5_7jqdf});"
        # self.ins_yh_str = "INSERT INTO `portrait_yh` (sid,susername,q0_zhdf,q1_yjzb,q2_yjzb,q3_yjzb,q4_yjzb,q5_yjzb,q90_zhdf,q91_yjzb,q92_yjzb,q93_yjzb,q95_yjzb,sumqh40_rd,qd01,q1_2hsz,q1_2jqdf,sumqh51_rd,qc05_0,q1_3hsz,q1_3jqdf,qj57,q1_4hsz,q1_4jqdf,qj56,q1_5hsz,q1_5jqdf,qc05_0_gf,q2_1hsz,q2_1jqdf,qd08,qd18,q2_2hsz,q2_2jqdf,qj80,q2_3hsz,q2_3jqdf,sn_qc05_0,q2_4hsz,q2_4jqdf,qc12,q2_5hsz,q2_5jqdf,qb11num,sn_qb11num,q2_6hsz,q2_6jqdf,qc226_qy,q2_7hsz,q2_7jqdf,qj73,qj79,q2_8hsz,q2_8jqdf,qz001,qc02,qc05_0_qt,q2_9hsz,q2_9jqdf,qc41_gy,qz001_gy,q3_1hsz,q3_1jqdf,sn_qd01,q3_5hsz,q3_5jqdf,qc51,q3_6hsz,q3_6jqdf,qj90_qy,q4_1hsz,q4_1jqdf,qj33_1,qj33_2,qj33_3,qj33_4,qj59,qj61,q4_2hsz,q4_2jqdf,qj79_2_qy,qj57_2_qy,q4_3hsz,q4_3jqdf,qj98_1_qy,q4_4hsz,q4_4jqdf,qc11_1,qc11,q4_5hsz,q4_5jqdf,qc11_gq,q4_6hsz,q4_6jqdf,qd25,qd03,q4_7hsz,q4_7jqdf,sn_qz001,q5_2hsz,q5_2jqdf,qc05_0_rd5,q5_3hsz,q5_3jqdf,qc05_0_sz,q5_4hsz,q5_4jqdf,qb15_xssqy,q5_6hsz,q5_6jqdf,qc05_rd5,q5_7hsz,q5_7jqdf) VALUES ('{sid}','{susername}',{q0_zhdf},{q1_yjzb},{q2_yjzb},{q3_yjzb},{q4_yjzb},{q5_yjzb},{q90_zhdf},{q91_yjzb},{q92_yjzb},{q93_yjzb},{q95_yjzb},{sumqh40_rd},{qd01},{q1_2hsz},{q1_2jqdf},{sumqh51_rd},{qc05_0},{q1_3hsz},{q1_3jqdf},{qj57},{q1_4hsz},{q1_4jqdf},{qj56},{q1_5hsz},{q1_5jqdf},{qc05_0_gf},{q2_1hsz},{q2_1jqdf},{qd08},{qd18},{q2_2hsz},{q2_2jqdf},{qj80},{q2_3hsz},{q2_3jqdf},{sn_qc05_0},{q2_4hsz},{q2_4jqdf},{qc12},{q2_5hsz},{q2_5jqdf},{qb11num},{sn_qb11num},{q2_6hsz},{q2_6jqdf},{qc226_qy},{q2_7hsz},{q2_7jqdf},{qj73},{qj79},{q2_8hsz},{q2_8jqdf},{qz001},{qc02},{qc05_0_qt},{q2_9hsz},{q2_9jqdf},{qc41_gy},{qz001_gy},{q3_1hsz},{q3_1jqdf},{sn_qd01},{q3_5hsz},{q3_5jqdf},{qc51},{q3_6hsz},{q3_6jqdf},{qj90_qy},{q4_1hsz},{q4_1jqdf},{qj33_1},{qj33_2},{qj33_3},{qj33_4},{qj59},{qj61},{q4_2hsz},{q4_2jqdf},{qj79_2_qy},{qj57_2_qy},{q4_3hsz},{q4_3jqdf},{qj98_1_qy},{q4_4hsz},{q4_4jqdf},{qc11_1},{qc11},{q4_5hsz},{q4_5jqdf},{qc11_gq},{q4_6hsz},{q4_6jqdf},{qd25},{qd03},{q4_7hsz},{q4_7jqdf},{sn_qz001},{q5_2hsz},{q5_2jqdf},{qc05_0_rd5},{q5_3hsz},{q5_3jqdf},{qc05_0_sz},{q5_4hsz},{q5_4jqdf},{qb15_xssqy},{q5_6hsz},{q5_6jqdf},{qc05_rd5},{q5_7hsz},{q5_7jqdf});"
        self.upd_sql = "update year_quota set sn_qc05_0_sum={0},sn_qb11num_sum={1},sn_qd01_sum={2},sn_qz001_sum={3} where year={4};"
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'root'
        self.database = 'torch'
        self.get_sjk_pz()

    def save_scb(self, sc_df, yh_df, year):
        try:
            db, cursor = self.create_conn()
            for index, row in yh_df.iterrows():
                data_dict = dict(row.to_dict())
                print(data_dict["susername"])
                if data_dict["susername"] == '优化前':
                    data_dict['sid'] = f'yhq{year}'
                else:
                    data_dict['sid'] = f'yhh{year}'
                cursor.execute(self.ins_yh_str.format(**data_dict))
            try:
                cursor.execute(self.tru_sql.format(year))
            except:
                cursor.execute(self.cre_sql.format(year))
            ins_list = []
            db.commit()
            try:
                for index, row in sc_df.iterrows():
                    data_dict = dict(row.to_dict())
                    if str(index).endswith('00'):
                        cursor.execute(self.ins_sql.format(year, ','.join(ins_list)))
                        ins_list = []
                    ins_list.append(self.ins_th_str.format(**data_dict))
                if ins_list:
                    cursor.execute(self.ins_sql.format(year, ','.join(ins_list)))
                db.commit()
            except:
                self.write_rz('切换年度-错误日志-插入生成表.txt')
            self.close_conn(db, cursor)
        except:
            self.write_rz('切换年度-错误日志-插入数据库.txt')

    def eval_zx(self, eval_str, sum_dict):
        try:
            eval_jg = eval(eval_str, sum_dict)
        except Exception as E:
            if str(E) in ['float division by zero', 'division by zero']:
                eval_jg = 0
            else:
                errorFile = open('eval-错误日志.txt', 'a')
                errorFile.write(f'{eval_str} \n')
                errorFile.close()
                eval_jg = 0
        return eval_jg

    def create_conn(self):  # 创建连接
        conn = sql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        cursor = conn.cursor(sql.cursors.DictCursor)
        return conn, cursor

    def close_conn(self, conn, cursor):  # 关闭连接
        cursor.close()
        conn.close()

    def get_all_sum(self, sum_dict, df, pd_list):
        yh_dict = {}
        for sum_zd in self.sum_zd_list[0]:
            if sum_zd.startswith('sn_'):
                yh_dict[sum_zd] = sum_dict[f'{sum_zd}_sum']
                continue
            else:
                sum_data = df[df[pd_list[0]] == pd_list[1]][sum_zd].apply(lambda x: Decimal('%.4f' % x))
                sjk_zd_sum = float(sum_data.sum())
            sum_dict[sum_zd + '_sum'] = sjk_zd_sum
            yh_dict[sum_zd] = sjk_zd_sum
        for sum_zd in self.sum_zd_list[1]:
            gs_list = self.title_gs_dict[sum_zd]
            hsz_gs = gs_list[0].replace("']", "_sum").replace("df['", "")
            sjk_zd_sum = self.eval_zx(hsz_gs, sum_dict)
            sum_dict[sum_zd + 'hsz_sum'] = sjk_zd_sum
            yh_dict[sum_zd + 'hsz'] = sjk_zd_sum
            jqdf = self.eval_zx(gs_list[3][:-10], sum_dict)
            if jqdf > 1:
                jqdf_zh = 1 * sum_dict[sum_zd + '_qz']
            elif jqdf < 0:
                jqdf_zh = 0 * sum_dict[sum_zd + '_qz']
            else:
                jqdf_zh = jqdf * sum_dict[sum_zd + '_qz']
            sum_dict[sum_zd + 'jqdf_sum'] = jqdf_zh
            yh_dict[sum_zd + 'jqdf'] = jqdf_zh
        for zb_df_set in self.zb_js_list:
            yjzb_df = 0
            for zb_name in zb_df_set[0]:
                try:
                    yjzb_df += sum_dict[zb_name + '_sum']
                except:
                    yjzb_df += sum_dict[zb_name]
            sum_dict[zb_df_set[1]] = yjzb_df
            yh_dict[zb_df_set[1]] = yjzb_df
        return sum_dict, yh_dict

    def get_sc_dict(self, data_dict, jg_dict, sum_dict):
        dbxs = 0
        dbfx = ''
        for js_tm, gs_dict in self.title_gs_dict.items():
            gxz_gs = gs_dict[1]['在库']
            gxl_gs = gs_dict[2]
            jq_gs_dict = gs_dict[4]
            eval_gxz = gxz_gs.format(**data_dict)
            gxz = self.eval_zx(eval_gxz, sum_dict)
            sum_dict[js_tm + 'gxz'] = gxz
            gxl = self.eval_zx(gxl_gs, sum_dict)
            if js_tm in ['q2_4', 'q2_6', 'q2_7', 'q3_5', 'q4_1', 'q4_3', 'q4_4', 'q5_6', 'q5_7'] and gxz == 0:
                dbxs += 1
                dbfx += self.db_fx_dict[js_tm].format(data_dict[f'{js_tm}hsz'], abs(
                    float(sum_dict[f'{js_tm}hsz_sum']) - float(data_dict[f'{js_tm}hsz'])))
            elif gxz < 0:
                dbxs += 1
                dbfx += self.db_fx_dict[js_tm].format(data_dict[f'{js_tm}hsz'], abs(
                    float(sum_dict[f'{js_tm}hsz_sum']) - float(data_dict[f'{js_tm}hsz'])))
            jg_dict[js_tm + 'gxz'] = gxz
            jg_dict[js_tm + 'gxl'] = gxl
            jqdf = self.eval_zx(jq_gs_dict['在库'], sum_dict)
            jg_dict[js_tm + 'jqdf'] = jqdf
        jg_dict['q0_dbxs'] = dbxs
        jg_dict['q0_dbfx'] = dbfx[:-1]
        for zb_df_set in self.zb_js_list:
            yjzb_df = 0
            for zb_name in zb_df_set[0]:
                yjzb_df += jg_dict[zb_name]
            jg_dict[zb_df_set[1]] = yjzb_df
        return jg_dict

    def fetch_all(self, sql_ml):  # 查询全部
        conn, cursor = self.create_conn()
        cursor.execute(sql_ml)
        res = cursor.fetchall()
        self.close_conn(conn, cursor)
        return res

    def fetch_one(self, sql_ml):  # 单个查询
        conn, cursor = self.create_conn()
        cursor.execute(sql_ml)
        res = cursor.fetchone()
        self.close_conn(conn, cursor)
        return res

    def get_max_mix(self, year, sum_dict):
        data_dict = self.fetch_one(f"select * from year_quota where year={year};")
        for k, v in data_dict.items():
            if k.startswith('q') or k.startswith('sn_'):
                try:
                    sum_dict[k] = float(v)
                except:
                    sum_dict[k] = 0
        return sum_dict

    def wtite_cwrz(self):
        errorFile = open('基础错误日志.txt', 'a')
        errorFile.write(traceback.format_exc())
        errorFile.close()

    def write_rz(self, txt_name):
        errorFile = open(txt_name, 'a', encoding='utf-8')
        errorFile.write(traceback.format_exc())
        errorFile.close()

    def get_sjk_pz(self):
        # 获取数据库配置信息
        try:
            db = sql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = db.cursor()
            sel_ml = 'select title,weight,hsz_gs,gxz_gs,gxl_gs,jqdf_zh_gs,jqdf_gs from qygzlpj_gs'
            cursor.execute(sel_ml)
            sjk_pz_list = cursor.fetchall()
            gjc_dict = {}
            for sjk_pz in sjk_pz_list:
                self.sum_dict[f'{sjk_pz[0]}_qz'] = float(sjk_pz[1])
                gjc_re = re.findall('{(.*?)}', sjk_pz[2])
                for gjc in gjc_re:
                    gjc_dict[gjc] = 0
                self.title_gs_dict[sjk_pz[0]] = [sjk_pz[2], eval(sjk_pz[3]), sjk_pz[4], sjk_pz[5], eval(sjk_pz[6])]
            self.gjc_list = list(gjc_dict.keys())
            self.close_conn(db, cursor)
        except:
            self.wtite_cwrz()

    def one_operation(self, _this_year, _last_year, _sum_qt_dict, _year):
        sn_data_dict = {}
        for data in _last_year:
            sn_list = []
            for key in ['qc05_0', 'qb11num', 'qd01', 'qz001']:
                sn_list.append(Decimal(data[key]))
            sn_data_dict[data['susername']] = sn_list
        sn_df = pd.DataFrame(sn_data_dict.values())
        for sy, key in enumerate(['qc05_0', 'qb11num', 'qd01', 'qz001']):
            _sum_qt_dict[f'sn_{key}_sum'] = sn_df.sum()[sy]
        conn, cursor = self.create_conn()
        cursor.execute(self.upd_sql.format(sn_df.sum()[0], sn_df.sum()[1], sn_df.sum()[2], sn_df.sum()[3], _year))
        conn.commit()
        self.close_conn(conn, cursor)
        data_dict = {}
        for one_data in _this_year:
            susername = one_data['susername']
            one_data['issta'] = '保留'
            try:
                sn_list = sn_data_dict[susername]
                one_data['sn_qc05_0'] = sn_list[0]
                one_data['sn_qb11num'] = sn_list[1]
                one_data['sn_qd01'] = sn_list[2]
                one_data['sn_qz001'] = sn_list[3]
                one_data['library'] = '在库'
                # one_data['issta'] = '保留'
            except:
                one_data['sn_qc05_0'] = 0
                one_data['sn_qb11num'] = 0
                one_data['sn_qd01'] = 0
                one_data['sn_qz001'] = 0
                one_data['library'] = '新增'
                # one_data['issta'] = '剔除'
            data_dict[susername] = one_data
        df = pd.DataFrame(data_dict.values(), dtype='float')
        for sum_zd in self.sum_zd_list[0]:
            df[sum_zd] = df[sum_zd].apply(lambda x: float('%.4f' % x))
        df['sbelongwhere'] = df['sbelongwhere'].apply(lambda x: '%.f' % x)
        for tm, gs in self.title_gs_dict.items():
            hsz_gs = f'np.array({gs[0]})'
            df[f'{tm}hsz'] = eval(hsz_gs)
        return df

    def sc_main(self, _json_data):
        try:
            this_year = _json_data['this_year']
            last_year = _json_data['last_year']
            js_year = int(_json_data['year'])
            sum_qt_dict = copy(self.sum_dict)
            sum_qt_dict = self.get_max_mix(js_year, sum_qt_dict)
            df = self.one_operation(this_year, last_year, sum_qt_dict, js_year)
            sum_qt_dict, lib_zk = self.get_all_sum(sum_qt_dict, df, ['library', '在库'])
            lib_zk['susername'] = '优化前'
            df.fillna(0, inplace=True)
            df.replace([np.inf, -np.inf], 0.0, inplace=True)
            data_list = []
            for index, row in df.iterrows():
                data_dict = dict(row.to_dict())
                jg_dict = self.get_sc_dict(data_dict, data_dict, sum_qt_dict)
                data_list.append(jg_dict)
            data_df = pd.DataFrame(data_list)
            data_df.replace([np.inf, -np.inf], 0.0, inplace=True)
            sum_qt_dict, iss_bl = self.get_all_sum(sum_qt_dict, df, ['issta', '保留'])
            iss_bl['susername'] = '优化后'
            yh_dict = pd.DataFrame([lib_zk, iss_bl])
            self.save_scb(data_df, yh_dict, js_year)
            return data_df, yh_dict
        except:
            self.write_rz('切换年度-错误日志.txt')
            return False

    def xg_main(self, _js_year):
        try:
            db, cursor = self.create_conn()
            js_year = int(_js_year)
            sum_xg_dict = copy(self.sum_dict)
            sum_xg_dict = self.get_max_mix(js_year, sum_xg_dict)
            cursor.execute(f'SELECT * FROM `portrait_{js_year}_sc`')
            data_sql = cursor.fetchall()
            df = pd.DataFrame(data_sql)
            sum_xg_dict, iss_bl = self.get_all_sum(sum_xg_dict, df, ['issta', '保留'])
            iss_bl['sid'] = f'yhh{js_year}'
            iss_bl['susername'] = '优化后'
            cursor.execute(self.ins_yh_str.format(**iss_bl))
            db.commit()
            self.close_conn(db, cursor)
            return True
        except:
            self.write_rz('单一修改-错误日志.txt')
            return False


PortraitCal = PortraitCal_class()
# if __name__ == '__main__':
#     切换年度
#     with open(r'D:\下载\response.json', 'r', encoding='utf-8') as r:
#         json_data = json.loads(r.read())
#     data_df, yh_dicts = self_sl.sc_main(json_data)
#     print(data_df)
#     print(yh_dicts)
