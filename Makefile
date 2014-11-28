check:
	find . -name '*.py' -exec pyflakes {} \;

clean:
	find . -name '*.pyc' | xargs rm -f
	find . -name '*.pyo' | xargs rm -f
	rm -rf build dist test MANIFEST vimp.egg-info/
