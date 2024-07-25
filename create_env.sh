# Configurando projeto para o ENV
# Antes de tudo deve-se desabilitar o pip.ini do acesso global.
# Caso tenha erro para instalar o psycopg2 executar os seguintes comandos:
# sudo apt-get -y install postgresql
# sudo apt-get install libpq-dev
# sudo apt install python3-virtualenv
python3 -m venv env;
source env/bin/activate;
python3 -m pip install --upgrade pip;
pip install twine keyring artifacts-keyring;
sudo cp pip.ini env/pip.conf;
pip install -r requirements.txt;