setup:
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt

launch:
	sudo cp ai_diagbe.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable ai_diagbe
	sudo systemctl restart ai_diagbe
	sleep 3; make status

start: launch


status:
	sudo systemctl status ai_diagbe ; sudo netstat -ntpav | grep 9000 || echo "\nERROR!\nCannot find 9000 port listening\n"
