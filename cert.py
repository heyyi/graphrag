import requests
import certifi
import sys

DellRootCACert_CA101PEM='''
# Issuer: CN=Dell Technologies Root Certificate Authority 2019
# Subject: CN=Dell Technologies Root Certificate Authority 2019
# Label: "Dell Technologies Root Certificate Authority 2019"
-----BEGIN CERTIFICATE-----
MIIEITCCAwmgAwIBAgIQGRwh4YLNUKpNzFg7nT7QgjANBgkqhkiG9w0BAQsFADCB
ojELMAkGA1UEBhMCVVMxDjAMBgNVBAgTBVRleGFzMRMwEQYDVQQHEwpSb3VuZCBS
b2NrMRowGAYDVQQKExFEZWxsIFRlY2hub2xvZ2llczEWMBQGA1UECxMNQ3liZXJz
ZWN1cml0eTE6MDgGA1UEAxMxRGVsbCBUZWNobm9sb2dpZXMgUm9vdCBDZXJ0aWZp
Y2F0ZSBBdXRob3JpdHkgMjAxODAeFw0xODA3MjMxNzA3NDVaFw00MzA3MjMxNzE3
NDRaMIGiMQswCQYDVQQGEwJVUzEOMAwGA1UECBMFVGV4YXMxEzARBgNVBAcTClJv
dW5kIFJvY2sxGjAYBgNVBAoTEURlbGwgVGVjaG5vbG9naWVzMRYwFAYDVQQLEw1D
eWJlcnNlY3VyaXR5MTowOAYDVQQDEzFEZWxsIFRlY2hub2xvZ2llcyBSb290IENl
cnRpZmljYXRlIEF1dGhvcml0eSAyMDE4MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEAqlQlbFbW7/Iy6wVtPEmfxbRMliJj4S/0vboVuZySAYI7TtMBAaDu
gBBeKPuKmRD1nUP+T4L0i5KBUFRWq5OvgtDYk8Ig382douSbWe4dwGOvcjNKvbHf
Iki9cVSvgTjaeOtORYXzMlCLw59JT6FtXFKjlW1GrM+TPbb2rjDLNir0IzDYvPUx
INXXnxyBSaBvkTipChTnIqXJJG53xEZIb/tK4NE3vcuP5RTFE0AEZmdY9Ka06x8Y
3X83ifbFZ2ZNTjRYggWdVpXB1PGjlya7FmDyIqlvN9xBdur4QIUhfsefpe8sVE0K
RAv7IFBKwo5X+zFrfFM9KZGRGQsCBhKWgwIDAQABo1EwTzALBgNVHQ8EBAMCAYYw
DwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQU2wDrJV+R+5nGtkgc0GOtX+KntFYw
EAYJKwYBBAGCNxUBBAMCAQAwDQYJKoZIhvcNAQELBQADggEBAKZ5Su5LLbOXtito
8OFAkOs/AxuzRPP16E1ZO8VWN8Q4y0RsCbJ7V+R1QAlhd793X1LnEMHYpnXQLPbg
tWtWcPfoZbVK5zcDCIt4/7XgpCmL6yGGk9SVDkJrZIv+bvlB6P64vR/Fs2BYHaQx
G2ITb2GN4CrU+UxmieBPMvj12epD23R8HIcarKD/ZRCAR3XAd80v2A5mncxSqdHI
PzNT/fmlMgiesEl+IjJqc98HCtVAVa2hLsXkiZiLGKZPmS0cbQTsW/sNBE+s5WlG
Yo++cDfTgqdLiYcTXmx9PPyMwbmzkUr8Mr8dbDBodWSEpVgv6oCej2kGOF6saUAr
/4YKU4g=
-----END CERTIFICATE-----
'''

try:
    requests.get('https://confluence.dell.com')
    print('Dell Root CA in current Python Certificate chain')
    sys.exit(0)
except requests.exceptions.SSLError as err:
    print('SSL Error. Adding custom certs to Certifi store...')
    cafile = certifi.where()
    print("Pythoon current certificate location: [{}]".format(certifi.where()))
    customca = bytes(DellRootCACert_CA101PEM, 'utf-8')
    with open(cafile, 'ab') as outfile:
        outfile.write(customca)
    print('Root cert added. Conduct another round of site verification')

try:
    requests.get('https://confluence.dell.com')
    print('View Confluence site, Dell Root CA successfully added to the certifi store')
    sys.exit(0)
except requests.exceptions.SSLError as err:
    print('Failed to add certificate to the certifi store')
    sys.exit(1)

