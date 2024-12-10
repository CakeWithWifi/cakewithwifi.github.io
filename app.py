from flask import Flask, request, redirect, render_template, url_for
import random
import string
import os

app = Flask(__name__)

url_mapping = {}

def generate_short_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_link = generate_short_link()
        url_mapping[short_link] = long_url
        short_url = f"http://cakewithwifi.github.io/{short_link}"

        # Save the new webpage
        save_html_file(short_link, long_url)

        return redirect(url_for('shortened', short_url=short_url))
    return render_template('index.html')

@app.route('/shortened')
def shortened():
    short_url = request.args.get('short_url')
    return render_template('shortened.html', short_url=short_url)

@app.route('/<short_link>')
def redirect_to_long_url(short_link):
    long_url = url_mapping.get(short_link)
    if long_url:
        return redirect(long_url)
    return 'URL not found', 404

def save_html_file(short_link, long_url):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Redirecting...</title>
        <meta http-equiv="refresh" content="0; url={long_url}">
    </head>
    <body>
        <p>If you are not redirected automatically, follow this <a href="{long_url}">link</a>.</p>
    </body>
    </html>
    """
    file_name = f"{short_link}.html"
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'w') as file:
        file.write(html_content)

if __name__ == '__main__':
    app.run(debug=True)
