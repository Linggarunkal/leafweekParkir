from flask import Flask, render_template, request, session, g, redirect, url_for, jsonify, json, flash
import os
import hashlib
import config
from connection import mysqlconnection
from admin import loginAdmin, facilityParkir, facilityUpdate, removeFacility, cashierParkir, cashierUpdate, removeCashier, updateParkirEnv, cashierLogin, transactionIn, transactionOut, getDetailPayment, payCash, cashPayment, balanceParkirOwner, reportParkir
from datetime import datetime
from flask_restful import reqparse
import decimal



app = Flask(__name__)
app.secret_key = os.urandom(24)

#set Global variable

transDetail = None



##admin site environment
@app.route("/admin/home")
def adminHome():
    return render_template('admin/index.html')

@app.route("/admin/postLogin", methods=['POST'])
def adminPostLogin():
    try:
        __username = request.form['username']
        __password = request.form['password']
        __hashPassword = hash_password(__password)

        print(__username, __password, __hashPassword)
        adminLogin = loginAdmin(__username, __hashPassword)
        checkLogin = adminLogin.admin_login()

        if (checkLogin == 0):
            return redirect(url_for('adminDasboard'))
        else:
            flash('Wrong password or Email')
            return redirect(url_for('adminHome'))
    except Exception as e:
        return "Error Databases: %s" % str(e)

@app.route("/admin/dasboard")
def adminDasboard():
    username = 'mercuPark'
    getCash = balanceParkirOwner(username)
    cashTotal = getCash.cashBalanace()
    cashFee = decimal.Decimal(cashTotal[0])
    convertFee = str(cashFee)

    getWallet = balanceParkirOwner(username)
    walletTotal = getWallet.walletBalance()
    walletFee = decimal.Decimal(walletTotal[0])
    convertWallet = str(walletFee)

    getTotalBalance = balanceParkirOwner(username)
    totalBalance = getTotalBalance.totalBalance()
    totalFee = decimal.Decimal(totalBalance[0])
    convertTotal = str(totalFee)


    countActivaParkir = reportParkir(username)
    getCountActiveParkir = countActivaParkir.countParkir()
    activeUser = str(getCountActiveParkir[0][0])

    countOutParkir = reportParkir(username)
    getCountOutParkir = countOutParkir.countParkirOut()
    outParkir = str(getCountOutParkir[0][0])

    return render_template('admin/dasboard.html', cash=convertFee, wallet=convertWallet, total=convertTotal, username=username, activeUser=activeUser, outParkir=outParkir)


@app.route("/admin/reportTransaction")
def adminReportTrans():
    username = 'mercuPark'
    succesReport = reportParkir(username)
    getSuccessReport = succesReport.parkirSuccess()
    print(getSuccessReport)
    detailList = []

    for index, list in enumerate(getSuccessReport):

        start_time = str(list[2])
        end_time = str(list[3])
        timeTotal = decimal.Decimal(list[6])
        timeTot = str(timeTotal)
        feeTotal = decimal.Decimal(list[7])
        totFee = str(feeTotal)
        print(start_time, end_time, timeTot, totFee)

        i = {
            'transaction_id': list[0],
            'plateNumber': list[1],
            'start_time': start_time,
            'end_time': end_time,
            'status_plate': list[4],
            'status_payment': list[5],
            'total_time': timeTot,
            'total_fee': totFee
        }
        detailList.append(i)
        countData = len(detailList)
    return render_template('admin/report_transaction.html', reportDetail=detailList, username=username, countData=countData)

@app.route("/admin/reportUserParking")
def adminReportUserParking():
    username = 'mercuPark'

    parkirUser = reportParkir(username)
    getParkirUser = parkirUser.parkirUser()
    print(getParkirUser)


    if getParkirUser > 0:
        detailGetParkirUser = []
        for index, list in enumerate(getParkirUser):
            i = {
                'transaction_id': list[0],
                'plateNumber': list[1],
                'statusPlate': list[2],
                'start_time': str(list[3]),
                'paymentMethod': list[4]
            }
            detailGetParkirUser.append(i)
        return render_template('admin/report_user_parking.html', getParkir=detailGetParkirUser, username=username)
    else:
        detailGetParkirUser = []
        return render_template('admin/report_user_parking.html', getParkir=detailGetParkirUser, username=username)



