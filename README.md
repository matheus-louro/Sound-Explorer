# SoundExplorer
#### Projeto final do curso CS50’s Introduction to Computer Science | Harvard University
## Introduction:
The SoundExplorer project was created with the aim of expanding the user's musical taste. Many people find themselves stuck with certain artists and music genres, and they may not give other artists a chance. The goal of the project is precisely to reverse this situation and help people discover new songs and appreciate this art form more.

To provide artist and songs recommendations, it was decided to leverage the world's largest music streaming platform, Spotify. In addition to its vast user base, Spotify offers an API that provides the necessary data to build an application capable of making personalized recommendations for each user. 

## Prerequisites and Dependency Installation:
Before getting started with SoundExplorer, make sure your environment meets the following prerequisites and follow the instructions to install the necessary dependencies:

### <strong>Python:</strong> 
Make sure you have Python installed on your system. You can download it from the official Python website (https://www.python.org) and follow the installation instructions specific to your operating system.
### <strong>Spotify Credentials:</strong>
- Visit the Spotify Developer Dashboard at https://developer.spotify.com/dashboard/ and log in with your Spotify account or create a new one if you don't have an account already.
- Create a new application by clicking on the 'Create an App' button and provide the necessary information such as the app name and description.
- Once your application is created, you will be redirected to the application dashboard. Here, you can find your Client ID and Client Secret. These credentials will be used to authenticate your application with the Spotify API.

- In the Spotify Developer Dashboard, make sure to configure the Redirect URI to match the URL where your SoundExplorer application will be hosted. For local development, you can use 'http://localhost:5000/callback' as the Redirect URI.

### <strong>.env example:</strong> 
The .env file stores the environment variables necessary for the application to function and should have the following structure:
```
CLIENT_ID = your_client_id
CLIENT_SECRET = your_client_secret
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "user-library-read playlist-read-private user-top-read user-read-private playlist-modify-public"
```
- This file is an example of an environment file that should be filled with your Spotify credentials and renamed to .env. 
- Make sure to replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your own credentials obtained from the Spotify Developer Dashboard. <br>
- By default, Flask runs on port 5000, but you can change it according to your preferences, just make sure to keep the /callback route. <br>
- The SCOPE variable already includes all the necessary scopes for the application to work. <br>
- Note: the REDIRECT_URI variable must be the same as the one you defined in the Spotify Developer Dashboard.

### <strong>Dependencies Installation:</strong>
SoundExplorer uses some Python libraries. To install all dependencies at once, run the following command:

```
pip install -r requirements.txt
```
Make sure you are in the SoundExplorer project directory when running this command. The requirements.txt file contains the list of all required dependencies along with their specific versions.

If you need to add or update any dependencies, update the requirements.txt file and run the above command again.

<strong>Other Dependencies:</strong> In addition to the libraries mentioned above, SoundExplorer also makes use of other standard Python dependencies such as os, flash, redirect, render_template, request, session, jsonify, random and time. These dependencies are typically included in the standard Python installation.
## Design choices:

The development of the SoundExplorer project was structured with the aim of exploring the content presented in the CS50 course. Therefore, the technologies and design choices used in the project were inspired by what was taught during the course, with a focus primarily on the web development concepts covered.
Below, we detail some of these choices:

## Architecture and Technologies Used:
In this project, we used an architecture based on the Flask framework, combining technologies such as HTML, CSS, JavaScript, Bootstrap, and the Spotipy library in Python.

We chose Flask due to its simplicity and flexibility. It allows us to build a fast and scalable web application while providing a comprehensive set of tools for handling routes, authentication, and data manipulation.

For creating the user interfaces, we used HTML and CSS for structuring and styling the pages, using Jinja to generate HTML templates. Additionally, the Bootstrap framework was incorporated to streamline development and provide a consistent experience across different devices and screen sizes.

The interactivity of the site is implemented with JavaScript, enabling a more dynamic and responsive experience for users. This choice allows us to manipulate data in real-time, make requests to the Spotify API, and update the interface asynchronously using AJAX.

## Integration with the Spotify API and Spotipy:
The integration with the Spotify API was one of the key features of SoundExplorer. We utilized the Spotipy library in Python, which provides a convenient interface for interacting with the Spotify API, especially for authentication and access token management.

By leveraging the Spotify API, we were able to access information about songs, artists, playlists, and personalized recommendations based on user preferences. These data were processed and presented to users through the website.

To ensure security and protect the API credentials, we stored them in an .env file, which is excluded from version control using the .gitignore file. This way, we keep the confidential information secure and avoid accidental exposure.

## User Interfaces:
The user interfaces of SoundExplorer were designed with the goal of providing an intuitive and enjoyable experience for users. We utilized Bootstrap to create a responsive layout and reusable components that adapt to different devices and screen sizes.

For the color design, we drew inspiration from Spotify's colors (black and green) to create a familiar environment for users who are accustomed to using Spotify as their primary music streaming platform.

## File Structure:

### <strong>README.md:</strong> 
This readme file that you are currently reading, containing information about the project and its usage.

### <strong>static: </strong>
Directory containing the static files of the website, such as images, font, CSS, and JavaScript.
- <strong>font:</strong> Directory containing the font used on the website. 
- <strong>images:</strong> Directory containing the images used on the website. 
- <strong>js:</strong> Directory containing the <strong>script.js</strong>, responsible for some website customizations and AJAX. 
### <strong>style.css</strong>:
CSS file responsible for styling the website.

### <strong>templates:</strong>
Directory with the HTML files.
- <strong>login.html:</strong> "Login page where the user logs in with their Spotify account. 
- <strong>layout.html:</strong> The base file that contains the common structure for all pages of the website, such as header and navigation elements. 
- <strong> index.html: </strong> Homepage of the website displaying options for the user to discover a new artist, receive songs recommendations, or view the top tracks of the moment. 
- <strong>artists.html:</strong> The "artists" page is where an artist is recommended based on the user's most listened artists on Spotify, showing their top 10 popular songs. This artist is generated by the artist_related_artists() function from the Spotipy library, and the "Next Artist" button on the page triggers an asynchronous request that returns another artist, allowing the user to see a new artist without refreshing the page. 
- <strong>songs.html:</strong> The "songs" page creates a playlist in the user's Spotify library with 100 songs generated using the recommendations() function from the Spotipy library. This function accepts a maximum of 5 items in its parameters and generates recommendations based on either the user's top 5 favorite artists or the 5 most listened songs within a specific time interval. In the case of SoundExplorer, we use the user's top 5 favorite artists as we believe it captures the essence of the user's musical taste more effectively. 
- <strong>top_tracks.html:</strong> The "top_tracks" page displays the Spotify's Top 50 Global playlist, which shows the most listened songs worldwide at the moment and is continuously updated by Spotify itself. Additionally, the page also shows the Top 50 most played songs in the user's country, which is also an official Spotify playlist. 

### <strong>app.py:</strong>
The main file that configures the server and handles the application routes.

## Contact:
<strong>Email: mhenriqueml561@gmail.com</strong>
