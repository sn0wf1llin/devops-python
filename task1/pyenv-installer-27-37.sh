yum install -y gcc bzip2 bzip2-devel openssl openssl-devel readline readline-devel sqlite sqlite-devel
yum install -y python-pip

curl -L  https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

pyenv install 3.7.2 || echo "pyenv 3.7.2 error"
pyenv install 2.7.5 || echo "pyenv 2.7.5 error"

pip install -U pip

pip install virtualenv
easy_install virtualenv

PROJECTS_PATH="/home/$USER/projects"
if [ ! -d $PROJECTS_PATH ]; then 
	mkdir -p $PROJECTS_PATH;
fi;

if [ `ls -la ~/.pyenv/versions/ | grep -E '2.7.5|3.7.2' | wc -l` -ne 2 ]; then echo "troubles with ./pyenv/versions installed: `ls -la ~/.pyenv/versions/`"; exit 1; else echo "./pyenv/versions : [ OK ]" fi;


mkdir -p $PROJECTS_PATH/test2/venv && echo “Virtualenv directory” > $PROJECTS_PATH/test2/venv/README;
mkdir -p $PROJECTS_PATH/test3/venv && echo “Virtualenv directory” > $PROJECTS_PATH/test3/venv/README;

pyenv global 2.7.5 && virtualenv --prompt="(test2py27)" $PROJECTS_PATH/test2/venv/python2.7
pyenv global 3.7.2 && virtualenv --prompt="(test3py37)" $PROJECTS_PATH/test3/venv/python3.7


