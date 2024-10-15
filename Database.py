import pymysql

class Database:
    def __init__(self,host,user,password,database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def user_register(self,user):
        con = None
        cursor = None
        temp = False

        try:
            con = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            cursor = con.cursor()

            sql = "INSERT INTO Users(user_id,email,password) VALUES(LAST_INSERT_ID(),%s,%s)"
            args = (user.email,user.password)
            cursor.execute(sql,args)
            temp = True
            con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return temp

    def user_login(self,user):
        con = None
        cursor = None
        temp = False

        try:
            con = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            cursor = con.cursor()

            sql = "SELECT * FROM Users WHERE email=%s AND password=%s"
            args = (user.email,user.password)
            res = cursor.execute(sql,args)
            if res:
                temp = True
                con.commit()

        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return temp


    def display_contacts(self,email):
        con = None
        cursor = None
        contact = []
        try:
            con = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            cursor = con.cursor()

            sql = "SELECT user_id FROM Users WHERE email=%s"
            args = (email,)
            res = cursor.execute(sql,args)
            if res:
                x = cursor.fetchone()
                sql = "SELECT * FROM Contacts WHERE user_id =%s"
                args = (x,)
                cursor.execute(sql,args)
                row = cursor.fetchall()
                for i in row:
                    cont = [i[0], i[1], i[2], i[3]]
                    contact.append(cont)
                con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return contact


    def add_contact(self,email,c):
        con = None
        cursor = None
        temp = False

        try:
            con = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database)
            cursor = con.cursor()

            sql = "SELECT user_id FROM Users WHERE email=%s"
            args = (email,)
            res = cursor.execute(sql, args)
            if res:
                x = cursor.fetchone()
                sql = "INSERT INTO Contacts(user_id,name,mobile,city) VALUES(%s,%s,%s,%s)"
                args = (x,c.name,c.mobile,c.city)
                cursor.execute(sql,args)
            con.commit()
            temp = True
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return temp

    def delete_contact(self,email,c):
        con = None
        cursor = None
        temp = False

        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            sql = "SELECT user_id FROM Users WHERE email=%s"
            args = (email,)
            res = cursor.execute(sql, args)
            if res:
                x = cursor.fetchone()
                sql = " Delete from Contacts WHERE user_id = %s AND name =%s OR mobile =%s OR city=%s "
                args = (x,c.name,c.mobile,c.city)
                cursor.execute(sql, args)
            con.commit()
            temp = True
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return temp

    def search_name(self,email):
        con = None
        cursor = None
        contact = []
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            sql = "SELECT user_id FROM Users WHERE email=%s"
            args = (email,)
            res = cursor.execute(sql, args)
            if res:
                x = cursor.fetchone()
                sql = "SELECT * FROM Contacts WHERE user_id =%s"
                args = (x,)
                cursor.execute(sql, args)
                row = cursor.fetchall()
                for i in row:
                    cont = [i[1], i[2], i[3]]

                    contact.append(cont)
                con.commit()
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return contact


    def update(self,ex,email,c):
        con = None
        cursor = None
        temp = False

        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            cursor = con.cursor()

            sql = "SELECT user_id FROM Users WHERE email=%s"
            args = (email,)
            res = cursor.execute(sql, args)
            if res:
                x = cursor.fetchone()
                sql = "UPDATE Contacts SET name = %s , mobile = %s , city = %s WHERE user_id = %s AND name = %s"
                args = (c.name,c.mobile,c.city,x,ex)
                cursor.execute(sql, args)
            con.commit()
            temp = True
        except Exception as e:
            print(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if con is not None:
                con.close()
            return temp

