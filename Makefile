all:
	make clean
	make all-tests
	make reports

all-tests:
	make tests
	make integration

tests:
	make -i clean-pyc
	nosetests -s -a '!integration'

integration:
	make -i clean-pyc
	nosetests -s -a 'integration'

reports:
	make report-coverage
	make report-pylint
	make report-pep8
	make report-gitstats
	make report-lines-of-code

MODULES = engine bo
report-pylint:
	- mkdir pylint-report
	- $(foreach imod,$(MODULES),pylint $(imod) > pylint-report/$(imod).html;)
	ls -1 pylint-report/*.html | xargs -n1 basename > pylint-report/index_0.txt
	awk '{print "<a href="$$0">"$$0"</a></br>";}' pylint-report/index_0.txt > pylint-report/index_contents.txt
	echo "<html><body>" > pylint-report/index.html
	cat pylint-report/index_contents.txt >> pylint-report/index.html
	echo "</body></html>" >> pylint-report/index.html
	rm pylint-report/index_*.txt

report-coverage:
	make -i clean-pyc
	nosetests -s --with-coverage --cover-html --cover-erase

report-gitstats:
	make switch-to-git-stats-python-version
	gitstats ./ ./gitstats > /dev/null
	make switch-to-dev-python-version

report-pep8:
	- mkdir pep8-report
	- pep8 --max-line-length=100 */*.py > ./pep8-report/report.txt

report-lines-of-code:
	make report-lines-of-test-code
	make report-lines-of-production-code

report-lines-of-test-code:
	find . -type f -iname '*.py' -path '*/test/*' | xargs wc -l | tail -1

report-lines-of-production-code:
	find . -type f -iname '*.py' ! -path '*/test/*' | xargs wc -l | tail -1

configure-pyenv:
	echo 'eval "$$(pyenv init -)"' >> ~/.bash_profile
	sed '$$!N; /^\(.*\)\n\1$$/!P; D' ~/.bash_profile > ~/.temp_profile
	cat ~/.temp_profile > ~/.bash_profile
	eval "$$(pyenv init -)"

PYTHON_VERSION = 3.4.0
PYTHON_VERSION_GIT_STATS = 2.7.6
configure-python-version:
	yes N | pyenv install $(PYTHON_VERSION)
	yes N | pyenv install $(PYTHON_VERSION_GIT_STATS)
	make refresh-packages

refresh-packages:
	pyenv rehash

switch-to-dev-python-version:
	pyenv local $(PYTHON_VERSION)

switch-to-git-stats-python-version:
	pyenv local $(PYTHON_VERSION_GIT_STATS)

install-dev-dependencies:
	make -i configure-python-version
	make switch-to-dev-python-version

	sudo pip install nose
	sudo pip install mock
	sudo pip install freezegun
	sudo pip install coverage
	sudo pip install pylint
	sudo pip install pep8
	sudo pip install python-forecastio

	make refresh-packages

install-dev-dependencies-mac:
	brew install pyenv
	make install-dev-dependencies

clean:
	make -i clean-pyc
	- rm -R -v ./cover
	- rm -R -v ./gitstats
	- rm -R -v ./pylint-report
	- rm -R -v ./pep8-report

clean-pyc:
	rm -R */*.pyc && rm -R *.pyc
