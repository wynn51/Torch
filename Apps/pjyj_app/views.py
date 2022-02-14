from django.db import connection
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from Apps.pjyj_app.tools.pjyj import pjyj_cal
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import json


def table_to_json(cols_tuple, res_tuple):
    if isinstance(cols_tuple, list):
        cols = cols_tuple
    else:
        cols = [col[0] for col in cols_tuple]
    list1 = [
        dict(zip(cols, row))
        for row in res_tuple
    ]
    return list1


# 综合评价
class Zhpj_data(APIView):
    # 获取综合评价页面数据
    def get(self, request):
        year = int(request.query_params.get('year'))
        area_code = str(request.query_params.get('area_code'))
        # 连接数据库分别获取三个指标的数据
        with connection.cursor() as cursor:
            # ----------判断是否存在对应目标值字段
            col = f'aim_{year}_{area_code}'
            search_col_sql1 = f"select count(*) from information_schema.columns where table_name = 'pjyj_grade2' and column_name = '{col}'"
            search_col_sql2 = f"select count(*) from information_schema.columns where table_name = 'pjyj_grade3' and column_name = '{col}'"

            cursor.execute(search_col_sql1)
            if cursor.fetchall()[0][0] == 0:
                cursor.execute(f'ALTER TABLE `pjyj_grade2` ADD COLUMN `{col}` decimal(64, 6) NULL default 0')
            cursor.execute(search_col_sql2)
            if cursor.fetchall()[0][0] == 0:
                cursor.execute(f'ALTER TABLE `pjyj_grade3` ADD COLUMN `{col}` decimal(64, 6) NULL default 0')
            # ----------------------一级指标----------------------
            # try:
            #     sql1 = f'select aid,CONCAT(aid,grade1) as grade1_name from pjyj_grade1'
            #     cursor.execute(sql1)
            # except Exception as e:
            #     print(e)
            #     return None
            # cols_tuple = ['aid', 'grade1_name']
            # res_tuple = cursor.fetchall()
            # list1 = table_to_json(cols_tuple, res_tuple)

            # ----------------------二级指标------------------------
            try:
                aim_value = f"aim_{str(year)}_{area_code}"
                sql2 = f'SELECT b.id,b.parent_id,a.grade1 as parent_grade_name, b.grade2 as grade_name, b.weight,unit, b.formula, b.look_table, b.this_year_value, b.last_year_value, b.this_year_value-b.last_year_value as year_dif, b.{aim_value} as aim_value, b.this_year_value-b.{aim_value} as aim_dif FROM pjyj_grade1 a inner join pjyj_grade2 b WHERE a.id = b.parent_id'
                cursor.execute(sql2)
            except Exception as e:
                print(e)
                return Response({'error': "grade2_get_error"})
            cols_tuple = cursor.description
            res_tuple = cursor.fetchall()
            list2 = table_to_json(cols_tuple, res_tuple)

            # ----------------------三级指标------------------------
            try:
                sql3 = f'SELECT id,parent_id,grade3 as grade_name,unit,code,look_table,this_year_value,last_year_value,this_year_value-last_year_value as year_dif,{aim_value} as aim_value,this_year_value-{aim_value} as aim_dif FROM pjyj_grade3'
                cursor.execute(sql3)
            except Exception as e:
                print(e)
                return Response({'error': "grade3_get_error"})
            cols_tuple = cursor.description
            # cols_tuple = ['cid', 'grade3_name', 'unit', 'code', 'look_table', 'value2019', 'value2018', 'year_dif',
            #               'aim_value', 'aim_dif']
            res_tuple = cursor.fetchall()
            list3 = table_to_json(cols_tuple, res_tuple)
        # --------------------二三级指标合并----------------------
        for index, json2 in enumerate(list2):
            bid = json2['id']
            for json3 in list3:
                parent_id = json3['parent_id']
                if bid == parent_id:
                    if 'children' not in json2.keys():
                        list2[index]['children'] = [json3]
                    else:
                        list2[index]['children'] = list2[index]['children'] + [json3]
        return Response(list2)

    # 修改目标值w
    def put(self, request):
        body = request.data  # bid/cid  year  aim_value
        year = str(body['year'])
        area_code = str(body['area_code'])
        aim2_dict = body['grade2_aim']
        aim3_dict = body['grade3_aim']
        print(aim2_dict)
        print(aim3_dict)
        when_then_grade3 = ''
        when_then_grade2 = ''
        # 修改目标值

        with connection.cursor() as cursor:
            # ----------判断是否存在对应目标值字段
            col = f'aim_{year}_{area_code}'
            search_col_sql1 = f"select count(*) from information_schema.columns where table_name = 'pjyj_grade2' and column_name = '{col}'"
            search_col_sql2 = f"select count(*) from information_schema.columns where table_name = 'pjyj_grade3' and column_name = '{col}'"

            cursor.execute(search_col_sql1)
            if cursor.fetchall()[0][0] == 0:
                cursor.execute(f'ALTER TABLE `pjyj_grade2` ADD COLUMN `{col}` decimal(64, 6) NULL default 0')
            cursor.execute(search_col_sql2)
            if cursor.fetchall()[0][0] == 0:
                cursor.execute(f'ALTER TABLE `pjyj_grade3` ADD COLUMN `{col}` decimal(64, 6) NULL default 0')
            # ----------修改二级指标目标值
            if aim2_dict != {}:
                for aim_tuple in aim2_dict.items():
                    id, value = aim_tuple
                    when_then_grade2 = when_then_grade2 + f'WHEN "{id}" THEN {value} '
                end_str = '("{}")'.format(('","').join(list(aim2_dict.keys())))
                sql = f'UPDATE pjyj_grade2 SET {col} = CASE id {when_then_grade2} END WHERE id IN {end_str}'
                print(sql)
                cursor.execute(sql)

            # ----------修改三级指标目标值
            if aim3_dict != {}:
                for aim_tuple in aim3_dict.items():
                    id, value = aim_tuple
                    when_then_grade3 = when_then_grade3 + f'WHEN "{id}" THEN {value} '
                end_str = '("{}")'.format(('","').join(list(aim3_dict.keys())))
                sql = f'UPDATE pjyj_grade3 SET {col} = CASE id {when_then_grade3} END WHERE id IN {end_str}'
                print(sql)
                cursor.execute(sql)

        return Response(body)


