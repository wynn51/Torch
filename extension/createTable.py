import pymysql


def create_table(table_name, data, col_line=0, start_data_line=1, end_data_line=0):
    """
    :param table_name:  表名
    :param data: 原始表数据，DataFrame型
    :param col_line:  数据库字段行在data的行数
    :param start_data_line: 第一行数据行数
    :param end_data_index:  最后一行数据行数，不设置默认则为数据表最后一行
    :return:
    """
    # 'ALTER TABLE user10 RENAME TO user11;'

    if end_data_line==0:
        end_data_line=len(data)
    data.fillna('', inplace=True)
    data = data.astype(str)
    up_data = data[start_data_line-1:end_data_line]
    # print(up_data)
    col = data.iloc[col_line-1]
    up_data.columns=col

    if len(up_data)==0:
        return '建表数据为空'
    sql_list = [f"CREATE TABLE IF NOT EXISTS {table_name} (\n"]

    for i in range(len(up_data.columns)):
        sql_col = up_data.columns[i]
        other_list = list()
        for j in range(col_line-1):
            other_list.append(str(data.iloc[j][i]))
        comment = '——'.join(other_list)
        data_len = max([len(str(k)) for k in up_data[sql_col]])

        n =1
        while True:
            if 2 ** n > data_len:
                break
            n += 1
        col_len = 2 ** (n)
        sql_list.append(
            f"{sql_col} varchar({col_len}) DEFAULT NULL COMMENT '{comment}'")
    sql_list.append(") \n ENGINE = MyISAM;")


    create_sql = sql_list[0] + ',\n'.join(sql_list[1:-1]) + sql_list[-1]

    sql_data = list()
    for i in range(0, len(up_data)):
        sql_data.append(tuple(up_data.iloc[i]))
    stmt = f"INSERT INTO {table_name} VALUES({','.join(['%s'] * len(up_data.columns))})"
    # print(create_sql)
    # db = pymysql.connect(host='127.0.0.1', user='xwj', password='123456', database='Torch1220', charset='utf8mb4')
    db = pymysql.connect(host='localhost', user='root', password='root', database='torch', charset='utf8mb4')
    try:
        cursor = db.cursor()
        cursor.execute(create_sql)
        cursor.executemany(stmt, sql_data)
        db.commit()
        db.close()

        return f'{table_name} 数据成功导入'
    except Exception as e:
        print(e)
        return '数据库建表失败，请检查表格内容，正确输入'
    finally:
        try:
            db.close()
            #return f'{table_name}数据成功导入'

        except:
            pass


if __name__ == '__main__':
    import pandas as pd
    data = pd.read_excel('./data/2019企业表数据处理.xlsx',header=None)
    create_table(table_name='2019qyb', data=data, start_data_line=2, col_line=1)

