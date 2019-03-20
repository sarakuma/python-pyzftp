"""
Description: This is a module to transfer multiple text/binary files in and out of mainframe using FTP
Date created: 3/18/2019
Python Version: 3.7.1
Dependencies: Bottle micro web framework 0.12
File system: Linux
"""


__author__ = "Kumar Saraboji"
__version__ = "0.1"
__license__ = "None"
__email__ = "me.kumar.saraboji@gmail.com"
__status__ = "development"

import os
from bottle import TEMPLATE_PATH
from bottle import static_file
from bottle import template, get, route, run, request, redirect
from ftplib import FTP
import os
from threading import Thread  # to implement threading

# declare global variable
statuses = {}  # to capture stats
anyerror = False


def gettext(machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist, iserror):
    """Function to perform FTP GET on text files"""

    global anyerror

    if not iserror:
        with FTP(machine) as host:
            host.login(userid, pswd)

            # try catch file name errors
            try:
                with open(filname, 'w') as tofile:
                    def getline(line):
                        tofile.write(line + '\n')

                    host.retrlines("RETR " + dsn, getline)
            except:
                isfile_exist = False
                iserror = True
                anyerror = True
                host.quit()

            if isfile_exist:
                bytees = os.path.getsize(filname)  # as FTP.size() didn't work used os module as temp/lazy workaround

    if iserror and not ismachine_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "text",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Hostname/IP address doesn't exist"}
    elif iserror and not iscred_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "text",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Incorrect UserID/password"}
    elif iserror and not isfile_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "text",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Source/destination file doesn't exist"}
    else:
        kb1 = str(round(bytees / 1024, 2)) + " KB transferred"
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "text",
                             "sourcefile": dsn, "destfile": filname, "status": "success",
                             "message": kb1}
    return


def getbinary(machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist, iserror):
    """Function to perform FTP GET on binary files"""

    global anyerror

    if not iserror:
        with FTP(machine) as host:
            host.login(userid, pswd)

            # try catch file name errors
            try:
                with open(filname, 'wb') as tofile:
                    host.retrbinary("RETR " + dsn, tofile.write)
            except:
                isfile_exist = False
                iserror = True
                anyerror = True
                host.quit()

            if isfile_exist:
                # as FTP.size() didn't work used os module as temp/lazy workaround
                bytees = os.path.getsize(filname)

    if iserror and not ismachine_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "binary",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Hostname/IP address doesn't exist"}
    elif iserror and not iscred_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "binary",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Incorrect UserID/password"}
    elif iserror and not isfile_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "binary",
                             "sourcefile": dsn, "destfile": filname, "status": "failure",
                             "message": "Source/destination file doesn't exist"}
    else:
        kb1 = str(round(bytees / 1024, 2)) + " KB transferred"
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "receive", "format": "binary",
                             "sourcefile": dsn, "destfile": filname, "status": "success",
                             "message": kb1}
    return


def puttext(machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist, iserror):
    """Function to perform FTP PUT on text files"""

    global anyerror

    if not iserror:
        with FTP(machine) as host:
            host.login(userid, pswd)

            # try catch file name errors
            try:
                with open(filname, 'rb') as fromfile:
                    host.storlines("STOR " + dsn, fromfile)
            except:
                isfile_exist = False
                iserror = True
                anyerror = True
                host.quit()

            if isfile_exist:
                # as FTP.size() didn't work used os module as temp/lazy workaround
                bytees = os.path.getsize(filname)

    if iserror and not ismachine_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "text",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Hostname/IP address doesn't exist"}
    elif iserror and not iscred_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "text",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Incorrect UserID/password"}
    elif iserror and not isfile_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "text",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Source/destination file doesn't exist"}
    else:
        kb1 = str(round(bytees / 1024, 2)) + " KB transferred"
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "text",
                             "sourcefile": filname, "destfile": dsn, "status": "success",
                             "message": kb1}
    return


def putbinary(machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist, iserror):
    """Function to perform FTP PUT on binary files"""

    global anyerror

    if not iserror:
        with FTP(machine) as host:
            host.login(userid, pswd)

            # try catch file name errors
            try:
                with open(filname, 'rb') as fromfile:
                    host.storbinary("STOR " + dsn, fromfile)
            except:
                isfile_exist = False
                iserror = True
                anyerror = True
                host.quit()

            if isfile_exist:
                # as FTP.size() didn't work used os module as temp/lazy workaround
                bytees = os.path.getsize(filname)

    if iserror and not ismachine_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "binary",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Hostname/IP address doesn't exist"}
    elif iserror and not iscred_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "binary",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Incorrect UserID/password"}
    elif iserror and not isfile_exist:
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "binary",
                             "sourcefile": filname, "destfile": dsn, "status": "failure",
                             "message": "Source/destination file doesn't exist"}
    else:
        kb1 = str(round(bytees / 1024, 2)) + " KB transferred"
        statuses[trsfrno] = {"machine": machine, "userid": userid, "pswd": pswd, "verb": "send", "format": "binary",
                             "sourcefile": filname, "destfile": dsn, "status": "success",
                             "message": kb1}
        return


