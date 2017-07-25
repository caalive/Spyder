#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 17/07/22 10:05 AM
# Author : CA

import xlsxwriter

workbook = xlsxwriter.Workbook('ex1format.xlsx')
worksheet = workbook.add_worksheet('test')

#add a bold format to use to highlight cells
money = workbook.add_format({'num_format': '$#,##0'})
bold = workbook.add_format({'bold': True})
#write sone data headers.
worksheet.write('A1', 'Item', bold)
worksheet.write('B1', 'Cost', bold)

#some data we want to write the worksheet

expenses = (['Rent', 1000],
            ['Gas', 100],
            ['Food', 300],
            ['Gym', 50]
            )

#start fronm the first cell below the headers
row = 1
col = 0

#iterate over the data and write it out row by row
for item, cost in (expenses):
    worksheet.write(row, col, item)
    worksheet.write(row, col+1, cost, money)
    row += 1

#write a total using a formula
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 1, '=SUM(B2:B5)', money)

workbook.close()



