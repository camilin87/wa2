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

MODULES = engine
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
	gitstats ./ ./gitstats > /dev/null

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

install-dev-dependencies:
	sudo pip install nose
	sudo pip install mock
	sudo pip install freezegun
	sudo pip install coverage
	sudo pip install pylint
	sudo pip install pep8

install-dev-dependencies-mac:
	sudo easy_install pip
	make install-dev-dependencies

clean:
	make -i clean-pyc
	- rm -R -v ./cover
	- rm -R -v ./gitstats
	- rm -R -v ./pylint-report
	- rm -R -v ./pep8-report

clean-pyc:
	rm -R */*.pyc && rm -R *.pyc
