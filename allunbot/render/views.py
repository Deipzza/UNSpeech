from django.shortcuts import render
import requests
from . import views
from .forms import loginUsForm
from .bot import bot
from bs4 import BeautifulSoup 

def index(request):
    return render(request, 'index.html', {})

def login(request):
    data=request.POST
    if data:
        URL = "https://sia.unal.edu.co/ServiciosApp"

        cookies = {
            'OAM_REQ_1': 'invalid',
            'OAM_REQ_COUNT': 'VERSION_4~1',
            'OAM_ID': 'VERSION_4~BMac3f8jLogrovIpeZU/ug==~M7/S3ER3YiOvE4XzH6hjeQtTNPjnoIV6cyH8hxm0HyQRr04QiRL9gt6Ta5a7ftFfk9b10Imb2E+5kAf/5Wc2JN+MNN/WLETnFLr/N6N9KN8ku2JA9qjeJnRXsDdPIU2zuEIiy4kEIFSXMzWXEKC/p9UxpzCTJBCLKIwBI7LHaq/N75Omz//hwg5zBUopxuOQh20QOc+M+QUTuzmIbaYnGWmTd6711Het4ckrWQK5GNG6RIKZWgFE2p4llgNo1wQzcty8AKVAJo6kqueW6ZQC9+d7ydgYrIFq5wRLOOUD1xCgBgHklRMsUKuT3o5P80Yv',
            'JSESSIONID': 'rFj7C3qkO1Ja-vHjEmX4xBwhhug30JzRH1zZ0dVkoWmKgtJl26o3!-1397904885',
            'AWSALB': 'udnLSllCG42tqKEQJDy1SwdbgycfdBAdfODWIQ0A/iDGxGL8zSs0dXg+37k2nC46jkEXtZt2b2sjAuYGDkv74cDcONhYWR2F2QSGsGED47WShzeMds5hqmlHRFtk',
            'AWSALBCORS': 'udnLSllCG42tqKEQJDy1SwdbgycfdBAdfODWIQ0A/iDGxGL8zSs0dXg+37k2nC46jkEXtZt2b2sjAuYGDkv74cDcONhYWR2F2QSGsGED47WShzeMds5hqmlHRFtk',
            'OAM_REQ_0': 'VERSION_4~3kBM2Qvco5D5l%2bvAUFui1TPgVlAFNQylheuB%2beeQyyTVYYEpKvqCym8kRzEk6EGcB4TDEy1CzGnsyC4okPl1bxJBTP7Pyd8pGm7oFjB974MqNdHMJ0tpXTkzr9RNUzUUJBFJSaASeS0wMFE%2fvh6ueWn0mfXImE3YSI%2bk1Cbmy9U%2bGLYSSzzlwxicEBipOvTDHRWeGgbgsZtfOIZ6YbegB4D2q%2b%2b1O0V2%2b1CVg9TeBbadjoD%2bgSbt0PLxAPZYwzVG8AM%2fRUAhPMB95r0OeEcq5HB3EDLrLAFTz1iefd%2baJN%2bEMndd9WMTDwEOefQ%2fvOjqpGWph6rkHe6%2f7pWIGV%2bOrWjPXoJuBQKHe045NBk7Y6IrLeZK2nvvJ8oHHP9hlzaK31gHJTmH%2bsPgnJ%2fPlT2z9dF4ENGIvmXOrnsOZqFIOUUpceT2lStFgRnrnZd%2fkT2SpKIaRfgtRg%2b%2bYvmenQ1Gn6opn30vnSrEp%2fXGJQ%2boJMZUN6pRwQHrPtD93B08LAjkSKalUAXXoQYLc%2bLORIjF4G%2fkirXxS8jARhbSZh8%2bsUuLJo5enVxxazF6in9DOULeps56yK1Ec6ArGH7B49Erce9pYhPZ8TU8zEwh8vvoL0lE99nLoDpajoiUH59glswT%2f8olPBpiqZB2WXJEuV68fxk%2bVsydEYTGtxSKOr7GY7Q0R3TtynnwndKajAdgt0wx1sX8wOPhv%2fFUe30HlanBk9NJFqSCg47u6f9YNmmc5ARbFuOxWCGxAmP9gJXUHyQiAHu8Yd1CdNag43nQV9LFieclUGIn2QDdFPNs9%2fAHKg9lO6VVRc9g3Q4bYMsrAYMGUUJbDG7d8fG18DgGRiCzAwYpj3p5TDBfkiG%2fC3Mu1Mp6LbwtqTZ9lZSGeCgVbZb9%2fOiCgU4PH6fyJl2GtY9QEL6Ug%2f9jLKijIEBi%2fAI9Mn%2bsqWd5aaFf2uABbynTI4fVWC5HHqcDJnEpUeL%2bpp1Gyu%2fyllXNr5CiM5viby3od%2bkpSasBkXFtLqOpclSrgLRTT%2f3IAE%2b2Dn1kk4ESUT5Nci%2bkJ4d4aSBSWc7P4Ad2SuuY36bduyhpVir4a3vJt47EPLGgzQ6W0gOS%2fVLJyhQqrB1A6DFPEIXF42TDMxHB%2bzROyhmjBOX6HJFjiAbi4fOQGGG6f5C%2f9eJwvE4U0%2bL5OIdMoVYG13lwiK7bQG%2fnfV00HMNLw9vK2V9rPyJgn6BjftlO8%2bUDfzXtDLgmYXdKAI94y%2bjvwycOJCh6GI3W3ooUNGMHtJnwMdzMrNO9ac%2b%2baagjRHKKbeZNOP%2bNsDmBTuezK916ohSWk2MpcJyxyiTEwYLW3S7NIpwQmYW68pORU0nUPR07BpgRE8pgZV8iHrLVrj4RhAJYK0suSQOkJzyNJPykKrE0%2fGU%2fyC%2biSCimjJPWX9hdMZaqLoWk11YP9AWTz7RRnKswK1Ilrt7MBmCEzQEneg8Umb0ceIh9DjgApwL258OfLmZVSJt1PRtU%2b0jj7D%2fwY2I8mNS5t%2bbBvdYL5RBPCtM07a8CyDvIfKM6taxQtQLZ6rPJl5HXmBaob03xS74%2fOWdM5ISNGb2GXmxwC3jImZ2TTkAWtx8iV4517Pm2I3Y7tpHcMCRKHj7RxgEgc0G14Gv7GvdKKKhGX5JMXWjDSIjjcoTApmQmi5etVDY%2fuhNzmEzKMZ5zXZ5gv74vOeNvZmn3gCyEmAPb558nC8XaP9adQfr1qoOKnucsRZbVRgqG7COXwlebDCGikbEHqyoA9jzQ1thVyX6HfzptRKIasLrRPBNXQcNSVX2t1OELcAcuNfRo%2fRG3ckmMAMoWhfHlWsxNV5DWvezjgJ2RJLovJlbZbN8N3TRXck1%2brkv%2bHD9CymS64mX2%2fh0%2fRw%3d%3d',
            'ECID-Context': '1.005tCwoA8cb6MQRMyYbe6G0000YW00020b@kXhgv0ZGZKSULGSPXKTPJHSRo4USpLO',
            'SSTT_TRIES': '0',
        }

        data = {
            'username': data["username"],
            'password': data["password"],
            'submit': 'Iniciar Sesión',
        }
        s = requests.session() 
        s.post('https://autenticasia.unal.edu.co/oam/server/auth_cred_submit',cookies=cookies,data=data)
        html = s.get(URL).content
        soup = BeautifulSoup(html, "html.parser")
        usuario = soup.find('a', {'class': 'af_menu_bar-item-text'}).text
        print(usuario)
        return 

    form = loginUsForm()
    return render(request, 'render/login.html', {"form":form})