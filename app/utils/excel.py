import io
from typing import List

import xlsxwriter


def export_excel(submissions: List) -> io.BytesIO:
    output = io.BytesIO()
    workBook = xlsxwriter.Workbook(output)
    workSheet = workBook.add_worksheet("default")
    workSheet.write_row("A1", ["ID", "姓名", "学号", "学生ID", "文件名", "原始文件名", "代码", "日志", "状态", "分数", "结果", "实验ID"])
    row = 1
    for submission in submissions:
        workSheet.write(row, 0, submission.id)
        workSheet.write(row, 1, submission.user.name)
        workSheet.write(row, 2, submission.user.student_id)
        workSheet.write(row, 3, submission.user_id)
        workSheet.write(row, 4, submission.filename)
        workSheet.write(row, 5, submission.origin_filename)
        workSheet.write(row, 6, submission.code)
        workSheet.write(row, 7, submission.log)
        workSheet.write(row, 8, submission.status)
        workSheet.write(row, 9, submission.total_score)
        workSheet.write(row, 10, submission.result)
        workSheet.write(row, 11, submission.lab_id)
        row += 1
    workBook.close()
    output.seek(0)
    return output
