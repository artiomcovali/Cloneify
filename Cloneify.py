from dotenv import load_dotenv
import os, base64
from requests import post,get, put
import json
import spotipy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import font
import tkinter, customtkinter 
from PIL import Image, ImageTk
from urllib import request
import io

# Add permanent environment variables - copy this into terminal (if using bash, replace ~/.zshrc with ~./bash_profile):
# echo "export SPOTIPY_CLIENT_ID=[YOUR CLIENT ID]" >> ~/.zshrc
# echo "export SPOTIPY_CLIENT_SECRET=[YOUR CLIENT SECRET]" >> ~/.zshrc
# echo "export SPOTIPY_REDIRECT_URI=http://localhost:8000/callback/" >> ~/.zshrc

# Make sure to download the font


client_id = "YOUR CLIENT ID"
client_secret = 'YOUR CLIENT SECRET'
redirect_url = "http://localhost:8000/callback/"


scope = "user-library-read playlist-modify-public playlist-modify-private ugc-image-upload" 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

user = sp.current_user()
userPfp = user["images"][0]["url"]
userName = user["display_name"]
user_id = user["id"]



def checkbox_event():
    if check_var.get() == "off":
        checkChangePfp = False
    else:
        checkChangePfp = True


def makeNewPlaylist(playlist_Id):
    def getToken():
        authString = client_id + ":" + client_secret
        authBytes = authString.encode("utf-8")
        auth64 = str(base64.b64encode(authBytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials", "code": "AQDWHi2KyDmssw6nMc0aUmRI9Sgnr659WuCeqYvfGNB51Q3i_BNrNuAb8cj1YSuTAU_4BTQxp0dn9rW9kIu7HKkD40EuWNSHLfGPzoGyxUVqtIgSHF_r68sVVHULoH0kdDobMTNga2iI2SlY5HWEbU8gIYRpcKlWGKlwVyAU2UJ4LU0e4jEi-JQZLtgvd4Gxft48mCUHvRKYAtzhrQ"}
        result = post(url, headers=headers, data=data)
        jsonResult = json.loads(result.content)
        token = jsonResult["access_token"]
        return token

    def getHeader(token):
        return{"Authorization": "Bearer " + token} 
        

    def getUserId(token):
        url = "https://api.spotify.com/v1/me"
        headers = getHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)
        return(jsonResult)

    def getPlaylist(token, playlistId):
        url = f"https://api.spotify.com/v1/playlists/{playlistId}"
        headers = getHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)
        return(jsonResult)
    
    


    token = getToken()
    try:
        playlist = getPlaylist(token, playlist_Id)
    except:
        insert.configure(text="Please enter a valid public playlist URL!", text_color="#d94227")


    copiedPlaylistName = playlist["name"]


    thumbnail = playlist["images"][0]["url"]
    with request.urlopen(thumbnail) as url:
        image_data = url.read()

    newPfp = base64.b64encode(image_data).decode("utf-8")
    playlist = playlist["tracks"]
    songs = []

    for idx,i in enumerate(playlist["items"]):
        songs.append(playlist["items"][idx]["track"]["id"])




    try:
        newPlaylist = sp.user_playlist_create(user_id, copiedPlaylistName, public=True, collaborative=False, description="Cloned using Cloneify. Learn more at https://github.com/artiomcovali/Cloneify")

        sp.playlist_add_items(newPlaylist["id"], songs, position=None)

        if check_var.get() == "off":
            checkChangePfp = False
        else:
            checkChangePfp = True

        if checkChangePfp == True:
            sp.playlist_upload_cover_image(newPlaylist["id"], newPfp)
        insert.configure(text="Successfully cloned playlist!", text_color="#51ad4c")
        insert.update()
    except:
        insert.configure(text="Error occured. Please try again!", text_color="#d94227")
        insert.update()


tempId = ''
playlist_id = ''

def getLink():
    insert.configure(text="Playlist Link:", text_color="white") 
    insert.update()
    tempId = ''
    playlist_id = ''
    tempId = enter.get()
    tempId = tempId[34:]
    

    for idx,i in enumerate(tempId):
        if tempId[idx]!='?':
            playlist_id = playlist_id + tempId[idx]
        else:
            break
    makeNewPlaylist(playlist_id)


with request.urlopen(userPfp) as url:
        image_data = url.read()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk()
app.geometry("800x500")
app.title("Cloneify")

image = Image.open(io.BytesIO(image_data))
photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(100, 100))
image_label = customtkinter.CTkLabel(app, image=photo, text="")  
image_label.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)

welcome = customtkinter.CTkLabel(master=app, text="Welcome, " + userName, font=("rubik", 40), text_color="white")
welcome.place(relx=0.5, rely=0.1+.2, anchor=tkinter.CENTER)

insert = customtkinter.CTkLabel(master=app, text="Playlist Link:", font=("rubik", 25), text_color="white")
insert.place(relx=0.5, rely=0.25+.2, anchor=tkinter.CENTER)

linkVar = tkinter.StringVar()
enter = customtkinter.CTkEntry(master=app, width=650, height=40, textvariable=linkVar, font=("rubik", 15))
enter.place(relx=0.5, rely=0.35+.2, anchor=tkinter.CENTER)



check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(app, text="Clone playlist cover image", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off", font=("rubik", 16), fg_color="#ba2fd6", hover_color="#802fd6")
checkbox.place(relx=0.5, rely=0.64, anchor=tkinter.CENTER)

submit = customtkinter.CTkButton(master=app, text="Clone!", fg_color="#802fd6", corner_radius=100, hover_color="#ba2fd6", command=getLink, font=("rubik", 30))
submit.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)

app.mainloop()



