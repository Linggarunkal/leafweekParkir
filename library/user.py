from connection import mysqlconnection
import config

class login(object):
     def __init__(self, username, password):
         self.username = username
         self.password = password

     def user_login(self):
        try:
            __name = self.username
            __password = self.password
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            conditional_query = 'email_user = %s '
            checkUser = conn.select('testing_user', conditional_query, 'email_user, password_user', email_user=__name)
            result = len(checkUser)

            if (result > 0):
                if(str(checkUser[0][1]) == __password):
                    print("Login Berhasil")
                else:
                    print("Login gagal")
        except Exception as e:
            return "error database : %s" % e

class registration(object):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def signUp(self):
        try:
            __username = self.username
            __email = self.email
            __password = self.password

            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            before_insert = conn.check_row('testing_user')
            sign_user = conn.insert('testing_user', nama_user=__username, email_user=__email, password_user=__password)

            if before_insert <= sign_user:
                return "Registation Successfully"
            else:
                return "Registration Failed"
            print(sign_user)

        except Exception as e:
            return "Error Database : %s" % e

class getProfile(object):
    def __init__(self, username):
        self.username = username
    def profile(self):
        try:
            __username = self.username

            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            profile = 'email_user = %s'
            getProfile = conn.select('testing_user', profile, '*', email_user=__username)
            return getProfile
        except Exception as e:
            return "Error Database : %s" % e

class update_profile(object):
    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password

    def updateprofile(self):
        try:
            email = self.email
            __username = self.username
            __password = self.password

            # print(__username)
            # print(__password)


            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            email_condition = 'email_user = %s'
            getConn = conn.update('testing_user', email_condition, email, nama_user=__username, password_user=__password)

            if getConn > 0:
                return "Update Field Successfully"
            else:
                return "Update Field Failed"

        except Exception as e:
            return "Database Error : %e" % e

class forgetpasswd(object):
    def __init__(self, email_user, oldPassword, newPassword):
        self.email_user = email_user
        self.oldPassword = oldPassword
        self.newPassword = newPassword

    def getOldPassword(self):

        email_user = self.email_user
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        email_condition = 'email_user = %s'
        getUser = conn.select('testing_user', email_condition, 'email_user, password_user', email_user=email_user)
        oldPassword = getUser[0][1]
        return oldPassword

    def chPasswd(self):

        email_user = self.email_user
        oldPassword = self.oldPassword
        dbOldPassword = self.getOldPassword()
        newPassword = self.newPassword

        if oldPassword == dbOldPassword:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            email_condition = 'email_user = %s'
            updatePassword = conn.update('testing_user', email_condition, email_user, password_user=newPassword)

            if updatePassword > 0:
                return "Update Password Successfully"
            else:
                return "Update Password failed"
        else:
            return "Password Not Same"