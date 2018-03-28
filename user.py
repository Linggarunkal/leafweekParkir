from connection import mysqlconnection
import config
import MySQLdb

class loginUser(object):
     def __init__(self, email, password):
         self.email = email
         self.password = password

     def user_login(self):
        try:
            __email = self.email
            __password = self.password

            print(__email, __password)
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            conditional_query = 'email = %s '
            checkUser = conn.select('user', conditional_query, 'email, password', email=__email)
            result = len(checkUser)

            if (result > 0):
                if(str(checkUser[0][1]) == __password):
                    return 0
                else:
                    return 1
        except Exception as e:
            return "error database : %s" % e

class registration(object):
    def __init__(self, firstname, lastname, email, password, telp, plateNumber, city):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.telp = telp
        self.plate = plateNumber
        self.city = city



    def signUp(self):
        try:
            __firstname = self.firstname
            __lastname = self.lastname
            __email = self.email
            __password = self.password
            __telp = self.telp
            __plate = self.plate
            __city = self.city

            print(__firstname, __lastname, __email, __password, __telp, __plate, __city)
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

            sign_user = conn.insert('user', firstname=__firstname, lastname=__lastname, email=__email, password=__password)




            if sign_user == 0:
                userCondition = 'email = %s'
                getUser_id = conn.select('user', userCondition, 'user_id', email=__email)
                print(getUser_id)
                plate_number = conn.insert('platenumber_user', platenumber_code=__plate, user_id=getUser_id)
                insertAccount = conn.insert('account', phoneNumber=__telp, city_id=__city, user_id=getUser_id)
                print(plate_number)
                print(insertAccount)

                if plate_number and insertAccount == 0:
                    return "Data Success Save to System"
                else:
                    return "Data Failed Save to System"



        except Exception as e:
            return "Error Database : %s" % e

class getProfile(object):
    def __init__(self, email):
        self.email = email
    def profile(self):
        try:
            __email = self.email

            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            profile = 'email = %s'
            getProfile = conn.select('v_user', profile, 'user_id, firstname, lastname, identityType, identityNumber, gender, city_name, city_id, phoneNumber, email', email=__email)
            resProfile = len(getProfile)

            if resProfile > 0:
                return getProfile
            else:
                return "Get Profile Failed from System"
        except Exception as e:
            return "Error Database : %s" % e



class update_profile(object):
    def __init__(self, user_id, firstname, lastname, identityNumber, identityType, gender, city, plate):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.identityNumber = identityNumber
        self.identityType = identityType
        self.gender = gender
        self.city = city
        self.plate = plate

    def updateprofile(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

            __user_id = self.user_id
            __firstname = self.firstname
            __lastname = self.lastname
            __identityNumber = self.identityNumber
            __identityType = self.identityType
            __gender = self.gender
            __city = self.city
            __plate = self.plate

            print(__city)

            conditionUpdate = 'user_id = %s'
            updateProfile = conn.update('user', conditionUpdate, __user_id, firstname=__firstname, lastname=__lastname)
            resUpdateProfile = updateProfile
            print('user %s' % resUpdateProfile)

            if resUpdateProfile == 0 or resUpdateProfile == 1:
                condAccount = 'user_id = %s'
                accUpdate = conn.update('account', condAccount, __user_id, identityType=__identityType, identityNumber=__identityNumber, gender=__gender, city_id=__city)
                print('account %s' % accUpdate)

                if accUpdate == 0 or accUpdate == 1:
                    condPlate = 'user_id = %s'
                    plateUpdate = conn.update('platenumber_user', condPlate, __user_id, plateNumber_code=__plate)
                    print('plate number %s' % plateUpdate)
                    if plateUpdate == 0 or plateUpdate == 1:
                        return "Update Data Successfull to System"
                    else:
                        return "Update Data Failed to System"

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

class topup(object):
    def __init__(self, provider, nominal, email):
        self.provider = provider
        self.nominal = nominal
        self.email = email

    def topupUpdate(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

            __provider = self.provider
            __nominal = self.nominal
            __email = self.email
            __transactionName = "Topup ParkPay Wallet"

            # condProvider = 'provide_topup = %s'
            # getProviderId = conn.select('topup_choose', condProvider, 'topupChoose_id', provide_topup=__provider)
            condAccountId = 'email = %s'
            getAccountID = conn.select('v_user', condAccountId, 'account_id', email=__email)


            topupWallet = conn.insert('parkpay_wallet', transaction_name=__transactionName, kredit=__nominal, account_id=getAccountID, source_transaction=__provider)
            print(topupWallet)
            if topupWallet == 0:
                return "Topup Successfully"
            else:
                return "Topup Failed"

        except Exception as e:
            return "Error Database: %s" % str(e)


class paymentUpdate(object):
    def __init__(self, payment, email):
        self.payment = payment
        self.email = email

    def paymentUpdateUser(self):
        try:
            __payment = self.payment
            __email = self.email

            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condAccountID = 'email = %s'
            getAccountId = conn.select('v_user', condAccountID, 'account_id', email=__email)
            condUserUpdate = 'account_id = %s'
            userUpdate = conn.update('account',condUserUpdate, getAccountId, paymentMethod_id=__payment)
            if userUpdate == 1:
                return "Update Payment Method Sucessfully to System"
            else:
                return "Update Payment Method Failed to System"

        except Exception as e:
            return "Error Database: %s" % str(e)


class historyUser(object):
    def __init__(self, email):
        self.email = email

    def getHistory(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condHistory = 'email = %s'
            getHist = conn.select('v_historyUser', condHistory, 'transaction_id, paymentMethod_name, plateNumber_code, start_time, end_time, status_payment, nama_parkir', email=self.email)
            print(len(getHist))
            if len(getHist) > 0:
                return getHist
            else:
                return "Error Get Detail History User"
        except Exception as e:
            return "Error Database: %s" % str(e)