# 体系配置-获取和修改
class Txpz_data(APIView):
    # 获取体系配置
    def get(self, request):
        key = request.query_params.get('key')
        key_dict = {'1': '一级指标', '2': '二级指标', '3': '三级指标', '4': '下钻规则'}
        if key not in key_dict.keys():
            return Response({'error': 'key值错误'})
        sql_dict = {
            '1': 'select id,grade1 as grade_name from pjyj_grade1',
            '2': 'SELECT b.parent_id, a.grade1 as parent_grade_name, b.id, b.grade2 as grade_name, b.weight, b.unit, b.formula FROM pjyj_grade1 a INNER JOIN pjyj_grade2 b WHERE a.id = b.parent_id',
            '3': 'SELECT b.parent_id, a.grade2 as parent_grade_name, b.id, b.grade3 as grade_name, b.code, b.unit, b.look_table FROM pjyj_grade2 a INNER JOIN pjyj_grade3 b WHERE a.id = b.parent_id'
        }
        cols_dict = {
            '1': ['aid', 'grade1'],
            '2': ['bid', 'grade1', 'grade2', 'unit', 'formula'],
            '3': ['cid', 'grade2', 'grade3', 'unit', 'code', 'look_table']
        }
        with connection.cursor() as cursor:
            try:
                sql1 = sql_dict[key]
                cursor.execute(sql1)
            except Exception as e:
                print(e)
                return Response({'error': "txpz_get_error"})
            cols_tuple = cursor.description
            res_tuple = cursor.fetchall()
            list1 = table_to_json(cols_tuple, res_tuple)
        result = list1
        return Response(result)

    # 修改体系配置
    def put(self, request):
        body = request.data
        sql = ''
        try:
            if str(body["type"]) == "1":
                sql = f'UPDATE pjyj_grade1 set grade1="{body["grade_name"]}" where id="{body["id"]}"'
            elif str(body["type"]) == "2":
                sql = f'UPDATE pjyj_grade2 set grade2="{body["grade_name"]}",unit="{body["unit"]}",formula="{body["formula"]}",look_table="{body["look_table"]}" where id="{body["id"]}"'
            elif str(body["type"]) == "3":
                sql = f'UPDATE pjyj_grade3 set grade3="{body["grade_name"]}",unit="{body["unit"]}",look_table="{body["look_table"]}",code="{body["code"]}" where id="{body["id"]}"'
            with connection.cursor() as cursor:
                print(sql)
                cursor.execute(sql)
        except Exception as e:
            print(e)
            return Response({'sql_error': '300'})
        return Response({'success': 200})


