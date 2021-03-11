import requests
import config.__setting__ as settings

IAMPORT_URL = 'https://api.iamport.kr'
IAMPORT_PAYMENTS_URL = 'https://api.iamport.kr/payments'


def get_tokent():
    
    url = IAMPORT_URL + "/users/getToken"

    data = {
        'imp_key' : settings.IAMPORT_KEY, 
        'imp_secret'  : settings.IAMPORT_SECRET_KEY
    }
    request = requests.post(url, data=data) 
    access_request = request.json()

    if access_request['code'] == 0:
        return access_request['response']['access_token']
    else:
        return None

# 결제 진행
def payments_prepare(order_id, amount, *args, **kwargs):
    token = get_tokent() 
    if token:
        data = {
            'amount' : amount,
            'merchant_uid': order_id,
        }

        url = IAMPORT_PAYMENTS_URL + '/prepare'
        headers = {
            'Authorization': token
        }
        request = requests.post(url, data=data, headers=headers)
        access_request = request.json()

        if access_request['code'] != 0:
            raise ValueError('PREPARE   ERROR')
    else:
        raise ValueError('TOKEN ERROR') 


#결제 완료 확인
def find_transaction(merchant_order_id, *args, **kwargs):
    token = get_tokent()
    if token:
        url = IAMPORT_PAYMENTS_URL + '/find/' + merchant_order_id
        headers = {
            'Authorization':token
        }
        request = requests.post(url, headers=headers)
        access_request = request.json()


        if access_request ['code'] == 0:
            response = access_request['response']

            context = {
                'imp_id':response['imp_uid'],
                'merchant_order_id':response['merchant_uid'],
                'amount':response['amount'],
                'status':response['status'],
                'type':response['pay_method'],
                'receipt_url':response ['receipt_url']
            }
            return context
        else:
            return None

    else:
        raise ValueError('TOKEN ERROR')

#환불
def order_cancel(merchant_order_id, reason, amount, *args, **kwargs):
    token = get_tokent()
    if token:
        url = IAMPORT_PAYMENTS_URL + '/cancel/'
        headers = {
            'Authorization':token
        }
        data = {
            'reason':reason,
            'merchant_uid': merchant_order_id,
            'amount': amount,
        }
        request = requests.post(url, headers=headers, data=data)
        access_request = request.json()

        return access_request
    else:
        raise ValueError('TOKEN ERROR')

