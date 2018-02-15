'''
Created on 23-Dec-2014
@author: Mayank Kodesia
'''
import httplib
import json

from framework.helper.Globals import logs
import framework.helper.Globals as Globals


class HttpConnectionHandler(object):
    '''
    This class is used to request a endpoint and get the response back.
    '''
    def __init__(self, projectConfig):
        '''
        Constructor
        '''
        try:
            self.serverAddress = projectConfig.server_address
        except:
            raise  Exception('Please provide valid server address')
        if projectConfig.HTTPS:
            self.protocolHTTPS = True
            try:
                self.http_connection = httplib.HTTPSConnection(self.serverAddress)
            except httplib.BadStatusLine as e:
                print str(e)
            except httplib.HTTPException:
                logs.error("'Could not open connection with the server!'")
                raise
        else:
            self.protocolHTTPS = False
            try:
                self.http_connection = httplib.HTTPConnection(self.serverAddress)
            except httplib.BadStatusLine as e:
                print str(e)
            except httplib.HTTPException:
                logs.error("Could not open connection with the server!\n")
                raise
    def request(self, method, url, headers= {}, body = None):
        Globals.apiCount += 1
        if not(url and method):
            logs.error('Invalid parameters are passed to http request.\n')
            raise Exception('Invalid parameters are passed to http request.')
        logs.info(str(Globals.apiCount)+ ". API Hit Detail start\n")
        logs.info("URL = %s", url)
        logs.info("method = %s", method)
        logs.info("Headers = %s", json.dumps(headers))
        logs.info("Post Body = %s", json.dumps(body))
        logs.info(str(Globals.apiCount)+ "API Hit Detail finished\n")
        try:
            self.http_connection.request(method, url, body, headers)
            self.http_response = self.http_connection.getresponse()
            self.response =  self.http_response.read()
        except Exception as e:
            print str(e)
            raise
        return self.http_response.status
    def json_response(self):
        """Returns the response of the  request send in JSON format"""
        if self.response:
            return json.loads(self.response)
        return None
    def close_connection(self):
        """Close HTTP connection"""
        self.http_connection.close()
