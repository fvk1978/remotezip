#!/usr/bin/env python

import httplib, urllib
from urlparse import urlparse


class HTTP:
    
    def __init__(self, url):
        self.url = url
        self.params = {}
        self.parts = urlparse(url)
        self.useragent = 'get-remote-file'
        self.is_multipart = False
        self.content_len = 0
    
        headers = {
            'User-agent': self.useragent,
            'Range': 'bytes=0-0'
        }
        
        conn = httplib.HTTPConnection(self.parts.netloc)
        self.path = self.parts.path
        conn.request("GET", self.path, self.params, headers)
        response = conn.getresponse()
        
        # If Range is not supported, just download first max bytes
        if response.status == 200 :
            if response.getheader("content-length") != None :
                self.content_len = int(response.getheader("content-length"))
        
        # Handle Redirect
        elif response.status == 302 :
            newurl = response.getheader("location")
            raise
        
        # Range response
        elif response.status == 206 :
            """ Response example 'content-range', 'bytes 0-40000/3796992"""
            field = response.getheader("content-range")
            self.content_len = int( field[field.find("/")+1:] )
            self.is_multipart = True
    
        # We are not handling errors here
        if response.status > 299 :
            conn.close()
            return
        
        response.close()
    
    def get(self, start, end):
        if self.is_multipart:
            conn = httplib.HTTPConnection(self.parts.netloc)
            headers = {
                'User-agent': self.useragent,
                #'Range': 'bytes=-%(start)d' %locals()
                'Range': 'bytes=%(start)d-%(end)d' %locals()
            }
        
            conn.request("GET", self.path, self.params, headers)
            response = conn.getresponse()
            result = response.read(end - start + 1)
            response.close()
        
            conn.close()
        
            return result
        
if __name__ == "__main__":
    h = HTTP('http://forum.fvk:81/3scan.zip')
    print "=%s=" % h.get(0,29)