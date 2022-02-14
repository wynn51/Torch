import jwt
import pandas as pd
import pymysql
from django.db import connection
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from extension import get_Table, qyhx_wy, dfTable
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
import traceback

this_year_sql_col = "`susername`,`sname`,`sbelongwhere`,`sumqh40_rd`,`qd01`,`sumqh51_rd`,`qc05_0`,`qj57`,`qj56`,`qc05_0_gf`,`qd08`,`qd18`,`qj80`,`qc12`,`qb11num`,`qc226_qy`,`qj73`,`qj79`,`qz001`,`qc02`,`qc05_0_qt`,`qc41_gy`,`qz001_gy`,`qc51`,`qj90_qy`,`qj33_1`,`qj33_2`,`qj33_3`,`qj33_4`,`qj59`,`qj61`,`qj79_2_qy`,`qj57_2_qy`,`qj98_1_qy`,`qc11_1`,`qc11`,`qc11_gq`,`qd25`,`qd03`,`qc05_0_rd5`,`qc05_0_sz`,`qb15_xssqy`,`qc05_rd5`"
last_year_sql_col = "`susername`,`qc05_0`,`qb11num`,`qd01`,`qz001`"


# 获取今年数据和去年数据
class Cal_sc(APIView):
    def get(self, request):
        year = int(request.query_params.get('year'))
        '''今年数据和去年数据'''
        with connection.cursor() as cursor:
            # -------this year
            try:
                cursor.execute(f'select {this_year_sql_col} from {str(year) + "qyb"}')
                print(f'select {this_year_sql_col} from {str(year) + "qyb"}')
            except Exception as e:
                print(e)
                return None
            this_year_cols_tuple = cursor.description
            this_year_res_tuple = cursor.fetchall()

            # -------last year
            try:
                cursor.execute(f'select {last_year_sql_col} from {str(year - 1) + "qyb"}')
            except Exception as e:
                print(e)
                return None
            last_year_cols_tuple = cursor.description
            last_year_res_tuple = cursor.fetchall()

        this_year_cols = [col[0] for col in this_year_cols_tuple]
        last_year_cols = [col[0] for col in last_year_cols_tuple]
        this_year_data = [
            dict(zip(this_year_cols, row))
            for row in this_year_res_tuple
        ]
        last_year_data = [
            dict(zip(last_year_cols, row))
            for row in last_year_res_tuple
        ]
        # ---------------------计算生成表--------------------
        try:
            sc_df, yh_df = qyhx_wy.PortraitCal.sc_main({'year': year,
                                                                  'this_year': this_year_data,
                                                                  'last_year': last_year_data})
            return Response({'code': 200})
        except:
            print(traceback.format_exc())
            return Response({'code': 500})
        # sc_df.to_excel('./sc_df.xlsx')
        # yh_df.to_excel('./yh_df.xlsx')


class SearchInfo(APIView):
    def get(self, request):
        year = request.query_params.get('year')
        # year = '2027'
        page_num = request.query_params.get('page')
        page_size = request.query_params.get('page_size')
        company_type = request.query_params.get('cType')  # 0全部  1高新技术企业  2上市挂牌企业
        is_keep = request.query_params.get('is_keep')  # 0全部 1保留 2剔除
        search_content = request.query_params.get('s_key')  # str
        # dict1 = request.query_params
        search_dict = {'cType': company_type, 'is_keep': is_keep, 's_key': search_content}

        sc_data, yh_data, total = get_Table.get_portrait_Table(year, int(page_num), int(page_size), search_dict)

        return Response({
            'total': total,
            'len': len(sc_data),
            'yh_data': yh_data,
            'result': sc_data,
        })

    def put(self, request):
        body = request.data
        year = body['year']
        # year = '2027'
        is_keep = body['is_keep']
        xydm = body['xydm']
        is_keep_dict = {'1': '保留', '2': '剔除'}
        # serverName = '127.0.0.1'
        # userName = 'root'
        # passWord = 'root'
        # db = pymysql.connect(user=userName, password=passWord, host=serverName, database="torch")
        # cur = db.cursor()

        with connection.cursor() as cur:
            try:
                cur.execute(f"UPDATE portrait_{year}_sc SET issta='{is_keep_dict[is_keep]}' WHERE susername='{xydm}'")
                qyhx_wy.PortraitCal.xg_main(year)
            except:
                return Response({'code': 500, "error": '操作失败'})
        return Response({'code': 200, 'success': '操作成功'})


class DownloadView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):

        def file_iterator(fn, chunk_size=512):
            while True:
                c = fn.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        year = request.data.get('year')
        downloads_name = f'{year}画像数据.xlsx'
        sc = dfTable.get_dfTable(f'portrait_{year}_sc')
        yh = dfTable.get_dfTable(f'portrait_yh')
        pd1 = pd.concat([yh.drop('sid', axis=1), sc], axis=0)
        pd1 = pd1[sc.columns]
        pd1.to_excel(f'./{downloads_name}', index=False)
        fn = open(f'./{downloads_name}', 'rb')
        response = StreamingHttpResponse(file_iterator(fn))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename="{downloads_name}"'

        return response
