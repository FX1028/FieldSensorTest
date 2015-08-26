__author__ = 'TheJoker'
from filetools import get_path

from win32com.client import Dispatch


class EasyWord:
    """Print word application definition"""

    def __init__(self, filename='校准报告', report=True, lang=0):
        """initialise the word application,then return the word handle"""
        if report:
            if lang == 0:
                self.reportpath = get_path() + '\Data\Report_cn.dot'
            elif lang == 1:
                self.reportpath = get_path() + '\Data\Report_en.dot'
            else:
                self.reportpath = get_path() + '\Data\Report_encn.dot'
        else:
            self.reportpath = get_path() + '\Data\Original.dot'
        self.wordapp = Dispatch('Word.Application')
        self.wordapp.Visible = 1
        self.worddoc = self.wordapp.Documents.Add(Template=self.reportpath)  # import the report template file
        self.myRange = self.worddoc.Range(0, 0)
        self.tablenum = self.worddoc.Paragraphs.Count
        if report:
            self.reportpath = get_path() + '/TestResult/' + filename
        else:
            self.reportpath = get_path() + '/TestResult/Original/' + filename + '_Original'

    def DocSave(self):
        self.worddoc.SaveAs(self.reportpath)

    def DocClose(self, changemodel=0):
        self.worddoc.Close(SaveChanges=changemodel)
        self.wordapp.Quit()

    def TableInsert(self, rng, row, column):
        self.worddoc.Tables.Add(rng, row, column)

    def TableContent(self, tablenum, cellrow, cellcolum, insertcontent):
        tab = self.worddoc.Tables[tablenum]
        cel = tab.Cell(cellrow, cellcolum)
        rng = cel.Range
        rng.Text = insertcontent

    def TablenumUpdate(self):
        self.tablenum = self.worddoc.Paragraphs.Count


if __name__ == '__main__':
    wordprint = EasyWord('123', False)
    wordprint.TableInsert(wordprint.myRange, 3, 4)
    wordprint.TableContent(0, 2, 2, 'adshkkljjl')
    wordprint.DocSave()
    wordprint.DocClose()
