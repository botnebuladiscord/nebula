import pyrebase


config = {
    'apiKey': "AIzaSyC6i2U3X43iq8YgVu4nd40dg1WacS45kRo",
    'authDomain': "storied-scarab-353711.firebaseapp.com",
    'projectId': "storied-scarab-353711",
    'storageBucket': "storied-scarab-353711.appspot.com",
    'serviceAccount': 'static/auth-firebase.json'
}

storage = pyrebase.initialize_app(config)