# 体系配置-删除和增加  txpz/opt/
class Txpz_add_del(APIView):
    # 体系配置-删除数据
    def get(self, request):
        type = str(request.query_params.get('type'))
        id = int(request.query_params.get('id'))
        sql_dict = {
            '2': f'DELETE FROM pjyj_grade2 WHERE id="{id}"',
            '3': f'DELETE FROM pjyj_grade3 WHERE id="{id}"'
        }
        try:
            with connection.cursor() as cursor:
                print(sql_dict[type])
                cursor.execute(sql_dict[type])
        except:
            return Response({'error': 300})
        return Response({"success": 200})

    # 体系配置-新增一条数据
    def post(self, request):
        body = request.data
        if not all(body.values()):
            return Response({'error': "值不能含空"})
        # 取值
        type = body["type"]

        grade_name = request.data.get("grade_name")
        look_table = request.data.get("look_table")
        code = request.data.get("code")
        formula = request.data.get("formula")
        weight = request.data.get("weight")
        unit = request.data.get("unit")
        parent_id = request.data.get("parent_id")

        sql_dict = {
            '2': f"INSERT INTO `torch`.`pjyj_grade2`(`parent_id`,`grade2`,`weight`,`unit`,`formula`,`look_table`) VALUES ('{parent_id}', '{grade_name}', '{weight}', '{unit}', '{formula}', '{look_table}')",
            '3': f"INSERT INTO `torch`.`pjyj_grade3` (`parent_id`,`grade3`,`unit`,`code`,`look_table`) VALUES ('{parent_id}', '{grade_name}', '{unit}', '{code}', '{look_table}')"
            }
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_dict[type])
        except:
            return Response({'error': '添加失败'})

        return Response({'success': 200})


# 体系配置-增加指标时请求获取指标信息  txpz/opt/list/
class Txpz_add_get(ModelViewSet):
    @action(methods=['get'], detail=False, url_path='lis')
    def lis(self, request):
        type = str(request.query_params.get("type"))   # 查询类型
        key = str(request.query_params.get("key"))    # 指标等级
        parent_id = str(request.query_params.get('id'))
        type0_sql = {
            '1': f'SELECT id,grade1 as grade_name From pjyj_grade1',
            '2': f'SELECT id,grade2 as grade_name From pjyj_grade2'
        }
        type1_sql = {
            '1': f'SELECT id,grade2 as grade_name From pjyj_grade2 Where parent_id="{parent_id}"',
            '2': f'SELECT id,grade3 as grade_name From pjyj_grade3 Where parent_id="{parent_id}"'
        }
        if type == '0':
            with connection.cursor() as cursor:
                sql = type0_sql[key]
                cursor.execute(sql)
                cols_tuple = cursor.description
                res_tuple = cursor.fetchall()
                res_json = table_to_json(cols_tuple,res_tuple)
                return Response(res_json)
        if type == '1':
            with connection.cursor() as cursor:
                sql = type1_sql[key]
                cursor.execute(sql)
                cols_tuple = cursor.description
                res_tuple = cursor.fetchall()
                res_json = table_to_json(cols_tuple, res_tuple)
                return Response(res_json)

        return Response({'error': 300})

    @action(methods=['get'], detail=False, url_path='isExist')
    def isExist(self, request):
        key = str(request.query_params.get('key'))
        grade_name = str(request.query_params.get('grade_name'))
        with connection.cursor() as cursor:
            sql = f"SELECT count(grade{key}) FROM `pjyj_grade{key}` where grade{key}='{grade_name}'"
            cursor.execute(sql)
            count = cursor.fetchall()[0][0]
            if count == 0:
                return Response({'code': 200})
            else:
                return Response({'code': 300})

# 指标计算
class Cal_grade(APIView):
    def get(self, request):
        # 三级指标校验
        # with connection.cursor() as cursor:
        #     sql = "SELECT a.id, b.id as cid, a.formula, b.code, a.grade2 FROM pjyj_grade2 a INNER JOIN pjyj_grade3 b ON a.id = b.parent_id"
        #     cursor.execute(sql)
        #     cols_tuple = cursor.description
        #     res_tuple = cursor.fetchall()
        #     print(res_tuple[0])
        #     inner_json = table_to_json(cols_tuple, res_tuple)
        #     return Response(inner_json)
        # 判断是否接收正确的年份和地域编码
        year = str(request.query_params.get('year'))
        area_code = str(request.query_params.get('area_code'))
        if not year or not area_code:
            return Response({"error": 300})
        # 开始计算
        aaa = pjyj_cal(year, area_code)
        bool1, error_json = aaa.grade_is_vaild()   # 公式校验
        if not bool1:
            return Response(error_json)
        aaa.get_grade3()
        aaa.cal_grade2()

        del aaa
        return Response({"success": 200})


