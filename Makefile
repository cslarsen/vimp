lint:
	find . -name '*.py' -print0 | parallel -0 pyflakes

check:
	python setup.py test

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*.pyo' | xargs rm -f
	rm -rf build dist test MANIFEST vimp.egg-info/

publish-test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

publish:
	python setup.py register -r pypi
	python setup.py sdist upload --sign -r pypi