@app.route("/admin/facility")
def adminFacility():
    username = "mercuPark"
    conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
    condUsername = 'username = %s'
    getFacilityParkir = conn.select('v_facilityParkir', condUsername, 'facility_id, nama_facility, price', username=username)
    return render_template('admin/manage_facility.html', listFacility=getFacilityParkir, username=username)


@app.route("/admin/addFacility", methods=['POST'])
def adminAddFacility():
    try:
        username = "mercuPark"
        __facilityName = request.form['facilityName']
        __price = request.form['price']

        facilityAdd = facilityParkir(__facilityName, __price, username)
        resFacilityAdd = facilityAdd.pushFacility()

        if resFacilityAdd == 0:
            flash("Add Facility Parkir Successfull to System")
            return redirect(url_for('adminFacility'))
        else:
            flash("Add Facility Parkir Failed to System")
            return redirect(url_for('adminFacility'))

    except Exception as e:
        return "Error Databases: %s" % str(e)


@app.route('/admin/manageEditFacility', methods=['POST'])
def adminManageEditFacility():
    try:
        if request.method == 'POST':
            conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            __facility_id = request.form['delList']
            condFacility = 'facility_id = %s'
            getDetailFacility = conn.select('v_facilityParkir', condFacility, 'facility_id, nama_facility, price', facility_id=__facility_id)
            detailFacility = []
            for list in getDetailFacility:
                i = {
                    'facility_id': list[0],
                    'nama_facility': list[1],
                    'price': list[2]
                }
                detailFacility.append(i)
                listDetailFacility = json.dumps(detailFacility)

        return render_template("admin/manage_facility_edit.html", facility=listDetailFacility)

    except Exception as e:
        return "Error Databases: %s" % str(e)


@app.route("/admin/manageUpdateFacility", methods=['POST'])
def adminManageUpdateFacility():
    try:
        __facility_id = request.form['facility_id']
        __nama_facility = request.form['nama_facility']
        __price = request.form['price']

        sendUpdateFacility = facilityUpdate(__facility_id, __nama_facility, __price)
        resUpdateFacility = sendUpdateFacility.updateFacility()
        if resUpdateFacility == 1:
            flash("Update Facility Parkir Successfully")
            return redirect(url_for('adminFacility'))
        else:
            flash("Update Facility Parkir Failed")
            return redirect(url_for('adminFacility'))
    except Exception as e:
        return "Error Databases: %s" % str(e)


@app.route("/admin/manageRemove/facility", methods=['POST'])
def adminManageRemoveFacility():
    try:
        __facility_id = request.form['removeList']

        sendFacility = removeFacility(__facility_id)
        resFacility = sendFacility.facilityRemove()
        if resFacility == 1:
            flash("Delete Facility Parkir Successfully")
            return redirect(url_for('adminFacility'))
        else:
            flash("Delete Facility Parkir Successfully")
            return redirect(url_for('adminFacility'))
    except Exception as e:
        return "Error Databases: %s" % str(e)


@app.route("/admin/manageParkir")
def adminManageParkir():
    username = "mercuPark"
    conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
    condPark = 'username = %s'
    viewPark = conn.select('parkirenv_account', condPark, 'nama_parkir, address, maxHour, feePer_hour, maxFee, start_parkir, end_parkir', username=username)
    listPark = []
    for list in viewPark:
        i={
            'nama_parkir': list[0],
            'address': list[1],
            'maxHour': list[2],
            'fee': list[3],
            'maxFee': list[4],
            'start_parkir': list[5],
            'end_parkir': list[6]
        }
        listPark.append(i)
        start_time = listPark[0]['start_parkir']
        startConvert = datetime.strptime(str(start_time), "%H:%M:%S")
        timeStart = startConvert.strftime("%I:%M %p")


        end_time = listPark[0]['end_parkir']
        print(end_time)
        endConvert = datetime.strptime(str(end_time), "%H:%M:%S")
        timeEnd = endConvert.strftime("%I:%M %p")

        listPark[0]['start_parkir'] = timeStart
        listPark[0]['end_parkir'] = timeEnd

        parkList = json.dumps(listPark)

    return render_template('admin/manage_parking.html', parkList=parkList, username=username)


