preinstall:
	@echo "Getting Pip-tools..."
	pip install pip-tools
	@echo "GOOGLE_DRIVE_EMAIL=user@gmail.com" > env.example
	mv env.example .env

install: preinstall
	@echo "Downloading dependencies..."
	pip-compile
	@echo "install dependencies..."
	pip-sync
	@echo "Done."

build: install
	@echo "Collecting staticfiles"
	./manage.py collectstatic --no-input
	@echo "Migrate DB"
	./manage.py migrate

clean:
	@echo "Cleaning un-needed files..."
	@rm -f requirements.txt
	@echo "Done."

