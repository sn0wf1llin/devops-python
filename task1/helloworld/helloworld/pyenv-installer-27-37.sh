
FOR_USER="$USER"
if [ $UID -ne 0 ]; then echo "You need root privileges to run this script."; exit 1; fi;

HOME_PATH="/home/$FOR_USER"
PROJECTS_PATH="/home/$FOR_USER/projects"
if [ ! -d $PROJECTS_PATH ]; then 
	mkdir -p $PROJECTS_PATH;
fi;


function install_pyenv() {
	if [ -d $HOME_PATH/.pyenv ]; then rm -rf $HOME_PATH/.pyenv; fi;

	yum install -y gcc bzip2 bzip2-devel openssl openssl-devel readline readline-devel sqlite sqlite-devel libffi-dev
	yum install -y python-pip 
	
	# customize installation folder
	export PYENV_ROOT="$HOME_PATH/.pyenv";
	export PATH="${PYENV_ROOT}/bin:${PATH}";
	eval "$(pyenv init -)";

	if [ ! -f /tmp/pyenv-installer ]; then wget https://raw.github.com/yyuu/pyenv-installer/master/bin/pyenv-installer -P /tmp/ ; fi;

	chmod +x /tmp/pyenv-installer && /tmp/pyenv-installer
	
	cat $HOME_PATH/.bashrc | grep -E '.pyenv|pyenv';
	if [ $? -eq 1 ]; then
		echo "export PATH=\"$HOME_PATH/.pyenv/bin:$PATH\"" >> $HOME_PATH/.bashrc;
		echo "eval \"\$(pyenv init -)\""  >> $HOME_PATH/.bashrc;
		echo "eval \"\$(pyenv virtualenv-init -)\""  >> $HOME_PATH/.bashrc;
		source $HOME_PATH/.bashrc;
	fi;
	
	chown -R $FOR_USER: $PYENV_ROOT;
}

function install_python37() {
	pyenv install 3.7.2;
	if [ "$?" -eq "1" ]; then echo "pyenv 3.7.2 error"; exit 1; fi;

	pyenv global 3.7.2;

	pip install -U pip
	pip install virtualenv
	easy_install virtualenv

}

function install_python27() {
	pyenv install 2.7.5;
	if [ $? -eq 1 ]; then echo "pyenv 2.7.5 error"; exit 1; fi;

	pyenv global 2.7.5;

	pip install -U pip
	pip install virtualenv
	easy_install virtualenv
}

install_pyenv
install_python27
install_python37

if [ $(ls -la $HOME_PATH/.pyenv/versions/ | grep -E '2.7.5|3.7.2' | wc -l) -ne 2 ]; then echo "troubles with $HOME_PATH/.pyenv/versions installed: "; ls -la $HOME_PATH/.pyenv/versions/; exit 1; else echo "$HOME_PATH/.pyenv/versions : [ OK ]"; fi;

mkdir -p $PROJECTS_PATH/test2/venv && echo “Virtualenv directory” > $PROJECTS_PATH/test2/venv/README;
mkdir -p $PROJECTS_PATH/test3/venv && echo “Virtualenv directory” > $PROJECTS_PATH/test3/venv/README;

pyenv global 2.7.5 && virtualenv --prompt="(test2py27)" $PROJECTS_PATH/test2/venv/python2.7;
pyenv global 3.7.2 && virtualenv --prompt="(test3py37)" $PROJECTS_PATH/test3/venv/python3.7;