@app.route("/admin/manageUpdateParkir", methods=['POST'])
def adminManageUpdateParkir():
    username="mercuPark"
    __namaParking = request.form['parking_name']
    __address = request.form['parking_address']
    __max_hour = request.form['max_hour']
    __fee = request.form['fee']
    __max_fee = request.form['max_fee']
    __start = request.form['start']
    __end = request.form['end']
    timeStart = datetime.strptime(__start, "%I:%M %p")
    startTime = timeStart.strftime("%H:%M:%S")
    timeEnd = datetime.strptime(__end, "%I:%M %p")
    endTime = timeEnd.strftime("%H:%M:%S")
    print(__namaParking, __address, __max_hour, __fee, __max_fee, startTime, endTime)

    sendUpdateParkir = updateParkirEnv(username, __namaParking, __address, __max_hour, __fee, __max_fee, startTime, endTime)
    resUpdateParkir = sendUpdateParkir.parkirUpdate()
    print(resUpdateParkir)

    if resUpdateParkir == 1:
        flash("Update Parkir Environment Successfull")
        return redirect(url_for('adminManageParkir'))
    else:
        flash("Update Parkir Environment Failed")
        return redirect(url_for('adminManageParkir'))


@app.route("/admin/manageCashier")
def adminManageCashier():
    username = "mercuPark"
    conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
    condUsername = 'username = %s'
    getCashierParkir = conn.select('v_cashierParkir', condUsername, 'cashier_id, name, usernameCashier, password',username=username)
    return render_template('admin/manage_cashier.html', cashier=getCashierParkir, username=username)

@app.route("/admin/manageAddCashier", methods=['POST'])
def adminManageAddCashier():
    try:
        username = "mercuPark"
        __name = request.form['name']
        __username = request.form['username']
        __password = request.form['pass2']
        __hasPassword = hash_password(__password)

        sendCashier = cashierParkir(__name, __username, __hasPassword, username)
        resCashier = sendCashier.pushCashier()

        if resCashier == 0:
            flash("Add Cashier Parkir Successfully")
            return redirect(url_for('adminManageCashier'))
        else:
            flash("Add Cashier Parkir Failed")
            return redirect(url_for('adminManageCashier'))
    except Exception as e:
        return "Error Database: %s" % str(e)


@app.route("/admin/manageEditCashier", methods=['POST'])
def adminManagerEditCashier():
    try:
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        __editCashier = request.form['editCashier']
        condCashier = 'cashier_id = %s'
        getDetailCashier = conn.select('v_cashierParkir', condCashier, 'cashier_id, name, usernameCashier, password', cashier_id=__editCashier)
        for i in range(len(getDetailCashier)):
            print(getDetailCashier[0][3])
        # print(getDetailCashier[0])
        detailCashier = []
        for list in getDetailCashier:
            i = {
                'cashier_id': list[0],
                'name': list[1],
                'username': list[2],
                'password': list[3]
            }
            detailCashier.append(i)
            listDetailCashier = json.dumps(detailCashier)
        return render_template('admin/manage_cashier_edit.html', cashier=listDetailCashier)
    except Exception as e:
        return "Error Database: %s" % str(e)


@app.route("/admin/manageUpdateCashier", methods=['POST'])
def manageUpdateCashir():
    try:
        __cashier_id = request.form['cashier_id']
        __name = request.form['name']
        __username = request.form['username']
        __password = request.form['pass2']
        __hashPassword = hash_password(__password)

        sendCashierUpdate = cashierUpdate(__cashier_id, __name, __username, __hashPassword)
        resCashierUpdate = sendCashierUpdate.updateCashier()
        print(resCashierUpdate)
        if resCashierUpdate == 1:
            flash("Update Cashier Parkir Succesfully")
            return redirect(url_for('adminManageCashier'))
        else:
            flash("Update Cashier Parkir Succesfully")
            return redirect(url_for('adminManageCashier'))
    except Exception as e:
        return "Error Database: %s" % str(e)



