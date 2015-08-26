__author__ = 'TheJoker'
import pyodbc
from filetools import get_path, copy_file, file_exist


class EasyDatabase:
    def __init__(self, databasename):
        # set the dot location
        self.frequency = [1, 2, 3, 4, 5, 6, 7.5, 9.5]
        self.SourceDatabase = get_path() + '/Data/MyDatabase.mdb'
        self.DatabaseDB = get_path() + '/' + 'TestResult/Database/' + str(databasename) + '.mdb'
        self.BasicinfoDB = get_path() + "/Data/BasicInfo.mdb"
        self.DBHandle = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % self.DatabaseDB
        # get the database handle
        self.DBHandle = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % self.DatabaseDB

        self.DBBasicHandle = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % self.BasicinfoDB
        self.DBBasicConnection = pyodbc.connect(self.DBBasicHandle)
        self.BasicCursor = self.DBBasicConnection.cursor()
        # create the test database
        if file_exist(self.DatabaseDB):
            # connect the database
            self.TestConnection = pyodbc.connect(self.DBHandle)
            # create the database cursor
            self.Cursor = self.TestConnection.cursor()
            if self.Cursor.tables(table='TestDate').fetchone():
                self.TestSeriesNo = self.Fetchone("SELECT MAX(TestSeriesNo) FROM TestDate")[0]
                if self.TestSeriesNo is None:
                    self.TestSeriesNo = 1
                    self.Execute("INSERT INTO TestDate (TestSeriesNo, TestDate) VALUES (%d, NOW())" % self.TestSeriesNo)
                else:
                    self.TestSeriesNo += 1
                    self.Execute("INSERT INTO TestDate (TestSeriesNo, TestDate) VALUES (%d, NOW())" % self.TestSeriesNo)
            else:
                self.TestSeriesNo = 1
                self.Execute("Create TABLE TestDate(TestSeriesNo INT  NOT NULL,"
                             " TestDate DATE, PRIMARY KEY(TestSeriesNo))")
                self.Execute("INSERT INTO TestDate (TestSeriesNo, TestDate) VALUES (%d, NOW())" % self.TestSeriesNo)

        else:
            copy_file(self.SourceDatabase, self.DatabaseDB)
            # connect the database
            self.TestConnection = pyodbc.connect(self.DBHandle)
            # create the database cursor
            self.TestSeriesNo = 1
            self.Cursor = self.TestConnection.cursor()
            self.Execute("INSERT INTO TestDate (TestSeriesNo, TestDate) VALUES (%d, NOW())" % self.TestSeriesNo)

    def Commit(self):
        self.TestConnection.commit()

    def Close(self):
        self.TestConnection.close()
        self.DBBasicConnection.close()

    def Execute(self, order):
        self.Cursor.execute(order)
        self.Commit()

    def Fetchone(self, order):
        self.Cursor.execute(order)
        return self.Cursor.fetchone()

    def FetchTable(self):
        self.Cursor

    def CreateTable(self, tablename='TestTable', tablenamelist=None, tablecontent=None):
        """Create the test table, only create varchar column, update will be set not longer"""
        if not self.Cursor.tables(table=tablename).fetchone():
            self.Execute("Create TABLE %s" % tablename)
            self.Execute("alter table %s add %s INT " % (tablename, 'TestSeriesNo'))
        if tablenamelist is not None:
            length = len(tablenamelist)
            for i in range(0, length):
                if not self.Cursor.columns(table=tablename, column=str(tablenamelist[i])).fetchone():
                    self.Execute("alter table %s add %s varchar(30)" % (tablename, str(tablenamelist[i])))
        if tablecontent is not None:
            pass

    def FreqUpdate(self, freq=[], increase=True):
        if len(freq) > 0 and increase is True:
            self.frequency = self.frequency + freq
            self.frequency = set(self.frequency)
            self.frequency = sorted(self.frequency)
        elif len(freq) > 0 and increase is False:
            self.frequency = freq
            self.frequency = sorted(self.frequency)
        else:
            self.frequency = sorted(self.frequency)
        if not self.BasicCursor.tables(table='Frequency').fetchone():
            self.BasicCursor.execute("Create TABLE Frequency")
            self.BasicCursor.commit()
            self.BasicCursor.execute("alter table Frequency add ID INT NOT NULL PRIMARY KEY")
            self.BasicCursor.commit()
            self.BasicCursor.execute("alter table Frequency add Frequency DOUBLE ")
            self.BasicCursor.commit()
        self.BasicCursor.execute("DELETE FROM Frequency ")
        self.BasicCursor.commit()
        length = len(self.frequency)
        for i in range(0, length):
            self.BasicCursor.execute("INSERT INTO Frequency (ID, Frequency) VALUES (%d, %f)"
                                     % (i + 1, self.frequency[i]))
            self.BasicCursor.commit()


if __name__ == '__main__':
    databasetest = EasyDatabase('Test Database')
    databasetest.CreateTable('Frequency', ['1', '3', 4])
    databasetest.FreqUpdate([100, 23234294187], True)
    databasetest.Close()
