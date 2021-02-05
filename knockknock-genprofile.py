#!/usr/bin/env python

__author__ = "Moxie Marlinspike"
__email__  = "moxie@thoughtcrime.org"
__license__= """
Copyright (c) 2009 Moxie Marlinspike <moxie@thoughtcrime.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA

"""

import os, sys
import secrets
import random
import mysql.connector
from mysql.connector import Error
from knockknock.Profiles import Profiles
from knockknock.Profile  import Profile

# database credentials
db = mysql.connector.connect(user='root', password='mrzira99',
                              host='127.0.0.1',
                              database='spa')

db1 = mysql.connector.connect(user='spa', password='mrzira99',
                              host='10.2.5.231',
                              database='spa')

cursor  = db.cursor()
cursor1 = db1.cursor()

DAEMON_DIR   = '/etc/knockknock.d/'
PROFILES_DIR = DAEMON_DIR + 'profiles/'

def usage():
    print("knockknock-genprofile <knockPort> <profileName>edited by sukhraj singh brar")
    sys.exit(3)

def checkProfile(profileName):
    """
    if (os.path.isdir(PROFILES_DIR + profileName)):
        print("Profile already exists.  First rm " + PROFILES_DIR + profileName + "/")
        sys.exit(0)
    """
    selectStatement = """SELECT * FROM `knockknock` WHERE `profileName` = '%s';"""%(profileName)
    cursor.execute(selectStatement)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    else:
        return 1

def checkPortConflict(knockPort):
    """if (not os.path.isdir(PROFILES_DIR)):
        return

    profiles        = Profiles(PROFILES_DIR)
    matchingProfile = profiles.getProfileForPort(knockPort)

    if (matchingProfile != None):
        print("A profile already exists for knock port: " + str(knockPort) + " at this location: " + matchingProfile.getDirectory())
    """
    selectStatement = """SELECT * FROM `knockknock` WHERE `knockport` = %s;"""%(knockPort)
    cursor.execute(selectStatement)
    result = cursor.fetchall()
    if len(result) == 0:
        return 0
    else:
        return 1

def createDirectory(profileName):
    if not os.path.isdir(DAEMON_DIR):
        os.mkdir(DAEMON_DIR)

    if not os.path.isdir(PROFILES_DIR):
        os.mkdir(PROFILES_DIR)

    if not os.path.isdir(PROFILES_DIR + profileName):
        os.mkdir(PROFILES_DIR + profileName)

def storeValuesInDb(knockPort, profileName, lastEntry, validKeyLocation, i):
    cipherKey = secrets.token_hex(5)
    macKey    = secrets.token_hex(5)
    counter   = 0

    """profile = Profile(PROFILES_DIR + profileName, cipherKey, macKey, counter, knockPort)
    profile.serialize()
    """

    currentEntry = lastEntry+i+1
    if  currentEntry == validKeyLocation:
        valid = 1
    else:
        valid = 0

    profile = """INSERT INTO knockknock ( `cipher`, `counter`, `mac`, `knockport`, `profileName`)
                VALUES ('%s', %s, '%s', %s, '%s');""" %( cipherKey, counter, macKey, knockPort, profileName)
    dataInValidKey = """INSERT INTO `validkey`(`Number`, `Valid`, `profileName`)
                        VALUES (%s, %s, '%s');"""%(currentEntry, valid, profileName)
    cursor.execute (profile)
    cursor1.execute (dataInValidKey)

    db.commit()
    db1.commit()

    print("(Update by Sukhraj Singh Brar)Keys successfully stored in db")

def main(argv):

    if len(argv) != 2:
        usage()

    knockPort   = argv[0]
    profileName = argv[1]
    #knockPort   = argv[1]
    
    checkPort = checkPortConflict(knockPort)
    checkProfileName = checkProfile(profileName)

    if checkPort == 1:
        print("A profile already exists for knock port: ", knockPort)

    elif checkProfileName == 1:
        print("A profile already exists for this Profile Name: ", profileName)

    else:
        lastEntryQuery = """SELECT `Number` FROM `knockknock` ORDER BY `Number` DESC LIMIT 1;"""
        cursor.execute (lastEntryQuery)
        lastEntry = cursor.fetchone()[0]
        validKeyLocation = random.randint (lastEntry+1, lastEntry+10)
        for i in range(10):
            storeValuesInDb(knockPort, profileName, lastEntry, validKeyLocation, i)

    """
    createDirectory(profileName)
    cipherKey = secrets.token_bytes(16)
    macKey    = secrets.token_bytes(16)
    counter   = 0
    profile = Profile(PROFILES_DIR + profileName, cipherKey, macKey, counter, knockPort)
    profile.serialize()
    """
    cursor.close()
    cursor1.close()
    db.close()
    db1.close()

if __name__ == '__main__':
    main(sys.argv[1:])
