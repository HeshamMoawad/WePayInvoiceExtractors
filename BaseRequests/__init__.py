import requests
from requests import Response


    

class NewResponse(Response):
    def __init__(self,response:Response) -> None:
        self.__dict__ = response.__dict__        
        # Information responses
        self.__Informational = {
            100 : "Continue" ,
            101 : "Switching Protocols",
            102 : "Processing",
            103 : "Early Hints",            
        }
        # Successful responses
        self.__Success = {
            200 : "OK" ,
            201 : "Created",
            202 : "Accepted",
            203 : "Non-Authoritative Information",            
            204 : "No Content",            
            205 : "Reset Content",            
            206 : "Partial Content",            
            207 : "Multi-Status",            
            208 : "Already Reported",            
            226 : "IM Used",            
        }
        # Redirection messages
        self.__Redirect = {
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            306: "(Unused)",
            307: "Temporary Redirect",
            308: "Permanent Redirect",
        }
        # Client error responses
        self.__ClientError = {
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Payload Too Large",
            414: "URI Too Long",
            415: "Unsupported Media Type",
            416: "Range Not Satisfiable",
            417: "Expectation Failed",
            418: "I'm a teapot",
            421: "Misdirected Request",
            422: "Unprocessable Entity",
            423: "Locked",
            424: "Failed Dependency",
            425: "Too Early",
            426: "Upgrade Required",
            428: "Precondition Required",
            429: "Too Many Requests",
            431: "Request Header Fields Too Large",
            451: "Unavailable For Legal Reasons",
        }
        # Server error responses
        self.__ServerError = {
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported",
            506: "Variant Also Negotiates",
            507: "Insufficient Storage",
            508: "Loop Detected",
            510: "Not Extended",
            511: "Network Authentication Required",
        }
    # @property
    # def status_code_type(self):
    #     match self.status_code:
    #         case Informational if Informational in self.__Informational.keys():
    #             return self.__Informational[Informational]
    #         case Success if Success in self.__Success.keys():
    #             return self.__Success[Success]
    #         case Redirect if Redirect in self.__Redirect.keys():
    #             return self.__Redirect[Redirect]
    #         case ClientError if ClientError in self.__ClientError.keys():
    #             return self.__ClientError[ClientError]
    #         case ServerError if ServerError in self.__ServerError.keys():
    #             return self.__ServerError[ServerError]
    #         case _:
    #             return None

class BaseSession(requests.Session):
    def __init__(self, BaseURL: str = "", DefaultHeaders: dict = {}) -> None:
        super().__init__()
        self.BaseURL = BaseURL
        self.headers = DefaultHeaders
        self.__proxies = []
        self.proxyindex = 0
        self.rotate_proxies = False
        self.__current_proxy = None
         
        
    @property
    def base_url(self):
        return self.__BaseURL
    
    @base_url.setter
    def base_url(self, BaseURL):
        self.__BaseURL = BaseURL 

    def set_proxies(self, proxies:list) -> None:
        self.__proxies = proxies
        
    def enable_rotate_proxies(self, enable: bool) -> None:
        self.rotate_proxies = enable
        
    def updateNewProxy(self):
        if self.proxyindex == len(self.proxies) :
            self.proxyindex = 0
        self.__current_proxy = self.__proxies[self.proxyindex]
        self.proxyindex += 1

    def get(self,endpoint: str, params: dict = None, headers=None, cookies=None, auth=None,
            timeout=None,allow_redirects=True, proxies=None, verify=None, stream=None,
            cert=None, data=None, json=None ,**kwargs ,
            ) -> NewResponse:
        _headers:dict = self.headers.copy()
        if headers is not None :
            _headers.update(headers)

        if self.rotate_proxies and self.__proxies:
            self.updateNewProxy()
            self.proxies.update({"http": self.__current_proxy, "https": self.__current_proxy})
        
        url = self.BaseURL + endpoint 
        return NewResponse(super().get(url, params=params, headers=_headers or self.headers, cookies=cookies,
                            auth=auth, timeout=timeout, allow_redirects=allow_redirects,
                            proxies=proxies, verify=verify, stream=stream, cert=cert, data=data,
                            json=json))

    def post(self,endpoint: str, data=None, json=None, headers=None, cookies=None, auth=None,
            timeout=None, allow_redirects=True, proxies=None, verify=None, stream=None,
            cert=None , **kwargs
            ) -> NewResponse:
        
        _headers:dict = self.headers.copy()
        if headers is not None:
            _headers.update(headers)

        if self.rotate_proxies and self.__proxies:
            self.updateNewProxy()
            self.proxies.update({"http": self.__current_proxy, "https": self.__current_proxy})
        
        url = self.BaseURL + endpoint 
        return NewResponse(super().post(url, data=data, json=json, headers=_headers, cookies=cookies,
                                auth=auth, timeout=timeout, allow_redirects=allow_redirects,
                                proxies=proxies, verify=verify, stream=stream, cert=cert))

class Requests(object):

    def __init__(self, BaseURL: str = "", DefaultHeaders: dict = {}) -> None:
        super().__init__()
        self.__headers = DefaultHeaders
        self.__BaseURL = BaseURL

    def updateHeaders(self , h:dict):
        self.__headers.update(h)
    @property
    def base_url(self):
        return self.__BaseURL
    
    @base_url.setter
    def base_url(self, BaseURL):
        self.__BaseURL = BaseURL 

    def get(self, 
            URL: str = None,
            params: dict = None, 
            headers: dict = None, 
            cookies: dict = None,
            auth: tuple = None, 
            timeout: float = None, 
            allow_redirects:bool = True, 
            proxies: dict = None,
            verify: bool = True, 
            stream: bool = False ) -> NewResponse:
        
        if URL is not None:
            url = self.__BaseURL + URL
        else :
            url = self.__BaseURL
        headers = self.__headers.copy()

        if headers is not None:
            headers.update(headers)

        return NewResponse(requests.get(url, params=params, headers=headers, cookies=cookies, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, verify=verify,
                                stream=stream))

    def post(self,
            URL: str = None, 
            data: dict = None, 
            json: dict = None, 
            headers: dict = None, 
            cookies: dict = None,
            auth: tuple = None, 
            timeout: float = None, 
            allow_redirects: bool = True, 
            proxies: dict = None,
            verify: bool = True, 
            stream: bool = False ) -> NewResponse:
        
        if URL is not None:
            url = self.__BaseURL + URL
        else :
            url = self.__BaseURL

        headers = self.__headers.copy()
        
        if headers is not None:
            headers.update(headers)
        return NewResponse(requests.post(url, data=data, json=json, headers=headers, cookies=cookies, auth=auth,
                                 timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, verify=verify,
                                 stream=stream))

