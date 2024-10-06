import os
from flask import Flask, send_file, render_template, abort, request, redirect, url_for

app = Flask(__name__)

# Define the base directory for videos and thumbnails
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, 'videos')
THUMBNAILS_PATH = os.path.join(VIDEO_PATH, 'thumbnails')

# Function to list available video titles (files in the videos folder)
def get_available_videos():
    videos = []
    for filename in os.listdir(VIDEO_PATH):
        if filename.endswith('.mp4'):  # You can add more video formats here
            videos.append(filename.split('.')[0])
    return videos

# Function to list all movie files in the video directory
def get_movie_list():
    movies = [f.split('.')[0] for f in os.listdir(VIDEO_PATH) if f.endswith('.mp4') or f.endswith('.mkv')]  # List only mp4 files
    return movies

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the search query if any
    search_query = request.form.get('search', '')

    # Get the list of movies
    all_movies = get_movie_list()

    # Filter movies based on the search query (case-insensitive)
    if search_query:
        movies = [movie for movie in all_movies if search_query.lower() in movie.lower()]
    else:
        movies = all_movies

    # Render the index page with the list of movies
    return render_template('index.html', movies=movies, search_query=search_query)

@app.route('/video/<filename>')
def video(filename):
    # Construct the full path to the video file based on the filename parameter
    video_path = os.path.join(VIDEO_PATH, filename+".mp4")
    print(video_path)
    if os.path.exists(video_path):
        return send_file(video_path, mimetype='video/mp4')
    else:
        abort(404, description=f"File {filename} not found")


@app.route('/sub/<filename>')
def sub(filename):
    # Construct the full path to the subtitle file based on the filename parameter
    subtitle_path = os.path.join(VIDEO_PATH, "subtitles\\"+filename+".vtt")
    print(f"Requested subtitle file path: {subtitle_path}")  # Debugging line

    # Check if the subtitle file exists
    if os.path.exists(subtitle_path):
        print(f"Serving subtitle file: {subtitle_path}")  # Debugging line
        return send_file(subtitle_path)
    else:
        print(f"Subtitle file {subtitle_path} not found")  # Debugging line
        abort(404, description=f"Subtitle file {filename} not found")

@app.route('/thumbnails/<filename>')
def thumbnail(filename):
    # Construct the full path to the thumbnail image based on the chapter parameter
    thumbnail_path = os.path.join(THUMBNAILS_PATH,filename+".jpg")
    print(thumbnail_path)
    if os.path.exists(thumbnail_path):
        return send_file(thumbnail_path, mimetype='image/jpeg')
    else:
        abort(404, description=f"Thumbnail for chapter {filename} not found")

def mysplit(s):
    head = s.rstrip('0123456789')
    tail = s[len(head):]
    return head, tail

@app.route('/preview/<filename>')
def preview(filename):
    # Construct the full path to the thumbnail image based on the chapter parameter
    thumbnail_path = os.path.join(VIDEO_PATH, "preview\\"+mysplit(filename)[0]+"\\"+filename+".jpg")
    print(thumbnail_path)
    if os.path.exists(thumbnail_path):
        return send_file(thumbnail_path, mimetype='image/jpeg')
    else:
        abort(404, description=f"Thumbnail for chapter {filename} not found")

@app.route('/watch/<filename>',methods=['POST','GET'])
def watch(filename):
    if request.method == 'POST':    
        video_file = request.form['movie']
        chapters = []  # Replace with actual logic if you have chapter info
        print(video_file)
        # Render the video player page for a specific movie
        return render_template('video.html', video_filename=filename, chapters=chapters)
    elif request.method == 'GET':
        video_file = filename
        chapters = []  # Replace with actual logic if you have chapter info
        print(video_file)
        # Render the video player page for a specific movie
        return render_template('video.html', video_filename=video_file, chapters=chapters)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
