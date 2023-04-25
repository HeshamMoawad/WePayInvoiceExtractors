class Proxy(object):
    def __init__(self,response:dict) -> None:
        self.username = response['username']
        self.password = response['password']
        self.proxy_address = response['proxy_address']
        self.port = response['port']
        self.socks5_proxy_expression = dict(http = f"socks5://{self.username}:{self.password}@{self.proxy_address}:{self.port}",https = f"socks5://{self.username}:{self.password}@{self.proxy_address}:{self.port}")
        self.socks4_proxy_expression = dict(http = f"socks4://{self.username}:{self.password}@{self.proxy_address}:{self.port}",https = f"socks4://{self.username}:{self.password}@{self.proxy_address}:{self.port}")
        self.https_proxy_exepression = dict(http = f"http://{self.username}:{self.password}@{self.proxy_address}:{self.port}",https = f"https://{self.username}:{self.password}@{self.proxy_address}:{self.port}")
        
