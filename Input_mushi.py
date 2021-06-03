


import xlrd
from xlutils.copy import copy

if __name__ == '__main__':
    cheng_file = r'C:\Users\小黑老弟\Desktop\实验数据\东升郊野公园\dongsheng_lvm.xls'
    my_file = r'D:\Tree\dongsheng\dongsheng\dongsheng.xls'
    data = []
    xf = xlrd.open_workbook(cheng_file)
    st = xf.sheet_by_index(1)
    for i in range(st.nrows):
        data.append([st.cell_value(i,1),st.cell_value(i,2)])
    print(data)
    rb = xlrd.open_workbook(my_file)
    wb = copy(rb)
    wsheet = wb.get_sheet(0)
    wsheet.write(1, 3, st.nrows)
    wsheet.write(1, 4, str(data))
    wb.save(my_file)
    #修改测试

