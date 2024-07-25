##Configurando projeto para o ENV
##Antes de tudo deve-se desabilitar o pip.ini do acesso global.
$executingScriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Write-Host ($executingScriptDirectory)
cd $executingScriptDirectory
pip install virtualenv --proxy 10.172.197.66:82
python -m virtualenv $executingScriptDirectory\env
.\env\Scripts\activate
.\env\Scripts\python.exe -m pip install --upgrade pip --proxy 10.172.197.66:82
pip install twine keyring artifacts-keyring --proxy 10.172.197.66:82
Copy-Item $executingScriptDirectory\pip.ini $executingScriptDirectory\env -Force
pip install -r requirements.txt --proxy 10.172.197.66:82
