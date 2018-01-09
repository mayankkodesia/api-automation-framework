__author__ = 'LT-CSIN'

'''
Created on 30-Apr-2014
@author: Mayank Kodesia

Store globals variable for the project
'''
import datetime
import os

import logging as logs


global TESTLINK
TESTLINK=False

global BUILDNO
BUILDNO='1.2.1b'

global PASSWORD
PASSWORD=''

global ADDED_TESTCASES_TO_TESTPLAN
ADDED_TESTCASES_TO_TESTPLAN=False

global BUILD_CREATED
BUILD_CREATED=False

global SINCE_REPORT
SINCE_REPORT="14-00000010"

global SINCE_REPORT2
SINCE_REPORT2="14-33346"

global TEST_DATA
TEST_DATA={}

global TEST_TO_RUN
TEST_TO_RUN = {}

global CLASS_OBJ
CLASS_OBJ = object

global REPORT_OBJ
REPORT_OBJ = None

global SINCE_REPORT_VERSION_PUBLISH_DATE
SINCE_REPORT_VERSION_PUBLISH_DATE="1416006240"#"1416006240" #1415941440 coming from function

global AUTH
AUTH=2

global API_VERSION
API_VERSION=2

global reportName
reportName="all"

global logs

global apiKey
apiKey="none"

global secret
secret="none"
# import logging.Handler
global testCaseNo
testCaseNo=0

global parentOrgName
parentOrgName = "automationDoNoUseOrDelete"

global subOrgName
subOrgName = "subOrgDoNotUse"

global parentOrgId
parentOrgId = "1170"

global subOrgId
subOrgId = "1192"

global UsageStatsParentOrg
UsageStatsParentOrg = "1162"

global UsageStatsSubOrg
UsageStatsSubOrg = "1279"

global apiCount
apiCount = 0

global epochTimeDaysBack
epochTimeDaysBack=50

global userId
userId = "9680"

global dailyLimitExceeded
global reportOutOfPublicationRange
global unauthorized
global licenseFailure
global rateLimitExceeded
global monthTicketSubmission
global dailySubmissionQuota
global nonAdminUser

dailyLimitExceeded={'X-App-Name':'application/json', 'public_key': '3307b1d816484a4b564ceda37e1c98c7d2e6cdf02c55b9b7a0cdfa0b45fb74f2', 'private_key': '60f4a2458a0e437b0a60efcf1edd8b2b9b7569dd931aaec98f08e82065c1213f'}
reportOutOfPublicationRange={'X-App-Name':'application/json', 'public_key': '90ddc11e6f68184f7ccb9ad74ee597f3e95d23c7005599fdc60fe99b55cb0812', 'private_key': '1f81bed0a3a5b5e5571483e572f23ea3a22b9600c3b93ac9a835e74510eca3be'}
unauthorized={'X-App-Name':'application/json', 'public_key': 'd231f05f4e06b3bcffaa3d296346db44f9c5a4bb0fb37e3aa59bf444fb5fba67', 'private_key': 'f419ff967b650b5bfeacc51e244bad5fb60b883a1d9b5ac15919b7c41fbe313'}
licenseFailure={'X-App-Name':'application/json', 'public_key': '13ac03741c8d7f9d4dd72e5694cb55473d04814f1cb946fd10ac2165bdda4df6', 'private_key': '287fbda6c63420c411ef640b86f4cde79734700392630de91bca74958b39e0c8'}
rateLimitExceeded={'X-App-Name':'application/json', 'public_key': 'ccd35d3e5424b4c23cd2ed3b550a00133c91f8910bd9563926264cf0a4e21b14', 'private_key': '4f07f922b7b7b8ab51a1cf7d991c1c76626468a6b7867d845986d6534e1f6877'}
monthTicketSubmission = {'X-App-Name':'application/json', 'public_key': '4deb2634bc66a8e1fc36b996dce5b37e32664859445a770d852e819c9d1a29a6', 'private_key': '71df684c8c47195e67b88bb84bf5922134b9c48d818ccea5f76ee965d502e532'}
dailySubmissionQuota = {'X-App-Name':'application/json', 'public_key': '29dd54bc9c6b1a9fa23a8d4334c5468cd25fa5e203b5835741ff3415d85cdce4', 'private_key': 'd7150a9650cb4854c23ff01d0e9012d7955e89f92c9f5b68a1a5641ed8f83ba4'}
nonAdminUser = {'public_key': '42de4459bdbe389cb7dcf4ece1992371695705936bd4c74c68f07d640142d07c', 'private_key': '42474b23544e5669608794d3bbc797210eda97f9b35c250f6326780735069b5b'}

global permission_header
permission_header = {'public_key': '6c1fa995b7fbd40b81a5276dc5ce60bd3146e998806f48cd5e77a461cebf84f1', 'private_key': 'ddd1427687181734b5dc3d9993a32f350743cf498716db4b76e68cf54c8b7a8b'}

global AAValidHeader
AAValidHeader = {'public_key': 'e6ebf1b7e80d1ff967d83d585161014f1d8ed82650d00106090c87d3225e0ea6', 'private_key': '305db6586ab6e6fecfe28b3019c8945297ba764cf85d0eab6f5c095f8e58ed95'}

global AAInvalidHeader
AAInvalidHeader = {'public_key': 'cbe1384bfec29b44512fc1c5123127625dd409e2d2207e76f60e3bae3e1f047b', 'private_key': '32f26d9139e8423e27bfdd84410f70392b980cd57d11f852f8df85d329ba4f0f'}

global heartBeatPublicKey
global heartBeatPrivateKey

heartBeatPublicKey = '91bf9dd9aa80453e94ca5262659fd76ada522fb51c2dde6087282f19a2df8841'
heartBeatPrivateKey = '487013f8541c0fee8c0b8b8f24d52f9c1705bef734ce37480fccca3d87a22ad8'

global API10PublicKey
global API10PrivateKey

API10PublicKey='a925106d89b828596020c8f636ab9c8006154c94fce1e1f248509c53a2273d40'
API10PrivateKey='12fbdb2c851f2b86d7a5233a2f7a002e6a070d7ee8fe49aab47df81c299a6c91'


global public_key
global private_key

global deptIdForNotAdminUser
global deptNameForNotAdminUser
global accountNameForNotAdminUser

deptIdForNotAdminUser = '1895'
deptNameForNotAdminUser = 'testDoNotDelete'
accountNameForNotAdminUser = 'loadauto1'

global errorCode
errorCode = 1

public_key = '1255ab93d089b7a1336186b2a11033754ef4996cba786dcb8cd68951f947c40d'
private_key = '1f596a4f9cd0b30412909fa29d8f5b4999bfd6cd259dd36857b5a9448592bfde'

dates = datetime.datetime.now().strftime("%d %B %Y %H %M %S %p")
script_dir = os.path.dirname(__file__)
logFileName = script_dir + "/../ConsoleLogs/Logs_"+(str(dates).replace(' ', "_")) + ".log"
dir = os.path.dirname(logFileName)
if not os.path.exists(dir):
    print "dir going to make {}".format(dir)
    os.makedirs(dir)
root_logger = logs.getLogger()
#logs.basicConfig(format='%(levelname)s** %(asctime)s ** %(module)s_%(funcName)s ** %(message)s', level=logs.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p', filename=logFileName, filemode='w')
# logs.basicConfig(format='%(levelname)s****%(module)s_%(funcName)s*** %(message)s', level=logs.INFO, filename=logFileName, filemode='w')
logs.basicConfig(format='%(levelname)s****%(module)s_%(funcName)s*** %(message)s', level=logs.DEBUG, filename=logFileName, filemode='w')


