import MySQLdb

class mysqlconnection(object):
    instance = None
    host = None
    user = None
    passwd = None
    database = None
    session = None
    connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance or not cls.database:
            cls.instance = super(mysqlconnection, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, _host='localhost', _user='root', _password='', _database='play'):
        self._host = _host
        self._user = _user
        self._password = _password
        self._database = _database

    def __open(self):
        try:
            conn = MySQLdb.connect(self._host, self._user, self._password, self._database)
            self.connection = conn
            self.session = conn.cursor()
        except MySQLdb.Error as e:
            print 'Error %d: %s' % (e.args[0], e.args[1])

    def __close(self):
        self.session.close()
        self.connection.close()

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = "SELECT "
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += ""+key+""
            if i < l:
                query += ","
            query += " FROM %s" % table

            if where:
                 query += " WHERE %s " % where

        self.__open()
        self.session.execute(query, values)

        number_rows = self.session.rowcount
        number_columns = len(self.session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.session.fetchall()]
        else:
            result = [item[0] for item in self.session.fetchall()]
        self.__close()

        return result

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
        query += " WHERE %s" % where

        self.__open()
        self.session.execute(query, values)
        self.connection.commit()

        updateRows = self.session.rowcount
        self.__close()
        return updateRows

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s" %table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(
                ["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.__open()
        self.session.execute(query, values)
        self.connection.commit()
        self.__close()

        return self.session.lastrowid

    def delete(self, table, where=None, *args, **kwargs):
        query = "DELETE FROM %s " % table
        if where:
            query += "WHERE %s " % where
        values = tuple(args)

        self.__open()
        self.session.execute(query, values)
        self.connection.commit()
        delete_rows = self.session.rowcount
        self.__close()
        return delete_rows

    def check_row(self, table):
        query = "SELECT * FROM %s" %table

        self.__open()
        self.session.execute(query)
        rownum = self.session.rowcount
        self.__close()

        return rownum

