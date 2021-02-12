from knockknock.Profile import Profile
from knockknock.Profiles import Profiles
# from knockknock.PortOpener import PortOpener
# from knockknock.LogEntry import LogEntry
import mysql.connector
import os, sys, socket
# import hmac, hashlib
from knockknock.MacFailedException import MacFailedException
from knockknock.CryptoEngine import CryptoEngine
# from Crypto.Cipher import AES
#
"""class Profiles:

    def __init__(self, directory):
        self.profiles = list()

        for item in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, item)):
                self.profiles.append(Profile(os.path.join(directory, item)))

    def getProfileForPort(self, port):
        for profile in self.profiles:
            if (int(profile.getKnockPort()) == int(port)):
                return profile
        return None
"""
#localhost = Profiles("/etc/knockknock.d/profiles/")
#result = localhost.getProfileForPort(222)
#print(result.directory)


# def getProfile(host):
#     homedir = os.path.expanduser('~')
#
#     if not os.path.isdir(homedir + '/.knockknock/'):
#         print("Error: you need to setup your profiles in " + homedir + '/.knockknock/')
#         sys.exit(2)
#
#     if not os.path.isdir(homedir + '/.knockknock/' + host):
#         print('Error: profile for host ' + host + ' not found at ' + homedir + '/.knockknock/' + host)
#         sys.exit(2)
#
#     profile = Profile(homedir + '/.knockknock/' + host)
#     serverProfile = Profile('/etc/knockknock.d/profiles/'+ host)
#     print(profile.config,serverProfile.config)
#
# def tailAndProcess(ciphertext):
#     homedir = os.path.expanduser('~')
#     profile    = Profile('/etc/knockknock.d/profiles/localhost')
#     port       = Profile.decrypt(profile, ciphertext, 22597)
#     sourceIP   = '127.0.0.1'
#
#     PortOpener.open(sourceIP, 22)
#     print("Received authenticated port-knock for port " + str(port) + " from " + sourceIP)
#
# data = b'\x8c\xb8\xf9k\x8f\xc3;\xc99GXE'
# tailAndProcess(data)
# #print(Profiles.getProfileForPort(999))
import string
import secrets
from struct import *

# database credentials
db = mysql.connector.connect(user='root', password='mrzira99',
                              host='127.0.0.1',
                              database='spa')

db1 = mysql.connector.connect(user='spa', password='mrzira99',
                              host='10.2.5.231',
                              database='spa')

cursor  = db.cursor()
cursor1 = db1.cursor()

def testing(port, counter):
    cipher = secrets.token_hex(5)
    mac    = secrets.token_hex(5)
    cipherCrypt = cipher + str(counter).zfill(2)
    macCrypt    = mac + str(port).zfill(2)
    encrypted = ''
    for i in range(len(cipherCrypt)):
        encrypted += chr(ord(cipherCrypt[i])^ord(macCrypt[i]))

    res = bytes(encrypted, 'ascii')
    packet = unpack('!HIIH',res)
    data   = pack('!HIIH',packet[0],packet[1],packet[2],packet[3])
    print("Encrypted is: ", res, "Data is: ", data)
    decrypted = ''
    for i in range(len(data)):
        decrypted += chr(data[i]^ord(cipherCrypt[i]))

    #macT = macCrypt[:10]
    #portT = macCrypt[10:]
    if decrypted == macCrypt:
        return "Mac id is: " + str(macCrypt[:10]) + " Port number is: "+ str(macCrypt[10:])
    else:
        return "SomeThing wrong"
#print (testing(48, 11))

def decrypt( encryptedData, windowSize):
    counter = 2
    for x in range(windowSize):
        try:
            counterCrypt = CryptoEngine.encryptCounter(counter + x)
            decrypted    = str()

            for i in range(len(encryptedData)):
                decrypted += chr(encryptedData[i] ^ counterCrypt[i])

            decrypted = decrypted.encode('cp037')
            port = decrypted[:2]
            mac  = decrypted[2:]
            self.verifyMac(port, mac)
            counter += x + 1


            return int(unpack("!H", port)[0])

        except MacFailedException:
            pass

    raise MacFailedException("Ciphertext failed to decrypt in range...")
#decrypt('Ç6ÝôôÎ¡÷!õÍ', 53109)

def retrieveprofile(port):
    query = """SELECT * FROM `knockknock` WHERE `knockport` = %s;"""%(port)
    cursor.execute(query)
    result = cursor.fetchall()
    for i in range(len(result)):
        (Number, profileName, cipher, counter, mac, knockport) = result[i]
        matchingQuery = """Select `Valid` from `validkey` WHERE `Number`= %s;"""%(Number)
        cursor1.execute(matchingQuery)
        data = cursor1.fetchone()
        (check) = data[0]
        if check == 1:
            return result[i]

    return None

def testingDecryption(encryption, counterd):
    (Number, profileName, cipher, counter, mac, knockport) = retrieveprofile(123)
    res = encryption
    packet = unpack('!HIIH',res)
    data   = pack('!HIIH',packet[0],packet[1],packet[2],packet[3])
    cipherCrypt = cipher[:5] + str(counterd).zfill(2) + cipher[5:]
    decrypted = ''
    for i in range(len(data)):
        decrypted += chr(data[i] ^ ord(cipherCrypt[i]))

    if (str(decrypted[:5])+str(decrypted[7:])) == mac:
        return "Mac id is: " + str(mac[:5]) + str(mac[7:]) + " Port number is: "+ str(decrypted[5:7])

    return "SomeThing wrong"

print(Profiles.getProfileForPort(123))
#print(testingDecryption(b'\x04\x00T\x02\x05\x03\x03\x04\x0f\x06RX', 11))
cursor.close()
cursor1.close()
db.close()
db1.close()
