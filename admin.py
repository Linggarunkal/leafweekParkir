from connection import mysqlconnection
import config
import geocoder
import MySQLdb


class loginAdmin(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def admin_login(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            __username = self.username
            __password = self.password

            condAdmin = 'username = %s'
            checkAdmin = conn.select('parkirenv_account', condAdmin, 'username, password', username=__username)
            resCheckAdmin = len(checkAdmin)

            if (resCheckAdmin > 0):
                if(str(checkAdmin[0][1])) == __password:
                    return 0
                else:
                    return 1

        except Exception as e:
            return "Error Database: %s" % str(e)

class facilityParkir(object):
    def __init__(self, facilityName, price, parkirenv):
        self.facilityName = facilityName
        self.price = price
        self.parkirenvID = parkirenv

    def pushFacility(self):
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        __facilityName = self.facilityName
        __price = self.price
        __parkirenv = self.parkirenvID

        condParkirEnv = 'username = %s'
        getParkirEnvAccID = conn.select('parkirenv_account', condParkirEnv, 'parkirEnvAccount_id', username=__parkirenv)

        __facilityAdd = conn.insert('facility_parkir', nama_facility=__facilityName, Price=__price, parkirEnvAccount_id=getParkirEnvAccID)

        if __facilityAdd == 0:
            return 0
        else:
            return 1


class facilityUpdate(object):
    def __init__(self, facility_id, nama_facility, price):
        self.facility_id = facility_id
        self.nama_facility = nama_facility
        self.price = price

    def updateFacility(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condFacility = 'facility_id = %s'
            __updateFacility = conn.update('facility_parkir', condFacility, self.facility_id, nama_facility=self.nama_facility, price=self.price)
            return __updateFacility
        except Exception as e:
            return "Error Databases: %s" % str(e)

class removeFacility(object):
    def __init__(self, facility_id):
        self.facility_id = facility_id

    def facilityRemove(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condFacility = 'facility_id = %s'
            __removeFacility = conn.delete('facility_parkir', condFacility, self.facility_id)
            return __removeFacility
        except Exception as e:
            return "Error Databases: %s" % str(e)


class cashierParkir(object):
    def __init__(self, name, username, password, parkirenv):
        self.name = name
        self.username = username
        self.password = password
        self.parkirAccount = parkirenv

    def pushCashier(self):
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

        condParkirEnv = 'username = %s'
        getParkirEnvAccID = conn.select('parkirenv_account', condParkirEnv, 'parkirEnvAccount_id', username=self.parkirAccount)

        __cashierAdd = conn.insert('cashier_parkir', name=self.name, username=self.username, password=self.password, parkirEnvAccount_id=getParkirEnvAccID)

        if __cashierAdd == 0:
            return 0
        else:
            return 1

class cashierUpdate(object):
    def __init__(self, cashier_id, name, username, password):
        self.cashier_id = cashier_id
        self.name = name
        self.username = username
        self.password = password

    def updateCashier(self):
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        condCashier = 'cashier_id = %s'
        __cashierUpdate = conn.update('cashier_parkir', condCashier, self.cashier_id, name=self.name, username=self.username, password=self.password)
        return  __cashierUpdate


class removeCashier(object):
    def __init__(self, cashier_id):
        self.cashier_id = cashier_id

    def cashierRemove(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condCashier = 'cashier_id = %s'
            __removeCashier = conn.delete('cashier_parkir', condCashier, self.cashier_id)
            return _-__removeCashier
        except Exception as e:
            return "Error Database: %s" % str(e)


class updateParkirEnv(object):
    def __init__(self, username, parkirName, address, maxHour, fee, maxFee, startParkir, endParkir):
        self.username = username
        self.parkirName = parkirName
        self.address = address
        self.maxHour = maxHour
        self.fee = fee
        self.maxFee = maxFee
        self.startParkir = startParkir
        self.endParkir = endParkir

    def parkirUpdate(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            __loc = geocoder.google(self.address)
            __location = __loc.latlng
            __lat = __location[0]
            __lng = __location[1]

            condPark = 'username = %s'
            __parkUpdate = conn.update('parkirenv_account', condPark, self.username, nama_parkir=self.parkirName, feePer_hour=self.fee, maxHour=self.maxHour, maxFee=self.maxFee, address=self.address, Langitude=__lat, longitude=__lng, start_parkir=self.startParkir, end_parkir=self.endParkir)
            return __parkUpdate
        except Exception as e:
            return "Error Database: %s" % str(e)

class cashierLogin(object):
    def __init__(self, usernameCashier, passwordCashier):
        self.usernameCashier = usernameCashier
        self.passwordCashier = passwordCashier

    def loginCashier(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condCashier = 'username = %s'
            getCashier = conn.select('cashier_parkir', condCashier, 'username, password', username=self.usernameCashier)
            print(len(getCashier))
            if len(getCashier) == 1:
                if getCashier[0][1] == self.passwordCashier:
                    #login success
                    return 0
                else:
                    #wrong password or username
                    return 1
            else:
                #failed login
                return 2
        except Exception as e:
            return "Error Database: %s" % str(e)


class transactionIn(object):
    def __init__(self, gateParkirId, plateNumber, startTime, statusParkir):
        self.gateID = gateParkirId
        self.plateNumber = plateNumber
        self.startTime = startTime
        self.statusParkir = statusParkir
        print(self.gateID, self.plateNumber, self.startTime, self.statusParkir)

    def pushGateIn(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condPlate = 'platenumber_code = %s'
            getStatusPlate = conn.select('v_transaction', condPlate, 'account_id, platenumber_code', plateNumber_code=self.plateNumber)
            if len(getStatusPlate) == 0:
                transIn = conn.insert('transaction', gateParkir_id=self.gateID, plateNumber_code=self.plateNumber, start_time=self.startTime, status_parkir=self.statusParkir, status_plate="Non Member", PaymentMethod="Cash")
                print(transIn)
                if transIn == 0:
                    return ({'status': 200, 'message': 'Success add transaction Gate In Parkir'})
                else:
                    return ({'status': 400, 'message': 'Failed add transaction Gate In Parkir'})
            elif len(getStatusPlate) == 1:
                condPayment = 'platenumber_code = %s'
                getPaymentMethod = conn.select('v_transaction', condPayment, 'paymentmethod_name', plateNumber_code=self.plateNumber)
                transIn = conn.insert('transaction', gateParkir_id=self.gateID, plateNumber_code=self.plateNumber,
                                      start_time=self.startTime, status_parkir=self.statusParkir,
                                      status_plate="Member", PaymentMethod=getPaymentMethod)
                if transIn == 0:
                    return ({'status': 200, 'message': 'Success add transaction Gate In Parkir'})
                else:
                    return ({'status': 400, 'message': 'Failed add transaction Gate In Parkir'})

        except Exception as e:
            return "Error Database: %s" % str(e)

class transactionOut(object):
    def __init__(self, gateId, plateNumber, timeEnd, statusParkir, transaction_id):
        self.gateId = gateId
        self.plateNumber = plateNumber
        self.timeEnd = timeEnd
        self.statusParkir = statusParkir
        self.transaction_id = transaction_id
        self.transName = "Payment User Parking"
        self.transSource = "Wallet Payment User Parking"
        self.statusWallet = "Wallet"

        print(self.plateNumber)

        # print(self.gateId, self.plateNumber, self.timeEnd, self.statusParkir)

    def pushGateOut(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condPayment = 'plateNumber_code = %s'
            getPaymentMethod = conn.select('transaction', condPayment, 'PaymentMethod', plateNumber_code=self.plateNumber)
            print(getPaymentMethod)

            if getPaymentMethod[0] == 'Cash':
                condTrans = 'transaction_id = %s'
                transOut = conn.update('transaction', condTrans, self.transaction_id, status_parkir=self.statusParkir, end_time=self.timeEnd, status_payment="confirmation")
                print(transOut)
                if transOut == 1:

                    return ({'status': 200, 'message': 'Transaction confirmation By Cashier'})
                else:
                    return ({'status': 400, 'message': 'Transaction Failed'})
            elif getPaymentMethod[0] == 'Wallet':
                print(self.transaction_id +"tahu")

                condTransaction = 'transaction_id = %s'
                transOut = conn.update('transaction', condTransaction, self.transaction_id, status_parkir=self.statusParkir, end_time=self.timeEnd,status_payment="success")
                if transOut == 1:
                    condGetAccountId = 'transaction_id = %s'
                    getAccountId = conn.select('v_detailtransaction', condGetAccountId, 'parkirEnvAccount_id',transaction_id=self.transaction_id)
                    getAccountfee = conn.select('v_detailtransaction', condGetAccountId, 'TotalFee', transaction_id=self.transaction_id)
                    sendWalletPay = conn.insert('parkirowner_wallet', transaction_name=self.transName, kredit=getAccountfee, status=self.statusWallet, parkirEnvAccount_id=getAccountId, source_transaction=self.transSource)
                    getPlateNumber = conn.select('v_detailtransaction',condGetAccountId, 'plateNumber_code', transaction_id=self.transaction_id)
                    plate = getPlateNumber[0]
                    condPlate = 'plateNumber_code = %s'
                    getUserAccountId = conn.select('v_accountDebit', condPlate, 'account_id', plateNumber_code=plate)
                    print(getUserAccountId)
                    sendUserWallet = conn.insert('parkpay_wallet', transaction_name=self.transName, debit=getAccountfee, account_id=getUserAccountId, source_transaction=self.transSource)

                    if sendUserWallet == 0:
                        return ({'status': 200, 'message': 'Transaction Success'})
                    else:
                        return ({'status': 400, 'message': 'Transaction Failed'})
                else:
                    return ({'status': 400, 'message': 'Transaction Failed'})



        except Exception as e:
            return "Error Database push gate: %s" % str(e)


class getDetailPayment(object):
    def __init__(self, plateNumber):
        self.plateNumber =  plateNumber

    def getPaymentMethod(self):
        try:
            conn = MySQLdb.connect(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            cursor = conn.cursor()
            cursor.execute('select transaction_id, paymentMethod from v_detailTransaction where status_parkir = "In" and platenumber_code = "'+self.plateNumber+'"')
            data = cursor.fetchall()
            if len(data) > 0:
                return data
            else:
                return "Data Not Found"
        except Exception as e:
            return "Error Database: %s" % str(e)

class payCash(object):
    def __init__(self, transaction_id):
        self.transaction_id = transaction_id

    def getCashTrans(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condGetCash = 'transaction_id = %s'
            getCashDetail = conn.select('v_detailTransaction', condGetCash, 'transaction_id, plateNumber_code, TotalFee, TotalTime, start_time, end_time, paymentMethod', transaction_id=self.transaction_id)
            if len(getCashDetail) == 1:
                return getCashDetail
            else:
                return "Data Not Found"

        except Exception as e:
            return "Error Database: %s" % str(e)

class cashPayment(object):
    def __init__(self, transactionId, plateNumber, fee):
        self.transactionId = transactionId
        self.plateNumber = plateNumber
        self.fee = fee
        self.statusPayment = "success"
        self.transName = "Payment User Parking"
        self.transSource = "Cash Payment User Parking"
        self.statusWallet = "Cash"

    def cashSubmit(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

            condCashPay = 'transaction_id = %s'
            cashPay = conn.update('transaction', condCashPay, self.transactionId, status_payment=self.statusPayment)
            if cashPay == 1:
                #add fee to jurnal wallet parkir owner
                condTransId = 'transaction_id = %s'
                getParkirOwnerId = conn.select('v_detailtransaction', condTransId, 'parkirEnvAccount_id', transaction_id=self.transactionId)
                #insert to jurnal waller kredit
                sendWalletPay = conn.insert('parkirOwner_wallet', transaction_name=self.transName, kredit=self.fee, status= self.statusWallet, parkirEnvAccount_id=getParkirOwnerId, source_transaction=self.transSource)
                if sendWalletPay == 0:
                    return 0
                else:
                    return 1
            else:
                return 1
        except Exception as e:
            return "Error Database: %s" % str(e)

class balanceParkirOwner(object):
    def __init__(self, username):
        self.username = username

    def cashBalanace(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condPay = 'status = %s'
            cashpay = conn.select('v_balanceParkirOwner', condPay, 'balance', status='Cash')

            if len(cashpay) > 0:
                return cashpay
            else:
                return "Data Not Found"

        except Exception as e:
            return "Error Databases: %s" % str(e)
    def walletBalance(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condwallet = 'status = %s'
            walletpay = conn.select('v_balanceParkirOwner', condwallet, 'balance', status='Wallet')

            if len(walletpay) > 0:
                return walletpay
            else:
                return "Data Not Found"

        except Exception as e:
            return "Error Databases: %s" % str(e)

    def totalBalance(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condTotalAccount = 'username = %s'
            totalpay = conn.select('v_totalBalanceAccount', condTotalAccount, 'balance', username=self.username)

            if len(totalpay) > 0:
                return totalpay
            else:
                return "Data Not Found"

        except Exception as e:
            return "Error Databases: %s" % str(e)


class reportParkir(object):
    def __init__(self, username):
        self.username = username

    def parkirSuccess(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condSuccess = 'status_payment = %s'
            getParkirSuccess = conn.select('v_detailtransaction', condSuccess, 'transaction_id, plateNumber_code, start_time, end_time, status_plate, paymentMethod, TotalTime, TotalFee', status_payment='success')

            if len(getParkirSuccess) > 0:
                return getParkirSuccess
            else:
                return "Data Not Found"
        except Exception as e:
            return "Error Database: %s" % str(e)
    def parkirUser(self):
        try:
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            condParkir = 'username = %s'
            getParkir = conn.select('v_parkirUser', condParkir, '*', username=self.username)

            if len(getParkir) > 0:
                return getParkir
            else:
                return 0
        except Exception as e:
            return "Error Database: %s" % str(e)

    def countParkir(self):
        try:
            conn = MySQLdb.connect(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            cursor = conn.cursor()
            cursor.execute('select count(*) from v_parkirUser where username = "'+self.username+'"')
            data = cursor.fetchall()
            if len(data) > 0:
                return data
            else:
                return "Data Not Found"
        except Exception as e:
            return "Error Database: %s" % str(e)

    def countParkirOut(self):
        try:
            conn = MySQLdb.connect(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            cursor = conn.cursor()
            cursor.execute('select count(*) from v_parkirOut where username = "'+self.username+'"')
            data = cursor.fetchall()
            if len(data) > 0:
                return data
            else:
                return "Data Not Found"
        except Exception as e:
            return "Error Database: %s" % str(e)