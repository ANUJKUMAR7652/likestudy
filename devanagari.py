ltw1import urllib.request
print("Naya Hindi font download ho raha hai...")
# Lohit Devanagari font (Bahut stable hai)
url = "https://github.com/fedora-hindi/lohit-hindi/raw/master/Lohit-Hindi.ttf"
urllib.request.urlretrieve(url, "devanagari.ttf")
print("✅ 'devanagari.ttf' mil gayi!")
