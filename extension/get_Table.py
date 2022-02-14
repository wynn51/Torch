import pymysql
from django.db import connection

def get_portrait_Table(year,pageNum,pageSize,search_dict=None):
    company_type = search_dict['cType']  # 0全部  1高新技术企业  2上市挂牌企业
    is_keep = search_dict['is_keep']  # 0全部 1保留 2剔除
    search_content = search_dict['s_key']  # 信用代码查询
    # serverName = '127.0.0.1'
    # userName = 'root'
    # passWord = 'root'
    # -----------------拼接查询条件--------------
    str1 = ''
    if company_type and company_type != '0':
        cType_dict = {'1': '1', '2': '0'}
        str1 = str1 + 'qb11num=' + cType_dict[company_type]
    if is_keep and is_keep != '0':
        if str1:
            str1 = str1 + ' and '
        is_keep_dict = {'1': '保留', '2': '剔除'}
        str1 = str1 + 'issta=' + '"' + is_keep_dict[is_keep] + '"'
    if search_content:
        if str1:
            str1 = str1 + ' and '
        if '\u4e00' <= search_content[0] <= '\u9fff':
            str1 = str1 + 'sname like ' + "'%" + search_content + "%'"
        else:
            str1 = str1 + 'susername like ' + "'%" + search_content + "%'"
    if str1:
        str1 = 'where ' + str1
    # -----------------拼接查询条件--------------
    # -----------------拼接查询生成表数据--------------
    # 建立连接并获取cursor
    with connection.cursor() as cur:
        sql = f'select * from portrait_{year}_sc {str1} limit {(pageNum-1)*pageSize},{pageSize}'
        print(sql)

        # 查询到的生成表数据
        cur.execute(sql)
        sc_cols_info = cur.description
        sc_data = cur.fetchall()
        sc_cols = [col[0] for col in sc_cols_info]
        sc_res = [
            dict(zip(sc_cols, row))
            for row in sc_data
        ]
    # 查询到的优化表数据
    year_temp = int(year)
    yh_res = {}
    with connection.cursor() as cur:
        while True:
            try:
                cur.execute(f'SELECT * FROM portrait_yh where sid="yhq{year_temp}" or sid="yhh{year_temp}" ORDER BY `sid` DESC')
                yh_cols_info = cur.description
                yh_data = cur.fetchall()
                if not yh_data:
                    break
                yh_cols = [col[0] for col in yh_cols_info]
                yh_res[str(year_temp)] = [
                    dict(zip(yh_cols, row))
                    for row in yh_data
                ]
                year_temp = year_temp-1
            except:
                break
        # 搜索到的总数
        cur.execute(f'SELECT count(1) FROM portrait_{year}_sc {str1}')
        total = cur.fetchall()

    return sc_res, yh_res, total[0][0]
