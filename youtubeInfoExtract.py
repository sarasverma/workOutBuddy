import youtube_dl, requests, os

#initialize youtube_dl
ydl = youtube_dl.YoutubeDL()

def getInfo(url):
    with ydl:
        if ("playlist?" in url):
            return Exception("Playlist link doesnot support !")
        if("&list" in url):
            url = url.split('&')[0]
        youtube_video = ydl.extract_info(url, download=False)

    informations = ['id', 'title', 'channel', 'view_count', 'channel_id', 'duration', 'categories', 'tags']

    # return a dictionary with all informations
    result = {}
    for key in informations:
        # formatting it for database
        if type(youtube_video[key]) == str:
            value = '"'+youtube_video[key]+'"'
        elif type(youtube_video[key]) == list:
            value = "json_array("+ str(youtube_video[key])[1:-1]+")"
        else:
            value = str(youtube_video[key])
        result[key] = value

    # for thumbnail
    try:
        img = requests.get(youtube_video['thumbnail'])
        if(os.path.isdir(r'img') == False):
            os.makedirs(r'img')
        #saving img
        with open(fr'img/{youtube_video["id"]}.png', 'wb') as f:
            f.write(img.content)
    except:
        raise Exception("Thumbnail could not be saved !")

    #return {key: youtube_video[key] for key in informations }
    return result

if __name__ == "__main__":
    # result = getInfo("https://youtu.be/_shA5Xwe8_4")
    result = getInfo("http")
    print(result)