def main(template_path):
    TEMPLATE_PATH.insert(0, template_path)

    @get("/static/<filename>")
    def serve_static_files(filename):
        """Function to serve CSS and JS files"""
        return static_file(filename, root='python-pyzftp/static')

    @route("/zftp", method=["GET", "POST"])
    def process_form():
        """Function to display main webpage and process the form contents"""

        global statuses, anyerror

        if not anyerror:
            machine = ""
            userid = ""
            pswd = ""
            ftno = 1
            checked1 = "checked"
            checked2 = ""
            checked3 = "checked"
            checked4 = ""
            dsn = ""
            filname = ""
        else:
            for k1, v1 in statuses.items():
                machine = v1["machine"]
                userid = v1["userid"]
                pswd = v1["pswd"]
                ftno = ""
                checked1 = ""
                checked2 = ""
                checked3 = ""
                checked4 = ""
                dsn = ""
                filname = ""
                break

        if request.method == "GET":
            return template("zftpmain", machine=machine, userid=userid, pswd=pswd,
                            ftno=ftno, checked1=checked1, checked2=checked2, checked3=checked3, checked4=checked4,
                            dsn=dsn, filname=filname, anyerror=anyerror, statuses=statuses)
        elif request.method == "POST":

            statuses = {}
            anyerror = False
            ismachine_exist = True
            iscred_exist = True
            isfile_exist = True
            iserror = False

            # get all the name attributes from the submitted form
            keylst = list(request.forms.keys())
            trnsfr1lst = [key for key in keylst if "trsfrno" in key]
            trnsfr2lst = [int(key.replace("trsfrno", "")) for key in trnsfr1lst]

            machine = request.forms.get("machine")
            userid = request.forms.get("userid")
            pswd = request.forms.get("pswd")

            # try catch hostname/ip error
            try:
                host = FTP(machine)
            except:
                ismachine_exist = False

            # try catch credentials error
            try:
                if ismachine_exist:
                    host.login(userid, pswd)
            except:
                iscred_exist = False
                host.quit()

            if not ismachine_exist or not iscred_exist:
                iserror = True
                anyerror = True

            threads = []

            for trsfrno in trnsfr2lst:
                ckey1 = "ftpverb-radio" + str(trsfrno)
                ckey2 = "ftpformat-radio" + str(trsfrno)
                if request.forms.get(ckey1) == "receive":
                    get = True
                else:
                    get = False
                if request.forms.get(ckey2) == "text":
                    text = True
                else:
                    text = False
                dsnkey = "dsn" + str(trsfrno)
                filnamekey = "filename" + str(trsfrno)
                dsn = request.forms.get(dsnkey)
                dsn = dsn.replace("'", "")
                dsn = dsn.replace('"', "")
                dsn = "'" + dsn + "'"
                filname = request.forms.get(filnamekey)

                if get:
                    if text:
                        # log = f"{trsfrno} transfer starts.."
                        # print(log)
                        thread = Thread(target=gettext, args=(
                            machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist,
                            iserror))
                        threads.append(thread)
                    else:
                        # log = f"{trsfrno} transfer starts.."
                        # print(log)
                        thread = Thread(target=getbinary, args=(
                            machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist,
                            iserror))
                        threads.append(thread)
                else:
                    if text:
                        # log = f"{trsfrno} transfer starts.."
                        # print(log)
                        thread = Thread(target=puttext, args=(
                            machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist,
                            iserror))
                        threads.append(thread)
                    else:
                        # log = f"{trsfrno} transfer starts.."
                        # print(log)
                        thread = Thread(target=putbinary, args=(
                            machine, userid, pswd, trsfrno, dsn, filname, ismachine_exist, iscred_exist, isfile_exist,
                            iserror))
                        threads.append(thread)

            for thread in threads:
                thread.daemon = True
                thread.start()

            for thread in threads:
                thread.join()

            redirect("/zftp/status")

    @route("/zftp/status", method=["GET"])
    def showmessages():
        """Function to display status webpage"""
        return template("zftpstatus", statuses=statuses)

    run(host="localhost", port=9001, debug=True)  # uses socket - localhost:9001

    return


if __name__ == "__main__":
    arg_template_path = 'python-pyzftp/views'
    main(arg_template_path)
