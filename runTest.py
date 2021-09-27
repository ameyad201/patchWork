import re
import subprocess
import os
import time
import requests

def send_slack_message (message):
    payload = '{"text":"%s"}' % message
    response = "NEED TO ADD SLACK WEBHOOK"
    print(response)

print("Running Attach Detach testcase")
result = os.chdir("/S1APTester/TestCntlrStub/bin/")
print(result)
#result = os.system("sudo ./testCntrlr AttachAndUlData 1 >> /tmp/test_output.log")
process = subprocess.Popen("sudo ./testCntrlr AttachAndUlData 1 >> /tmp/test_output.log", shell=True)
time.sleep(600)
fh = open("/tmp/test_output.log",'r')
output = fh.read()
patt1 = "Received Attach Accept Indication from TFW"
patt2 = "Sending Detach Request"
attachFoundFlag = 0
detachFoundFlag = 0
for line in output:
    attachCheck = re.search(patt1,line)
    if attachCheck != None:
        print (attachCheck)
        attachFoundFlag = 1;
    detachCheck = re.search(patt2,line)
    if detachCheck != None:
        print(detachCheck)
        detachFoundFlag = 1;

if attachFoundFlag == 1 and detachFoundFlag == 1:
    print ("Testcase : AttachDetach Passed")
    send_slack_message ("Tests complete : Result Passed")
else:
    print ("Testcase : Attach Detach Failed")
    send_slack_message ("Tests complete : Result Failed")