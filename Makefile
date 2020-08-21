run:
	pipenv run python3 main.py

init:
	pipenv install -r requirements.txt

docker:
	docker build -t conixcenter/arena-runtime-simulated .
	# do 'docker login' before
	docker push conixcenter/arena-runtime-simulated