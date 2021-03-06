__author__ = 'LT-CSIN'
'''
Created on 20-Feb-2014
@author: Mayank Kodesia
'''
from httplib import BadStatusLine
import json
import os
import requests
import time
import traceback

from framework.helper.Globals import logs
import framework.helper.Globals as Globals


class URLFormer(object):
    '''
    This class is used to make the URL configured in main.conf
    Return the response after reading Main.conf file.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__request = requests.Session()


    def getURLResponse(self, url, requestType='GET', headers=None, body='', verifyCert = False, returnTimeTaken=False, fileObjectDict=None, responseIsFile=False, responseHeaders=False, **kwargs):
        '''
        give full URL to this like "http://google.com"
        ## kwargs arguments : 'updateHeaders' to allow update headers with Content-Type = application/json and 'certPath' which accepts certificate path from system.
        Returns variable responses, see argument list, first is response Code and other is response string and so on as 
        per arguments given
        => If u dont pass headers default will be 
            {'Content-Type':'application/json',
              'Accept' : 'application/json',
             }
        => If u dont want any headers to be passed or passed header should not be updated with 
            default value of Content-Type and Accept, pass 'updateHeaders=False' from your calling place of getURLResponse()
        
        If any thing more need to be given, pass that in headers, or if need to be overridden pass that too
        so if Accept should be text/xml, pass that in headers, it will be overridden.
        '''
        
        Globals.apiCount+=1
        logs.debug("Total API Hit Till Now {}".format(Globals.apiCount))
        finalHeaders = {'Content-Type':'application/json',
                  'Accept' : 'application/json',
                  }
        if headers:
            if kwargs and kwargs.get('updateHeaders'):
                finalHeaders.update(headers) 
                headers = finalHeaders
#         print "headers", headers
        
        certPath = kwargs.get('certPath')
        if certPath:
            print "using certificate Path '" + certPath+ "' from certPath argument"
        logs.debug("Headers used for this query is {}".format(headers))

        try:
            logs.debug("Hitting {}".format(url))
            logs.debug("Post Data for this : {}".format(body))

            try:
                start = time.time()
#                 self.flag = "request"
#                 url = self.baseURL+url
#                 url = "https://"+url if self.protocolHTTPS else "http://"+url
                if "post" in requestType.lower():
                    response = self.__request.post(url, data=body,headers=headers, verify = verifyCert, cert=certPath, files=fileObjectDict if fileObjectDict else None)
                
                elif "get" in requestType.lower():
                    response = self.__request.get(url, headers=headers, verify = verifyCert, cert=certPath)
                
                elif "put" in requestType.lower():
                    response = self.__request.put(url, data=body,headers=headers, verify = verifyCert, cert=certPath)
                
                elif "delete" in requestType.lower():
                    response = self.__request.delete(url, data=body, headers=headers, verify = verifyCert, cert=certPath)
                
                elif "patch" in requestType.lower():
                    response = self.__request.patch(url, data=body, headers=headers,verify = verifyCert, cert=certPath)
                
                else:
                    return "Method Not supported in request module","Method Not supported in request module", 000
                timeTaken = time.time() - start
                timeTaken = float("%.2f" %timeTaken)
                print "Got response for {} took {} seconds".format(url, time.time() - start)
                
                if responseIsFile:
                    filePath = os.path.join(os.getcwd(),"temp_"+str(int(time.time())))
                    with open(filePath, "a") as f:
                        f.write(response.content)
                    
                    if returnTimeTaken:
                        return response.status_code, filePath, timeTaken
                    else:
                        return response.status_code, filePath 
            
                    
                if returnTimeTaken and not responseHeaders:
                    return response.status_code, response.content, timeTaken
                elif returnTimeTaken and responseHeaders:
                    return response.status_code, response.content, timeTaken, response.headers
                elif not returnTimeTaken and responseHeaders:
                    return response.status_code, response.content, response.headers
                else:
                    return response.status_code, response.content
            #http://stackoverflow.com/questions/8734617/python-django-badstatusline-error
            except BadStatusLine as e:
                logs.debug("Query {} took {} seconds".format(url, time.time() - start))
                self.__init__()
                logs.error("BAD STATUS LINE EXCEPTION OCCURRED"+str(e))
                logs.error(traceback.format_exc())
                if returnTimeTaken:
                    return "", "Bad Status Line Exception" + traceback.format_exc(), "NotCalculated"
                else:
                    return "", "Bad Status Line Exception" + traceback.format_exc()


        except Exception as e:
            logs.error(e)
            print(traceback.format_exc())
            if returnTimeTaken:
                return "Exception Occurred", traceback.format_exc(), "Not Calculated"
            else:
                return "Exception Occurred", traceback.format_exc()

    
