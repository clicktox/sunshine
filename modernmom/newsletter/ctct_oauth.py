class CTCTOAuthClient(oauth.OAuthClient):
 
    def __init__(self, callback, domain, https=False, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_url=ACCESS_TOKEN_URL, authorization_url=AUTHORIZATION_URL, request_token_url=REQUEST_TOKEN_URL):
        if not consumer_key:
            raise OAuthError(message="CTCT_API_KEY not set in settings.")
        if not consumer_secret:
            raise OAuthError(message="CTCT_SECRET not set in settings.")
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.request_token_url = request_token_url
        self.consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.callback = callback
        self.domain = domain
        self.https = https
        self.connection = httplib.HTTPSConnection('%s' % SERVER)
        
    def callback_url(self):
        base = 'http://'
        if self.https:
            base = 'https://'
        return '%s%s%s' % (base, self.domain, self.callback)
    
    def fetch_access_token(self, verifier, key, secret):
        token = oauth.OAuthToken(key, secret)
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, verifier=verifier, http_url=self.access_token_url, http_method='POST')
        oauth_request.sign_request(self.signature_method, self.consumer, token)
        url = oauth_request.to_url()
        self.connection.request(oauth_request.http_method,url)
        response = self.connection.getresponse()
        response_string = response.read()
        return oauth.OAuthToken.from_string(response_string)
    
    def auth_url(self, token):
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url=self.authorization_url)
        return oauth_request.to_url()
    
    def auth_token(self, key, secret):
        token = oauth.OAuthToken(key, secret)
        return token
    
    def fetch_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, callback=self.callback_url(), http_url=self.request_token_url, http_method='POST')
        oauth_request.sign_request(self.signature_method, self.consumer, None)
        url = oauth_request.to_url()
        self.connection.request(oauth_request.http_method,url)
        response = self.connection.getresponse()
        response_string = response.read()
        return oauth.OAuthToken.from_string(response_string)
    
    def request_token(self):
        token = self.fetch_request_token()
        return token
    
    def access_resource(self, oauth_request):
        connection = httplib.HTTPSConnection('%s' % API_SERVER)
        url = oauth_request.to_url()
        connection.request(oauth_request.http_method, url)
        response = connection.getresponse()
        return response
    
    def verify_credentials(self, username, token):
        resource_url = API_BASE_URL + username + "/"
        parameters = {}
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_method='GET', http_url=resource_url, parameters=parameters)
        oauth_request.sign_request(self.signature_method, self.consumer, token)
        response = self.access_resource(oauth_request)
        if response.status == 200:
            return True, ''
        else:
            return False, response.read()
    
    def get_contact_lists(self, username, token, path=None):
        #Most of this code is a carbon copy from the Constant Contact restful python lib
        #Who's author is "Huan Lai, Constant Contact Labs"
        contact_lists = []
        if(path == None):
            path = '/lists'
        resource_url = API_BASE_URL + username + path
        parameters = {}
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_method='GET', http_url=resource_url, parameters=parameters)
        oauth_request.sign_request(self.signature_method, self.consumer, token)
        response = self.access_resource(oauth_request)
        if response.status != 200:
            return None
        # Build an XML Tree from the return
        response_string = response.read()
        xml = ET.fromstring(response_string.encode('ascii','xmlcharrefreplace'))
        # Check if there is a next link
        links = xml.findall('{http://www.w3.org/2005/Atom}link');
        next_path = None
        for link in links:
            if(link.get('rel') == 'next'):
                next_link = link.get('href')
                slash = next_link.find('/lists')
                next_path = next_link[slash:]
                break
        # Get all of the contact lists
        entries = xml.findall('{http://www.w3.org/2005/Atom}entry')
        for entry in entries:
            contact_list = {'id': entry.findtext('{http://www.w3.org/2005/Atom}id'),
                            'name': entry.findtext('{http://www.w3.org/2005/Atom}content/'
                                                   '{http://ws.constantcontact.com/ns/1.0/}ContactList/'
                                                   '{http://ws.constantcontact.com/ns/1.0/}Name'),
                            'updated': entry.findtext('{http://www.w3.org/2005/Atom}updated')}
            list_url = urlparse(contact_list['id'])
            try:
                contact_list['int_id'] = int(list_url.path.split('/')[-1])
            except:
                pass
            # Don't include some lists
            if(contact_list['name'] not in DO_NOT_INCLUDE_LISTS):
                contact_lists.append(contact_list)
        # If there is a next link, recursively retrieve from there too
        if(next_path != None):
            contact_lists.extend(self.get_contact_lists(path=next_path))
        return contact_lists