@app.route("/admin/manageRemoveCashier", methods=['POST'])
def adminManageRemoveCashier():
    try:
        __cashier_id = request.form['removeCashier']
        sendCashier = removeCashier(__cashier_id)
        resCashier = sendCashier.cashierRemove()
        if resCashier == 1:
            flash("Delete Cashier Parkir Successfully")
            return redirect(url_for('adminManageCashier'))
        else:
            flash("Delete Cashier Parkir Failed")
            return redirect(url_for('adminManageCashier'))
    except Exception as e:
        return "Error Database: %s" % str(e)

@app.route("/transactionIn", methods=['POST'])
def transIn():
    try:
        parse = reqparse.RequestParser()
        parse.add_argument('gateId', type=str, help='Gate ID Parkir')
        parse.add_argument('plateNumber', type=str, help='Plate Number Vechile')
        parse.add_argument('timeStart', type=str, help='vechile Start Parking')
        parse.add_argument('statusParkir', type=str, help='Status vechile parking')
        args = parse.parse_args()

        __gateId = args['gateId']
        __plateNumber = args['plateNumber']
        __timeStart = args['timeStart']
        __status_parkir = args['statusParkir']

        sendTransIn = transactionIn(__gateId, __plateNumber, __timeStart, __status_parkir)
        resTransIn = sendTransIn.pushGateIn()
        value = resTransIn
        message = {
            'status': 200,
            'message': 'Data Successfully add to System'
        }
        return json.dumps(message)
    except Exception as e:
        return "Error Database: %s" % str(e)



@app.route("/transactionOut", methods=['POST'])
def transOut():
    #set Global variable

    transDetail = None
    try:


        parse = reqparse.RequestParser()
        parse.add_argument('gateId', type=str, help='Gate Id')
        parse.add_argument('plateNumber', type=str, help='Plate Number Vechile')
        parse.add_argument('timeEnd', type=str, help='End Time')
        parse.add_argument('statusParkir', type=str, help='Status vechile parking')
        args = parse.parse_args()


        __gateId = args['gateId']
        __plateNumber = args['plateNumber']
        __timeEnd = args['timeEnd']
        __statusParkir = args['statusParkir']




        getPaymentMethod = getDetailPayment(__plateNumber)
        resPaymentMethod = getPaymentMethod.getPaymentMethod()

        transactionData = [{
            'transaction_id': resPaymentMethod[0][0],
            'gate_id': __gateId,
            'plateNumber': __plateNumber,
            'timeEnd': __timeEnd,
            'statusParkir': __statusParkir,
            'paymentMethod': resPaymentMethod[0][1]

        }]

        print(resPaymentMethod[0][1])

        if resPaymentMethod[0][1] == "Cash":

            global transDetail
            transDetail = transactionData
            transaction_id = transactionData[0]['transaction_id']
            sendTransOut = transactionOut(__gateId, __plateNumber, __timeEnd, __statusParkir, transaction_id)
            resTransOut = sendTransOut.pushGateOut()
            value = json.dumps(resTransOut)
            # print("Cash Payment")
            return value

        elif resPaymentMethod[0][1] == "Wallet":
            transaction_id = transactionData[0]['transaction_id']
            # print(transaction_id)
            sendTransOut = transactionOut(__gateId, __plateNumber, __timeEnd, __statusParkir, transaction_id)
            resTransOut = sendTransOut.pushGateOut()
            value = json.dumps(resTransOut)
            # print("Wallet Payment")
            return value

    except Exception as e:
        return "Error Database admin: %s" % str(e)


@app.route("/getdata")
def getData():
    getDataTrans = transDetail
    print(getDataTrans[0]['transaction_id'])
    return "testing"
