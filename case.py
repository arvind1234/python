import requests
import math
import sys
import argparse
 
# create parser
parser = argparse.ArgumentParser()
 
###
## needs python3
## run as 
## python3 case.py <receipt#>  <form> <center> <offset>
## all parameters are optional and defaults to 2190218894, i-765, 120000
###
# add arguments to the parser
parser.add_argument("--receipt", "-r", dest="receipt", type=int, help="Number portion of the receipt without center prefix")
parser.add_argument("--center", "-c", dest="center", default="LIN", help="Center prefix of receipt number, defaults to LIN")
parser.add_argument("--offset", "-o", dest="offset", type=int, default=120000, help="How far back do you want to start, defaults to 120000")
parser.add_argument("--form", "-f", dest="form", default="i-765", help="Form you are searching for in lower case, defaults to i-765")
 
# parse the arguments
args = parser.parse_args()

url = "https://egov.uscis.gov/casestatus/mycasestatus.do"
r = args.receipt
form = args.form
prefix = args.center
offset = args.offset
r -= offset

print(F"Processing receipt number {r} with offset {offset} with form {form} in center {prefix} ")

e = r
s = r - 2000

#Content type must be included in the header
header = {"content-type": "application/json"}

def find_case(s):
  for i in range(s - 10, s + 10):
    res = requests.post(url, {"appReceiptNum": F"{prefix}{i}"}, header).text.lower()
    if "validation error(s)" in res:
      print(F"Error in {prefix}{i}")
      return True
    if form in res:
      if "approved" in res:
        print(F"X Approved:{i}")
        approved_cases.append(i)
        return True
      else:
        print(F"! Not approved:{i}")
        cases.append(i)
        return False
    else:
      print(F"{form} not found in {prefix}{i}")
  return False

# curl ';jsessionid=0B7104EAEDB50D22906DC1109CF91758' \
# -XPOST \
# -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Origin: https://egov.uscis.gov' \
# -H 'Cookie: JSESSIONID=0B7104EAEDB50D22906DC1109CF91758; _ga=GA1.3.1168278628.1584296322; _gat_GSA_ENOR0=1; _gid=GA1.3.476605453.1584296322; 3cbb7032b4319f7a013efe7b56e63a2a=2341d721107bb7fd82c9ef13669b8418' \
# -H 'Content-Length: 133' \
# -H 'Accept-Language: en-us' \
# -H 'Host: egov.uscis.gov' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15' \
# -H 'Referer: https://egov.uscis.gov/casestatus/mycasestatus.do' \
# -H 'Accept-Encoding: gzip, deflate, br' \
# -H 'Connection: keep-alive' \
# --data 'changeLocale=&completedActionsCurrentPage=0&upcomingActionsCurrentPage=0&'
approved_cases = []
cases = []
while e - s > 1 :
  m = (s + e) / 2
  print(F"m={m}, s={s}, e={e}")
  if find_case(math.floor(m)):
    s = math.floor(m)
  else:
    e = math.floor(m)






# for r1 in reversed(range(2011350349, 2011350549)):
#   res = requests.post(url, {"appReceiptNum": F"WAC{r1}"}, header).text.lower()
#   # print(r1)
#   if "i-539" in res:
#     if "approved" in res:
#       approved_cases.append(r1)
#       print(F"X Approved:{r1}")
#       break
#     else:
#       cases.append(r1)
#       print(F"! Not approved:{r1}")


print(F"Approved {form}......")
print(approved_cases)

print("-----------------------------")
print(F"Non - Approved {form}......")
print(cases)
