# coding=utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages, Command
import os
import shutil
import glob
import sys

# Hack to prevent stupid "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when running `python setup.py test`
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
for m in ('multiprocessing', 'billiard'):
	try:
		__import__(m)
	except ImportError:
		pass

#~~ configure versioneer

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'src/octoprint/_version.py'
versioneer.versionfile_build = 'octoprint/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = ''

#~~ configure paths

BASE_DIR = os.path.dirname(__file__)
MANIFEST_FILE = os.path.join(BASE_DIR, "MANIFEST")

BUILD_DIR = os.path.join(BASE_DIR, "build")
DIST_DIR = os.path.join(BASE_DIR, "dist")

DOCS_DIR = os.path.join(BASE_DIR, "docs")
DOCS_BUILD_DIR = os.path.join(DOCS_DIR, "_build")

#~~ helpers


def package_data_dirs(source, sub_folders):
	"""
	Returns a list of all files and directories within the given sub folders within the given source folder.

	:param source: the source folder from which to crawl the given sub folders
	:param sub_folders: a list of sub folders relative to source which to crawl
	:return: a list of all files and directories contained within the given sub folders within the source folder
	"""

	dirs = []

	for d in sub_folders:
		for dirname, _, files in os.walk(os.path.join(source, d)):
			dirname = os.path.relpath(dirname, source)
			for f in files:
				dirs.append(os.path.join(dirname, f))

	return dirs


class CleanCommand(Command):
	"""
	A setuptools command to clean OctoPrint's build artifacts. Currently removes the build folder and any folders
	matching *.egg*.
	"""

	description = "clean build artifacts"
	user_options = []
	boolean_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		if os.path.exists(BUILD_DIR):
			print "Deleting build directory"
			shutil.rmtree(BUILD_DIR)
		if os.path.exists(DIST_DIR):
			print "Deleting dist directory"
			shutil.rmtree(DIST_DIR)
		if os.path.exists(DOCS_BUILD_DIR):
			print "Deleting docs build directory"
			shutil.rmtree(DOCS_BUILD_DIR, ignore_errors=True)
		if os.path.exists(MANIFEST_FILE):
			print "Deleting generated MANIFEST"
			os.remove(MANIFEST_FILE)

		eggs = glob.glob(os.path.join(BASE_DIR, '*.egg*'))
		for egg in eggs:
			if os.path.isfile(egg):
				print "Deleting file %s" % egg
				os.remove(egg)
			elif os.path.isdir(egg):
				print "Deleting directory %s" % egg
				shutil.rmtree(egg, ignore_errors=True)


class DocsCommand(Command):
	"""
	A setuptools command to build OctoPrint's documentation via sphinx.
	"""

	description = "build documentation"
	user_options = []
	boolean_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		import sphinx
		sphinx.main(['-b html', DOCS_DIR, os.path.join(DOCS_BUILD_DIR, 'html')])


def get_cmdclass():
	"""
	:return: the command classes to use for this setup script
	"""
	cmdclass = versioneer.get_cmdclass()
	cmdclass.update({
		"clean": CleanCommand,
		"docs": DocsCommand
	})
	return cmdclass


#~~ Configure setup method


def requirements():
	print sys.argv
	extras = extra_requirements()
	docs = extras["docs"]
	test = extras["test"]

	r = [
		"flask==0.9",
		"werkzeug==0.8.3",
		"tornado==3.0.2",
		"sockjs-tornado>=1.0.0",
		"PyYAML==3.10",
		"Flask-Login==0.2.2",
		"Flask-Principal==0.3.5",
		"pyserial>=2.6",
		"netaddr>=0.7.10",
		"watchdog",
		"sarge",
	]

	if "docs" in sys.argv or "develop" in sys.argv:
		r = r + docs
	if "test" in sys.argv or "develop" in sys.argv:
		r = r + test

	return r


def extra_requirements():
	return {
		"docs": [
			"sphinx",
			"sphinxcontrib-httpdomain",
			"sphinx_rtd_theme"
		],
		"test": test_requirements()
	}


def test_requirements():
	return [
		"mock>=1.0.1",
		"nose>=1.3.0"
	]


def params():
	name = "OctoPrint"
	version = versioneer.get_version()
	cmdclass = get_cmdclass()

	description = "A responsive web interface for 3D printers"
	long_description = open("README.md").read()
	classifiers = [
		"Development Status :: 4 - Beta",
		"Environment :: Web Environment",
		"Framework :: Flask",
		"Intended Audience :: Education",
		"Intended Audience :: End Users/Desktop",
		"Intended Audience :: Manufacturing",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: JavaScript",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Internet :: WWW/HTTP :: WSGI",
		"Topic :: Printing",
		"Topic :: System :: Networking :: Monitoring"
	]
	author = "Gina Häußge"
	author_email = "osd@foosel.net"
	url = "http://octoprint.org"
	license = "AGPLv3"

	packages = find_packages(where="src")
	package_dir = {"octoprint": "src/octoprint"}
	package_data = {"octoprint": package_data_dirs('src/octoprint', ['static', 'templates'])}

	include_package_data = True
	zip_safe = False

	install_requires = requirements()
	extras_require = extra_requirements()

	test_suite = 'nose.collector'
	tests_require = test_requirements()

	entry_points = {
		"console_scripts": [
			"octoprint = octoprint:main"
		]
	}

	#scripts = {
	#	"scripts/octoprint.init": "/etc/init.d/octoprint"
	#}

	return locals()

setup(**params())
