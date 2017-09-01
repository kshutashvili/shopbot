
Setup local copy of shopbot project
===================



Clone repository
-----------------
`git clone git@unruled.cloudapp.net:/var/git/shopbot.git`

install and setup pyenv
-----------------

`git clone https://github.com/pyenv/pyenv.git ~/.pyenv`
`echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc`
`echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc`
`echo 'eval "$(pyenv init -)"' >> ~/.bashrc`
`exec "$SHELL"`

install pyenv-virtualenv
-----------------

`git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv`
`echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc`
`exec "$SHELL" `
`pyenv install 3.5.2`
`pyenv virtualenv 3.5.2 ENV_NAME`
`pyenv activate ENV_NAME`

install requirements.txt
-----------------

`pip install -r requirements.txt`