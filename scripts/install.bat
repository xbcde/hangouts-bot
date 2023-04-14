rmdir /s /q venv

python -m venv venv
call .\venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r .\scripts\requirements.txt

pre-commit install
pre-commit install -t commit-msg
