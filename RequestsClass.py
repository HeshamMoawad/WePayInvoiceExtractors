import requests

# URL = 'https://pay.jumia.com.eg/api/v3/utilities/order/summary/internet.bill.tedata@fawry'

# headers = {
#     'authority': 'pay.jumia.com.eg' ,
#     'method': 'POST',
#     'path': '/api/v3/utilities/order/summary/internet.bill.tedata@fawry',
#     'scheme': 'https',
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en',
#     'content-length': '3032',
#     'content-type': 'application/json;charset=UTF-8',
#     'cookie': '_gcl_au=1.1.1770403842.1674681967; jpay_app_tmx_session_id=f6801cdb-465e-4f0e-88f8-e5aa51543f68; userLanguage=en_EG; _fbp=fb.2.1674681967920.197242572; _ga=GA1.3.1606906537.1674681968; _gid=GA1.3.1893996276.1674681968; _gat_UA-60910804-8=1; __cf_bm=slh7eKV7.4oBDD8dHIN6KH2V0oRzypImz8n6Wo44WYI-1674683848-0-AdqZLhnM9eQ2JmORc59sxJcsmKT4kUEJHd+AsfrGZPt5/aoYjxyKNXsZlx/6kHf52qDUy7qUMLVqIbxCTtUWuUw=',
#     'origin': 'https://pay.jumia.com.eg',
#     'referer': 'https://pay.jumia.com.eg/ar/services/internet-bills',
#     'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': "Windows",
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#     'x-device-id': 'device-hash',
#     'x-device-version': 'Web',
# }

proxy = {
    "https": 'https://41.33.207.146:443',
    #"http": 'https://129.80.58.106:3128'
}


# payload = {"service_key": "internet.bill.tedata@fawry", "payload": {"phone_number_message": "For landline numbers, you must enter the governate code", "phone_number": "EG_+20221842002", "list_types": "1"}, "form_segments": [{"service_key": "internet.bill.tedata@fawry", "elements": [{"key": "phone_number_message", "label": "For landline numbers, you must enter the governate code", "options":'[]', "template":"message", "title":"", "validators":'[]'}, {"key": "phone_number", "label": "Phone Number", "options": [{"form_elements": '[]', "icon":"", "label":"Egypt", "message":"", "option_value":"EG_+20", "preselected":'false'}], "template":"phone_with_country", "title":"What is your phone number?", "validators":[{"message": "Phone Number is required", "options": '[]', "type":"required"}, {"message": "Invalid phone number", "options":'[]', "type":"phoneNumber"}]}, {"key": "list_types", "label": "fawry_internet_bill_tedata_type_label", "options": [{"display_value": "", "form_elements": '[]', "icon":"", "label":"fawry_internet_bill_tedata_pay_bill_label", "message":"", "option_value":"1", "preselected":'true'}, {"display_value": "", "form_elements": [{"key": "billType_code", "label": "fawry_internet_bill_tedata_buy_extra_bill_type_code_label", "options": [{"display_value": "", "form_elements": '[]', "icon":"", "label":"fawry_internet_bill_tedata_buy_extra_bill_type_code_12720_label", "message":"", "option_value":"12720", "preselected":'false'}, {"display_value": "", "form_elements": '[]', "icon":"", "label":"fawry_internet_bill_tedata_buy_extra_bill_type_code_12721_label", "message":"", "option_value":"12721", "preselected":'false'}, {
#     "display_value": "", "form_elements": '[]', "icon":"", "label":"fawry_internet_bill_tedata_buy_extra_bill_type_code_12722_label", "message":"", "option_value":"12722", "preselected":'false'}], "template":"list", "title":"fawry_internet_bill_tedata_buy_extra_bill_type_code_title", "validators":[{"message": "fawry_internet_bill_tedata_buy_extra_bill_type_code_label is required", "options": '[]', "type":"required"}]}], "icon":"", "label":"fawry_internet_bill_tedata_buy_extra_label", "message":"", "option_value":"2", "preselected":'false'}, {"display_value": "", "form_elements": [{"key": "amount", "label": "Amount", "options": [{"form_elements": '[]', "icon":"EGP", "label":"EGP", "message":"", "option_value":"EGP", "preselected":'true'}], "template":"money", "title":"WHAT IS THE REQUIRED AMOUNT?", "validators":[{"message": "Amount is required", "options": '[]', "type":"required"}, {"message": "Invalid amount", "options": [{"message": "Supported currency: EGP", "option": "currency", "value": "EGP"}, {"message": "Minimum amount: 5 EGP", "option": "min", "value": "5"}, {"message": "Max amount: 1000 EGP", "option": "max", "value": "1000"}], "type": "money"}]}], "icon": "", "label": "fawry_internet_bill_tedata_top_up_label", "message": "", "option_value": "3", "preselected": 'false'}], "template": "list", "title": "fawry_internet_bill_tedata_type_title", "validators": [{"message": "fawry_internet_bill_tedata_type_label is required", "options": '[]', "type":"required"}]}], "step":'1', "step_count":'1', "payload":'[]', "integrity_key":"b568c4f1deaeaa455d7f94d68a963f920ce80cc6"}], "voucher": 'null'}


