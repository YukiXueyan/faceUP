import os
import xlwt
import xlrd

workBook = xlwt.Workbook(encoding='utf-8')
count = 0
col = 0
path = 'Face2.xls'

def readExcel():
    document = xlrd.open_workbook(path)
    allSheetNames = document.sheet_names()
    print(allSheetNames)

    for i in range(len(allSheetNames)):
            workSheet = workBook.add_sheet(allSheetNames[i])
            writeTitle(workSheet)
            content = document.sheet_by_index(i)
            print(content.name,content.nrows,content.ncols)

            data = []
            for a in range(content.nrows):
                cells = content.row_values(a)
                data.append(cells[12])   #第12列是该图片的情绪类别编号

            del data[0]
            print(data)
            writeEmotion(workSheet,data)

    workBook.save('./filmRating/excelData/emotion.xls')
    print('处理完毕')

def writeTitle(sheet):

    title = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7','p8', 'p9']
    for col in range(len(title)):
        sheet.write(0, col, title[col])

def writeEmotion(sheet,data):
    global count
    row = 1
    col = 0
    for i in data:
        count += 1
        if (col < 9):
            sheet.write(row, col, i)
            print("这是第"+str(row)+"行，第"+str(col)+"列")
            col += 1
        else:
            row += 1
            col = 0
            sheet.write(row, col, i)
            print("这是第" + str(row) + "行，第" + str(col) + "列")
            col += 1

if __name__ == '__main__':
        readExcel()
        print(count)











