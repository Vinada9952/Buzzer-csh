# custom sounds

import requests

# response = requests.post("https://myinstants-api.vercel.app/", json=
#     {
#         "id": 3525
#     }
# )

# print(response.json())

response = requests.get( "https://proxy.corsfix.com/?https://myinstants-api.vercel.app/detail?id=akh-70972" )
data = response.text
print(data)