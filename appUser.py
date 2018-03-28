from flask import Flask, render_template, request, session, g, redirect, url_for, jsonify, json, flash
import os
import hashlib
import config
from connection import mysqlconnection
from user import loginUser, registration, getProfile, update_profile, forgetpasswd, topup, paymentUpdate, historyUser
import MySQLdb


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/user/home")
def userHome():
    conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
    cityName = conn.select('city', None, 'city_id, city_name')
    return render_template('user/index.html', city=cityName )


@app.route("/user/signup", methods=['POST'])
def userSignup():
    message = None
    try:
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        __firstname = request.form['firstname']
        __lastname = request.form['lastname']
        __email = request.form['inputEmail']
        __telp = request.form['telp']
        __password = request.form['password']
        __plate = request.form['plateNumber']
        __city = request.form['city']
        __passwordHash = hash_password(__password)

        city_name = 'city_name = %s'
        city_id = conn.select('city', city_name, 'city_id', city_name=__city)
        register = registration(__firstname, __lastname, __email, __passwordHash, __telp, __plate, city_id)
        resRegister = register.signUp()
        message = resRegister
        print(resRegister)

        return redirect(url_for('userHome'))
    except Exception as  e:
        return "Error Database: %s" % str(e)


@app.route("/user/signin", methods=['POST'])
def userSignIn():
    try:
        __email = request.form['signin-email']
        __password = request.form['signin-password']
        __passwordHash = hash_password(__password)

        userLogin = loginUser(__email, __passwordHash)
        resLogin = userLogin.user_login()

        if resLogin == 0:
            session['user'] = __email
            return redirect(url_for('userProfile'))
        else:
            flash('Wrong password or Email')
            return redirect(url_for('userHome'))
    except Exception as e:
        return "Error Database: %s" % str(e)


#user signUp
@app.route("/user/auth/signup", methods=['GET', 'POST'])
def signup():
    conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
    cityName = conn.select('city', None, 'city_id, city_name')

    message = None
    if request.method == 'POST':
        try:
            db = MySQLdb.connect(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
            cursor = db.cursor()
            __firstName = request.form['inputName']
            __lastName = request.form['name_belakang']
            __email = request.form['inputEmail']
            __password = request.form['inputPassword']
            __passwordHash = hash_password(__password)
            __telp = request.form['telp']
            __plateNumber = request.form['plateNumber']
            __cityName = request.form['city']


            city_name = 'city_name = %s'
            city_id = conn.select('city', city_name, 'city_id', city_name=__cityName)

            register = registration(__firstName, __lastName, __email, __passwordHash, __telp, __plateNumber, city_id)
            resRegister = register.signUp()
            message = resRegister
            print(resRegister)


        except Exception as e:
            return "Error Database : %s" % e
    return render_template('signUp.html', city=cityName, message=message)



@app.route("/user/auth/signin", methods=['GET', 'POST'])
def signin():
    message = None
    if request.method == 'POST':
        session.pop('user', None)

        try:
            __email = request.form['emailUser']
            __password = request.form['password']
            __passConvert = hash_password(__password)


            userLogin = loginUser(__email, __passConvert)
            resLogin = userLogin.user_login()

            if resLogin == 0:
                session['user'] = __email
                return redirect(url_for('userProfile'))

            else:
                message = "Wrong Email or Password"


        except Exception as e:
            return "Error Database: %s" % str(e)

    return render_template('signIn.html', message=message)

@app.route('/user/profile', methods=['GET', 'POST'])
def userProfile():
    if g.user:
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        city_name = conn.select('city', None, 'city_id, city_name')
        email = g.user
        # email = "rika@mail.com"

        profile = getProfile(email)
        resProfile = profile.profile()

        profileList = []
        for list in resProfile:
            i = {
                'user_id': list[0],
                'firstname': list[1],
                'lastname': list[2],
                'identityType': list[3],
                'identityNumber': list[4],
                'gender': list[5],
                'cityName': list[6],
                'cityId': list[7],
                'phoneNumber': list[8],
                'email': list[9]
            }
            profileList.append(i)
            condition = "email = %s"
            plateNumber = conn.select('v_plateNumber', condition, 'platenumber_code', email=email)

        return render_template('user/profile.html', city_name=city_name, profile=json.dumps(profileList), platenumber=plateNumber)
    return redirect(url_for('userHome'))

@app.route("/postProfile", methods=['POST'])
def postProfile():


    try:
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)

        __user_id = request.form['user_id']
        __firstname = request.form['firstname']
        __lastname = request.form['lastname']
        __identityType = request.form['identityType']
        __identityNumber = request.form['identityNumber']
        __gender = request.form['gender']
        __cityName = request.form['cityName']
        __plateNumber = request.form['plate']
        cityCondition = 'city_name = %s'
        cityId = conn.select('city', cityCondition, 'city_id', city_name=__cityName)

        updateProfile = update_profile(__user_id,__firstname, __lastname, __identityNumber, __identityType, __gender, cityId, __plateNumber)
        resUpdate = updateProfile.updateprofile()
        print(resUpdate)


        return redirect(url_for('userProfile'))

    except Exception as e:
        return "Error Database: %s" %  str(e)

