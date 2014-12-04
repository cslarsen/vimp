check:
	find . -name '*.py' -print0 | parallel -0 pyflakes

clean:
	find . -name '*.pyc' | xargs rm -f &
	find . -name '*.pyo' | xargs rm -f &
	rm -rf build dist test MANIFEST vimp.egg-info/
