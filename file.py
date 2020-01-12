from firebase import firebase
firebase = firebase.FirebaseApplication('https://pyocr-464c8.firebaseio.com/')
SECRET_KEY = 'gi2m28GsAeA2FPEdYJpAN4MAeM1qAUMZMlboifeQ'
speed = firebase.get("vehicle", "speed")
id = firebase.get("vehicle", "id")
print(speed)
print(id)
if(speed>=3):
    f = open("file.txt", "a")
    f.write( )
    f.close()
