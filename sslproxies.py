import requests


h = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Length': '71',
    'Cookie': 'token=B48FA4B0712495394276362E62465E6220230422312040A914D4C153C2E02965E1B8A6C667E42E;',
    'Host': 'billing.te.eg',
    'Origin': 'https://billing.te.eg',
    'Referer': 'https://billing.te.eg/ar-EG',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


data = {
    'AreaCode': '02',
    'PhoneNumber': '3603190',
    'PinCode': '',
    'InquiryBy': 'telephone',
    'AccountNo': '',
}

response = requests.post(
    url="https://billing.te.eg/api/Account/Inquiry",
    headers=h,
    data=data,
    verify=False
)
print(response)
print(response.status_code)
print(response.text)
print(response.json())
# print(response)
