from flask import Flask, request, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

# In-memory dictionary to store short and long URLs
url_mapping = {}

# Function to generate a random short URL
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_code = generate_short_code()
        url_mapping[short_code] = long_url
        short_url = request.host_url + short_code  # Full shortened URL
        return render_template("result.html", short_url=short_url)
    return render_template("index.html")

@app.route("/<short_code>")
def redirect_to_long(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