# response = requests.post(
#     url=URL,
#     headers=headers,
#     data=payload,
#     proxies=proxy,
# )

# print(response)
# print(response.text)
# print(response.status_code)

print(requests.get("https://billing.te.eg/ar-EG?AreaCode=02&PhoneNumber=27038065&PinCode=&InquiryBy=telephone"))


# ur = "https://billing.te.eg/api/Account/Inquiry"


# headers = {
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Connection': 'keep-alive',
#     'Content-Length': '72',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Cookie': '_ga=GA1.2.611413960.1656066340; f5avraaaaaaaaaaaaaaaa_session_=BDDLHMNJBBDLLINDCMNJAKGDPADANDABEGDNLPABKLMEKJAILGFABEHBGKJPFFDIOCJDBINCCLPHBGGPLIKAOHNNNKADAELJBKJMKKNEFJIADILFFLAGAHHHCBGIHJGF; _gcl_au=1.1.1941158367.1674685471; _ga=GA1.3.611413960.1656066340; _gid=GA1.3.899064777.1674685471; culture=ar-EG; UnPaidInvoicesA40023236009266481F187BF11250C214AB5DFEF954=A9187756525422CABD786C0C1FC665F8Sr72yuRMtWDAjHj2KxEfiHAjBtzw3uhaBw5llfiPgROYnD7oTOWSwK2YfP75OrXvJp%2BVK6me%2FgUG4gmFTRdrFRN8Q6MoyHha0KMM2LYOngyEW%2FWnDjxmER%2Fh05EehOhr; token=9266481F187BF11250C214AB5DFEF954202301260028135A5A8A621BC8E1ED3EA09A1F5A2F89F6; TS016e6d92=010aa23b1d7aebe5edd046f08e8d1c1382e9f66f2bd24b8ae13da77732258d8c6829470250537a103a500fc58ddb980f062882b88283c04655ef5d829f6faa9b5ae27170d071928c31acc4aa8c4353f68c1b4358d388c24bcc5992de958813c47956fb6e41',
#     'Host': 'billing.te.eg',
#     'Origin': 'https://billing.te.eg',
#     'Referer': 'https://billing.te.eg/ar-EG?AreaCode=02&PhoneNumber=27038065&PinCode=&InquiryBy=telephone',
#     'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': "Windows",
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#     'X-Requested-With': 'XMLHttpRequest',
# }

# data = "AreaCode=02&PhoneNumber=27038065&PinCode=&InquiryBy=telephone&AccountNo="

# res = requests.post(
#     url=ur ,
#     data= data ,
#     proxies = proxy ,
#     headers = headers ,
#     #proxies = proxy ,
# )

# print(res)
# print(res.text)
# print(res.status_code)


# BaseURL = "https://pay.jumia.com.eg"
# ProxyService =  "http://sp72048375:adelraslan@gate.smartproxy.com:7000"
# APIpathWEhome = "/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"

# number = "2033648"      #"050-2033648"   bill # 142.5
# code = "050"


# jasonCode = f"""[
#             "service_key" => "internet.postpaid.wehome@aman",
#             "payload" => [
#                 "phone_number" => "EG_+20" . {code} . {number},
#                 "phone_number_message" =>
#                     "For landline numbers, you must enter the governate code",
#             ],
#             "form_segments" => [
#                 [
#                     "service_key" => "internet.postpaid.wehome@aman",
#                     "elements" => [
#                         [
#                             "key" => "phone_number_message",
#                             "label" =>
#                                 "For landline numbers, you must enter the governate code",
#                             "options" => [],
#                             "template" => "message",
#                             "title" => "",
#                             "validators" => [],
#                         ],
#                         [
#                             "key" => "phone_number",
#                             "label" => "Phone Number",
#                             "options" => [
#                                 [
#                                     "form_elements" => [],
#                                     "icon" => "",
#                                     "label" => "Egypt",
#                                     "message" => "",
#                                     "option_value" => "EG_+20",
#                                     "preselected" => false,
#                                 ],
#                             ],
#                             "template" => "phone_with_country",
#                             "title" => "What is your phone number?",
#                             "validators" => [
#                                 [
#                                     "message" => "Phone Number is required",
#                                     "options" => [],
#                                     "type" => "required",
#                                 ],
#                                 [
#                                     "message" => "Invalid phone number",
#                                     "options" => [],
#                                     "type" => "phoneNumber",
#                                 ],
#                             ],
#                         ],
#                     ],
#                     "step" => 1,
#                     "step_count" => 2,
#                     "payload" => [],
#                     "integrity_key" => "19ef610d2e8588e883a3148ba272e0556cc99c25",
#                 ],
#             ],
#         ];"""


# req = requests.post(
#     url = BaseURL + APIpathWEhome,
#     json = jasonCode ,

#     )

# print(req)
# print(req.content)
# print(req.status_code)
# print(req.json())
