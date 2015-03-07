lint:
	find . -name '*.py' -print0 | parallel -0 pyflakes

check:
	python setup.py test

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*.pyo' | xargs rm -f
	rm -rf build dist test MANIFEST vimp.egg-info/

publish:
	python setup.py bdist_wheel
	gpg --detach-sign -a dist/vimp*.whl
	twine upload dist/vimp*
