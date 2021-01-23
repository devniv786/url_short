import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":10,"name":"Ronaldo","views":1100},
        {"likes":100,"name":"Nivesh","views":5100},
        {"likes":120,"name":"Binil","views":1000}]

for i in range(len(data)):

    response = requests.put(BASE + "video/"+str(i),data[i])
    print(response.status_code)
    print(response.json())

# input()
# response = requests.delete(BASE+"video/0")
# print(response)
input()
#response = requests.get(BASE + "video/0")
response = requests.patch(BASE + "video/2", {"views":99,"name":"Nivesh","likes":500000})
print(response.json())
