import pymysql
import pandas as pd
import numpy as np
import time
import re
import copy
from django.db import connection
from rest_framework.response import Response


class pjyj_cal():
    def __init__(self,year,area_code):
        print('初始化中.......')
        self.year = int(year)
        self.area_code = str(area_code)
        self.df_grade3 = self.get_dfTable('pjyj_grade3')
        self.df_grade2 = self.get_dfTable('pjyj_grade2')
        self.df_nianjian = self.get_dfTable('nianjian', area_open=True)
        self.df_this_zhb = self.get_dfTable(f'{self.year}zhb', area_open=True)
        self.df_this_qyb = self.get_dfTable(f'{self.year}qyb', area_open=True)
        self.df_last1_zhb = self.get_dfTable(f'{self.year-1}zhb', area_open=True)
        self.df_last1_qyb = self.get_dfTable(f'{self.year-1}qyb', area_open=True)
        self.df_last2_zhb = self.get_dfTable(f'{self.year-2}zhb', area_open=True)
        self.df_last2_qyb = self.get_dfTable(f'{self.year-2}qyb', area_open=True)

    def get_dfTable(self, tablename, area_open=False):
        # serverName = 'localhost'
        # # 登陆用户名和密码
        # userName = 'root'
        # passWord = 'root'
        # # 建立连接并获取cursor
        # db = pymysql.connect(user=userName, password=passWord, host=serverName, database="torch")
        with connection.cursor() as cur:
            # cur = db.cursor()
            sql = f'select * from {tablename}'
            if area_open:
                sql = f'select * from {tablename} where sbelongwhere={self.area_code}'
            try:
                cur.execute(sql)
                col = cur.description
                dbdata = cur.fetchall()

                col_list = [i[0] for i in col]
                return pd.DataFrame(dbdata, columns=col_list)
            except:
                return False

    def get_var(self, logical: str):
        regax = '([a-zA-Z0-9_"]+)'
        x = re.findall(regax, logical)  # 提取出式子中的单元
        bl_list = x[:]  # 变量存放
        for e in x:  # 循环删除常数值，保留赋值变量
            if '"' in e:
                bl_list.remove(e)
            if 'in' == e:
                bl_list.remove(e)
            if 'and' == e:
                bl_list.remove(e)
            if 'or' == e:
                bl_list.remove(e)
            if e.isdigit():
                bl_list.remove(e)
            if 'year' == e:
                bl_list.remove(e)

        bl_list = list(set(bl_list))
        bl_list.sort(key=lambda i: len(i), reverse=True)  # 字段名长到短排序，以防短字段替换掉部分长字段
        return bl_list

    def get_grade3(self):
        this_result_list = []
        last_result_list = []
        # 三级指标数据提取
        for index, var in self.df_grade3[['code', 'look_table']].iterrows():
            code, look_table = var
            # print(f'---------------{index, "   ", code," ",look_table}------------------')
            if look_table == '综合':
                # ---今年
                try:
                    this_result_list = this_result_list + [self.df_this_zhb[code][0]]
                except:
                    this_result_list = this_result_list + [0]
                # ---去年
                try:
                    last_result_list = last_result_list + [self.df_last1_zhb[code][0]]
                except:
                    last_result_list = last_result_list + [0]
            if look_table == '企业':
                # ---今年
                try:
                    this_result_list = this_result_list + [np.sum(np.array(self.df_this_qyb[code], dtype='float'))]
                except:
                    this_result_list = this_result_list + [0]
                # ---去年
                try:
                    last_result_list = last_result_list + [np.sum(np.array(self.df_last1_qyb[code], dtype='float'))]
                except:
                    last_result_list = last_result_list + [0]
            if look_table == '上年综合':
                # ---今年
                try:
                    this_result_list = this_result_list + [self.df_last1_zhb[code[3:]][0]]
                except:
                    this_result_list = this_result_list + [0]
                # ---去年
                try:
                    last_result_list = last_result_list + [self.df_last2_zhb[code[3:]][0]]
                except:
                    last_result_list = last_result_list + [0]
            if look_table == '上年企业':
                # ---今年
                try:
                    this_result_list = this_result_list + [np.sum(np.array(self.df_last1_qyb[code[3:]], dtype='float'))]
                except:
                    this_result_list = this_result_list + [0]
                # ---去年
                try:
                    last_result_list = last_result_list + [np.sum(np.array(self.df_last2_qyb[code[3:]], dtype='float'))]
                except:
                    last_result_list = last_result_list + [0]
            if look_table == '公开':
                # ---今年
                try:
                    temp1 = self.df_nianjian[code+'_'+str(self.year)][self.df_nianjian['sbelongwhere']==self.area_code].values[0]
                    this_result_list = this_result_list + [temp1]
                except:
                    this_result_list = this_result_list + [0]
                # ---去年
                try:
                    temp2 = self.df_nianjian[code + '_' + str(self.year-1)][self.df_nianjian['sbelongwhere'] == self.area_code].values[0]
                    last_result_list = last_result_list + [temp2]
                except:
                    last_result_list = last_result_list + [0]
            # None ——> 0
            for i in range(len(this_result_list)):
                if this_result_list[i] == None:
                    this_result_list[i] = 0
            for i in range(len(last_result_list)):
                if last_result_list[i] == None:
                    last_result_list[i] = 0
            # print('2020:', len(this_result_list), '    ', this_result_list[index])
            # print('2019:', len(last_result_list), '    ', last_result_list[index])
        self.df_grade3['this_year_value'] = pd.Series(this_result_list)
        self.df_grade3['last_year_value'] = pd.Series(last_result_list)
        # self.df_grade3.to_excel('./grade.xlsx')
        # 三级指标数据入库
        cid_list = list(self.df_grade3['id'])
        # print(cid_list)
        case_when1 = ''
        case_when2 = ''
        end_str = '","'.join(map(str, cid_list))
        for i in range(len(this_result_list)):
            case_when1 = case_when1 + f'WHEN "{cid_list[i]}" THEN {this_result_list[i]} '
            case_when2 = case_when2 + f'WHEN "{cid_list[i]}" THEN {last_result_list[i]} '
        this_sql = f'UPDATE pjyj_grade3 SET this_year_value = CASE id {case_when1}END WHERE id IN ("{end_str}")'
        last_sql = f'UPDATE pjyj_grade3 SET last_year_value = CASE id {case_when2}END WHERE id IN ("{end_str}")'
        # ---------------!!!!!!-------------
        with connection.cursor() as cur:
            cur.execute(this_sql)
            # print(this_sql)
            cur.execute(last_sql)
            # print(last_sql)
        return this_result_list, last_result_list

    def grade_is_vaild(self):
        for index, var in self.df_grade2[['id','formula','grade2']].iterrows():
            grade2_id, formula, grade2_name = var
            print(f'-----------------------{index}-----{formula}---------------------')
            listc = list(self.df_grade3['code'][self.df_grade3['parent_id']==grade2_id])
            listb = self.get_var(formula)
            print(listc)
            for value in listb:
                if value not in listc:
                    print(f'!!! {grade2_id} {grade2_name} 指标出错')
                    error_json = {
                        'error': 300,
                        'grade': f'{grade2_name}'
                    }
                    return False, error_json
        return True, 'True'

    def cal_grade2(self):
        this_value_list = []
        last_value_list = []
        for index, var in self.df_grade2[['id', 'formula']].iterrows():
            bid, formula = var
            # print(f'----------{index}-----{bid}--------------')
            formula = formula.replace(' ', '')
            # print(f'公式：', formula)
            if not formula: continue
            # -------------------------提取变量-----------------------
            bl_list = self.get_var(formula)
            # print(bl_list)
            # -------------------------数值替换-----------------------
            this_exc = copy.deepcopy(formula)
            last_exc = copy.deepcopy(formula)
            for bl in bl_list:
                this_temp = self.df_grade3['this_year_value'][self.df_grade3['code']==bl].values[0]
                last_temp = self.df_grade3['last_year_value'][self.df_grade3['code']==bl].values[0]
                this_exc = this_exc.replace(bl,str(this_temp))
                last_exc = last_exc.replace(bl,str(last_temp))
            # print('算式：', this_exc)
            # print('算式：', last_exc)
            # -------------------------算式求值----------------------
            try:
                this_value = eval(this_exc)
                this_value_list = this_value_list + [this_value]
                # print('success')
            except Exception as e:
                this_value_list = this_value_list + [0]
                print(f'{bid} this_year_value calculate error')
            try:
                last_value = eval(last_exc)
                last_value_list = last_value_list + [last_value]
                # print('success')
            except Exception as e:
                last_value_list = last_value_list + [0]
                print(f'{bid} last_year_value calculate error')
        print('今年数据：', len(this_value_list), this_value_list)
        print('去年数据：', len(last_value_list), last_value_list)
        self.df_grade2['this_year_value'] = pd.Series(this_value_list)
        self.df_grade2['last_year_value'] = pd.Series(last_value_list)

        # 二级指标数据入库
        bid_list = list(self.df_grade2['id'])
        case_when1 = ''
        case_when2 = ''
        end_str = '","'.join(map(str,bid_list))
        for i in range(len(this_value_list)):
            case_when1 = case_when1 + f'WHEN "{bid_list[i]}" THEN {this_value_list[i]} '
            case_when2 = case_when2 + f'WHEN "{bid_list[i]}" THEN {last_value_list[i]} '
        this_sql = f'UPDATE pjyj_grade2 SET this_year_value = CASE id {case_when1}END WHERE id IN ("{end_str}")'
        last_sql = f'UPDATE pjyj_grade2 SET last_year_value = CASE id {case_when2}END WHERE id IN ("{end_str}")'
        # ---------------!!!!!!-------------
        with connection.cursor() as cur:
            cur.execute(this_sql)
            # print(this_sql)
            cur.execute(last_sql)
            # print(last_sql)


# aaa = pjyj_cal('2020','500198')
# # aaa.get_grade3()
# aaa.cal_grade2()
# del aaa
