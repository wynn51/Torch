from rest_framework.exceptions import AuthenticationFailed
import json
import re

def formula_isvalid(payload):
    print(payload['indicator_type'])
    payload['indicator_type'] = payload['indicator_type'].replace('0','跨表-简易匹配').replace('1','跨表-匹配汇总').replace('2','表内-简易计算').replace('3','表内-单条件计算').replace('4','表内-多条件计算')
    print(payload['indicator_type'])
    if payload['indicator_type'] == '表内-单条件计算' or payload['indicator_type'] == '表内-多条件计算':
        print(payload['dynamicFormula'])
        formula = payload['dynamicFormula']
        lastJustify = payload['lastJustify']
        str_f = ''
        for i in range(len(formula)):
            justify = formula[i]['justify']
            rowInput = formula[i]['rowInput']
            for j in range(len(rowInput)):
                str_f = str_f + rowInput[j]['value']
                if rowInput[j]['andor']:
                    str_f = str_f + rowInput[j]['andor'].replace('and','&').replace('or','|')
                else:
                    str_f = str_f + '?' + justify + '#'
        str_f = str_f[:-1] + '@' + lastJustify

    elif payload['indicator_type'] == '跨表-简易匹配' or payload['indicator_type'] == '跨表-匹配汇总':
        formula = payload['dynamicFormula']

        print(formula[0]['rowInput'][0]['value'])
        if len(formula[0]['rowInput'][0]['value'].split('|')) != 4:
            raise AuthenticationFailed({'info': '格式不对', 'formula': formula})
        str_f = formula[0]['rowInput'][0]['value']

    elif payload['indicator_type'] == '表内-简易计算':
        formula = payload['dynamicFormula']
        print(formula)
        str_f = formula[0]['rowInput'][0]['value']

    payload['dynamicFormula'] = str_f
    return payload
