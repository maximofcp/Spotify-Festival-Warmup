1. Install ngrok (mac:   brew install ngrok/ngrok/ngrok)
2. Setup ngrok token (ngrok config add-authtoken <token>)
3. Start ngrok (make ngrok)
4. Copy forwarding address into app's and spotify's configuration (don't forget to add /generate-code endpoint to it)
5. Start endpoint to catch the auth code (make run)
6. Copy the code from the browser and add it to app settings CODE
7. Create playlists (make playlists)