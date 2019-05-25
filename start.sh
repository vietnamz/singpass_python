export DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY=./ssl/stg-demoapp-client-privatekey-2018.pem
export MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT=./ssl/stg-auth-signing-public.pem

export MYINFO_APP_CLIENT_ID=STG2-MYINFO-SELF-TEST
export MYINFO_APP_CLIENT_SECRET=44d953c796cccebcec9bdc826852857ab412fbe2
export MYINFO_APP_REDIRECT_URL=http://localhost:3001/callback
export MYINFO_APP_REALM=http://localhost:3001
export PROJECT_ID=''

#############################
# FOR version 2.1 APIs only
############################

# L0 APIs
# export AUTH_LEVEL=L0
# export MYINFO_API_AUTHORISE='https://myinfosgstg.api.gov.sg/dev/v2/authorise'
# export MYINFO_API_TOKEN='https://myinfosgstg.api.gov.sg/dev/v2/token'
# export MYINFO_API_PERSON='https://myinfosgstg.api.gov.sg/dev/v2/person'

# L2 APIs
# export AUTH_LEVEL=L2
# export MYINFO_API_AUTHORISE='https://myinfosgstg.api.gov.sg/test/v2/authorise'
# export MYINFO_API_TOKEN='https://myinfosgstg.api.gov.sg/test/v2/token'
# export MYINFO_API_PERSON='https://myinfosgstg.api.gov.sg/test/v2/person'


##############################
# FOR version 2.2 APIs only
##############################

# SANDBOX ENVIRONMENT (no PKI digital signature)
export AUTH_LEVEL=L0
export MYINFO_API_AUTHORISE='https://sandbox.api.myinfo.gov.sg/com/v2/authorise'
export MYINFO_API_TOKEN='https://sandbox.api.myinfo.gov.sg/com/v2/token'
export MYINFO_API_PERSON='https://sandbox.api.myinfo.gov.sg/com/v2/person'

# TEST ENVIRONMENT (with PKI digital signature)
export AUTH_LEVEL=L2
export MYINFO_API_AUTHORISE='https://test.api.myinfo.gov.sg/com/v2/authorise'
export MYINFO_API_TOKEN='https://test.api.myinfo.gov.sg/com/v2/token'
export MYINFO_API_PERSON='https://test.api.myinfo.gov.sg/com/v2/person'
export GOOGLE_APPLICATION_CREDENTIALS='./key.json'

python main.py 