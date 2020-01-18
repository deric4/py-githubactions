from setuptools import setup, find_packages

setup(
    name="githubactions",
    author="deric4",
    url="https://github.com/deric4/githubactions",
    packages=find_packages(where="src", exclude=['tests']),
    package_dir={"": "src"},
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    python_requires='>=3.7',
)