#cashier site
@app.route("/cashier/home")
def cashierHome():
    return render_template('cashier/index.html')


@app.route("/cashier/postLogin", methods=['POST'])
def cashierPostLogin():
    try:
        __username = request.form['usernameCashier']
        __password = request.form['passwordCashier']
        __hashPassword = hash_password(__password)

        sendCashierLogin = cashierLogin(__username, __hashPassword)
        resCashierLogin = sendCashierLogin.loginCashier()

        if resCashierLogin == 0:
            return redirect(url_for('cashierDashboard'))
        elif resCashierLogin == 1:
            flash("Wrong Username or Password ")
            return redirect(url_for('cashierHome'))
        else:
            flash("Failed Login to System")
            return redirect(url_for('cashierHome'))
    except Exception as e:
        return "Error Database: %s" % str(e)


@app.route("/cashier/dashboard")
def cashierDashboard():
    return render_template('cashier/dashboard.html')


@app.route("/cashier/transaction")
def cashierTransaction():
    if transDetail:
        getDataTrans = transDetail
        print(getDataTrans[0]['transaction_id'])
        transID = getDataTrans[0]['transaction_id']

        getTransactionDetail = payCash(transID)
        resTransDetail = getTransactionDetail.getCashTrans()
        transaction_id = str(resTransDetail[0][0])
        plateNumber = str(resTransDetail[0][1])
        convertFee = str(resTransDetail[0][2])
        Fee = decimal.Decimal(resTransDetail[0][2])
        convertFee = str(Fee)
        convertTime = str(resTransDetail[0][3])
        convertStartTime = str(resTransDetail[0][4])
        convertEndTime = str(resTransDetail[0][5])
        #
        # print(convertFee, convertTime, convertStartTime, convertEndTime)
        # lst = list(resTransDetail)
        # lst[0][2] = convertFee
        # lst[0][3] = convertTime
        # lst[0][4] = convertStartTime
        # lst[0][5] = convertEndTime
        # resTransDetail = tuple(lst)

        data = {
            'transaction_id': transaction_id,
            'plateNumber': plateNumber,
            'fee': convertFee,
            'mountTime': convertTime,
            'startTime': convertStartTime,
            'endTime': convertEndTime,

        }
        print(json.dumps(data['transaction_id']))
        v_transId = json.dumps(data['transaction_id'])
        v_plateNumber = json.dumps(data['plateNumber'])
        v_fee = json.dumps(data['fee'])
        v_time = json.dumps(data['mountTime'])
        v_startTime = json.dumps(data['startTime'])
        v_endTime = json.dumps(data['endTime'])

        return render_template('cashier/transaction.html', cashier=json.dumps(data), transId=v_transId, plateNumber=v_plateNumber, fee=v_fee, startTime=v_startTime, endtime=v_endTime, time=v_time)

    else:
        flash("Not Data Loaded")
        return render_template('cashier/transaction.html')


@app.route("/cashier/payment", methods=['POST'])
def cashierpPayment():
    try:
        __transaction_id = request.form['transactionId']
        __plateNumber = request.form['plateNumber']
        __mountFee = request.form['total_biaya']
        __mountTime = request.form['mountTime']
        __startTime = request.form['startTime']
        __endTime = request.form['endTime']
        __bayar = request.form['bayar']
        __refund = request.form['kembalian']

        sendPayment = cashPayment(__transaction_id, __plateNumber, __mountFee)
        resPayment = sendPayment.cashSubmit()

        print(resPayment)

        # this condition can add process to send value to IoT device
        if resPayment == 0:
            print("Payment Successfully")
            flash("Payment Successfully")
            return redirect(url_for('cashierTransaction'))
        else:
            print("Payment Failed")
            flash("Payment Failed")
            return redirect(url_for('cashierTransaction'))
    except Exception as e:
        return "Error Database: %s" % str(e)


@app.route("/getSession")
def getSession():
    if 'user' in session:
        return session['user']
    return 'Not LoggIn User'


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('adminHome'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)