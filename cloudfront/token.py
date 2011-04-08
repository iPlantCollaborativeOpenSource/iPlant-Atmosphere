#
# The contents of this file are subject to the terms listed in the LICENSE file you received with this code.
#
# Author: Seung-jin Kim
# Contact: seungjin@email.arizona.edu
# Twitter: @seungjin
#

import httplib, urllib

def get_token(username,password):
  
  headers = {
      "Content-type" : "application/x-www-form-urlencoded",
      "Accept" : "text/plain",
      "X-Auth-User" : username,
      "X-Auth-Key" : password
      }

  conn = httplib.HTTPConnection("bond.iplantcollaborative.org",8000)
  conn.request("GET","/auth",None,headers)
  r1 = conn.getresponse()
  headers = r1.getheaders()
  conn.close()
  
  if r1.status == 200 :
    for a in headers :
      # insert into database
      if ( a[0] == 'x-auth-token' ) :
        x_auth_token = a[1]
      if ( a[0] == 'x-cdn-management-url' ) :
        x_cdn_management_url = a[1]
      if ( a[0] == 'x-server-management-url' ) :
        x_server_management_url = a[1]
      if ( a[0] == 'date' ) :
        date = a[1]
      if ( a[0] == 'x-storage-url' ) :
        x_storage_url = a[1]
      if ( a[0] == 'server') :
        server = a[1]
      if ( a[0] == 'content-type' ) :
        content_type = a[1]
    cloudfront_token = tokens(
      username=username,
      x_auth_token = x_auth_token,
      x_cdn_management_url = x_cdn_management_url,
      x_server_management_url = x_server_management_url,
      date = date,
      x_storage_url = x_storage_url,
      server = server,
      content_type = content_type,
      issued_at = datetime.datetime.now()
      )
    cloudfront_token.save()
    return x_auth_token
  else :
    print "not valid user"
    
    
def validate_access(request):
    return True

"""
    if request.META.has_key('HTTP_X_AUTH_USER') and request.META.has_key('HTTP_X_AUTH_TOKEN') and request.META.has_key('HTTP_X_AUTH_API_SERVER') :
        
        username = request.META['HTTP_X_AUTH_USER']
        token = request.META['HTTP_X_AUTH_TOKEN'] 
        api_server_url = request.META['HTTP_X_AUTH_API_SERVER']
        
        auth_server_ip = "150.135.78.195"
        port = 8000
        path = "/auth/validate_token"
        method = "GET"
        params = urllib.urlencode(request.GET)
        headers = {
            "Content-type" : "application/x-www-form-urlencoded",
            "Accept" : "text/plain",
            "X-Auth-User" : username,
            "X-Auth-Token" : token,
            "X-Auth-Api-Server": api_server_url
        }

        co = httplib.HTTPConnection(auth_server_ip,port)
        #co.request(method,path,params,headers)
        #r1 = conn.getresponse()
        #print r1.status
        #co.close()
        return "a"
    else :
        return "b"
"""