#Payment GET Proses
@app.route("/user/payment")
def userPayment():
    if g.user:
        email = g.user
        # email = "rika@mail.com"
        conn = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, config.DATABASE)
        condition = 'email = %s'
        getBalance = conn.select('v_user', condition, 'balance', email=email)
        getProviderBank = conn.select('topup_choose', None, 'topupChoose_id, provide_topup')
        getPaymentMethod = conn.select('payment_method', None, 'paymentMethod_id, PaymentMethod_name,icon_payment')
        condSeleted = 'email = %s'
        getSelectedPayment = conn.select('v_user', condSeleted, 'paymentMethod_id, PaymentMethod_name', email=email)


        return render_template('user/payment.html', balance=getBalance, providerBank=getProviderBank, paymentMethod=getPaymentMethod, paymentSelected=getSelectedPayment)
    return redirect(url_for('userHome'))

@app.route("/user/topup", methods=['POST'])
def userTopup():
    if g.user:
        try:
            email = g.user
            # email = "rika@mail.com"
            __provider = request.form['jenisPembayaran']
            __topupNominal = request.form['nominal']
            __email = email

            sendTopup = topup(__provider, __topupNominal, __email)
            resTopup = sendTopup.topupUpdate()
            print(resTopup)


            return redirect(url_for('userPayment'))
        except Exception as e:
            return "Error Database: %s" % str(e)
    return redirect(url_for('userHome'))

@app.route("/user/updatePayment", methods=['POST'])
def updatePayment():
    if g.user:
        try:
            email = g.user
            # email = "rika@mail.com"
            __payment = request.form['payment_method']

            sendPayment = paymentUpdate(__payment, email)
            resPayment = sendPayment.paymentUpdateUser()
            print(resPayment)

            return redirect(url_for('userPayment'))
        except Exception as e:
            return "Error Database: %s" % str(e)

    return redirect(url_for('userHome'))


@app.route("/user/searchMaps")
def searchMaps():
    if g.user:
        connect = mysqlconnection(config.HOST, config.USERNAME, config.PASSWORD, "test")
        result = connect.select('parkirlocation', None, 'name_place, address, latitude, Longitude, postalCode')

        location_result = []
        for list in result:
            i = {
                'name': list[0],
                'address': list[1],
                'lat': list[2],
                'lng': list[3],
                'postalCode': list[4]
            }
            location_result.append(i)

            items = location_result
            json_result = json.dumps(items)

            print(json_result)
        return render_template('user/location.html', json_result=json_result)
    return redirect(url_for('userHome'))

@app.route("/user/history")
def userHistory():
    if g.user:
        email = g.user
        userHist = historyUser(email)
        getUserHist = userHist.getHistory()
        # print(getUserHist[0][0])
        historyDetail = []

        for index,list in enumerate(getUserHist):

            # i = {
            #     'transaction': list[0],
            #     'paymentMethod': list[1],
            #     'plateNumber': list[2],
            #     'start_time': list[3],
            #     'end_time': list[4],
            #     'status_payment': list[5]
            # }
            # print(loop.index)
            # print(list[0], list[1],list[2],str(list[3]),str(list[4]), list[5])
            i = {
                'transaction_id': list[0],
                'paymentMethod': list[1],
                'plateNumber': list[2],
                'start_time': str(list[3]),
                'end_time': str(list[4]),
                'status_payment': list[5],
                'name_parkir': list[6]
            }

            historyDetail.append(i)

        return render_template('user/history.html', history=historyDetail)
    return redirect(url_for('userHome'))



@app.route("/getSession")
def getSession():
    if 'user' in session:
        return session['user']
    return 'Not LoggIn User'


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('userHome'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')