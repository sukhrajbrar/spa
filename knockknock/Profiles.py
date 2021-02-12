# Copyright (c) 2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import os, socket
import mysql.connector
from .Profile import Profile

# database credentials
db = mysql.connector.connect(user='root', password='mrzira99',
                              host='127.0.0.1',
                              database='spa')

db1 = mysql.connector.connect(user='spa', password='mrzira99',
                              host='10.2.5.231',
                              database='spa')

cursor  = db.cursor()
cursor1 = db1.cursor()


class Profiles:

    def __init__(self, directory):
        self.profiles = list()

        for item in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, item)):
                self.profiles.append(Profile(os.path.join(directory, item)))

    def getProfileForPort(port):
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
        """
        for profile in self.profiles:
            if (int(profile.getKnockPort()) == int(port)):
                return profile
        return None"""

    def getProfileForName(self, name):
        for profile in self.profiles:
            if (name == profile.getName()):
                return profile

        return None

    def getProfileForIP(self, ip):
        for profile in self.profiles:
            ips = profile.getIPAddrs()

            if ip in ips:
                return profile

        return None

    def resolveNames(self):
        for profile in self.profiles:
            name                     = profile.getName()
            address, alias, addrlist = socket.gethostbyname_ex(name)

            profile.setIPAddrs(addrlist)

    def isEmpty(self):
        return len(self.profiles) == 0

cursor.close()
cursor1.close()
db.close()
db1.close()
