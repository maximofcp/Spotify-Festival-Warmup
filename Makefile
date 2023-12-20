run:
	flask --debug run

playlists:
	python create_playlists.py

ngrok:
	ngrok http http://127.0.0.1:5000
