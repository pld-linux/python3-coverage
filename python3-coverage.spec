# TODO: finish doc and tests (where dependencies available in PLD)
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define 	module	coverage
Summary:	Tool for measuring code coverage of Python programs
Summary(pl.UTF-8):	Narzędzie do szacowania pokrycia kodu programów w Pythonie
Name:		python3-%{module}
Version:	7.10.7
Release:	1
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/coverage/
Source0:	https://files.pythonhosted.org/packages/source/c/coverage/%{module}-%{version}.tar.gz
# Source0-md5:	6dd415363fa3b40d67f5510a684151e4
URL:		http://coverage.readthedocs.org/
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:42.0.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-eventlet >= 0.39
BuildRequires:	python3-flaky >= 3.8.1
BuildRequires:	python3-gevent >= 24.11
BuildRequires:	python3-greenlet >= 3.1
BuildRequires:	python3-hypothesis >= 6.139.2
BuildRequires:	python3-pytest >= 8.4.2
BuildRequires:	python3-pytest-xdist >= 3.8
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-tomli >= 2.2.1
%endif
%endif
%if %{with doc}
BuildRequires:	python3-cogapp >= 3.6
BuildRequires:	python3-doc8 >= 2.0
BuildRequires:	python3-pyenchant >= 3.3.0
BuildRequires:	python3-scriv >= 1.7
BuildRequires:	python3-sphinx_autobuild >= 2025.8.25
BuildRequires:	python3-sphinx_rtd_theme >= 3.0.2
BuildRequires:	python3-sphinx_code_tabs >= 0.5.5
BuildRequires:	python3-sphinx_lint >= 1.0
BuildRequires:	python3-sphinxcontrib-restbuilder >= 0.3
BuildRequires:	python3-sphinxcontrib-spelling >= 8.0.1
BuildRequires:	sphinx-pdg-3 >= 8.2.3
%endif
Requires:	python3-modules >= 1:3.10
Conflicts:	python-coverage < 5.5-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Coverage.py is a tool for measuring code coverage of Python programs.
It monitors your program, noting which parts of the code have been
executed, then analyzes the source to identify code that could have
been executed but was not.

%description -l pl.UTF-8
Coverage.py to narzędzie do szacowania pokrycia kodu programów w
Pythonie. Monitoruje program, zapisując, które części kodu zostały
wykonane, a następnie analizuje kod źródłowy w celu zidentyfikowania
kodu, który mógłby zostać wykonany, ale nie był.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

export PYTHONPATH=$(readlink -f build-3/lib.*)
%if %{with tests}
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTEST_PLUGINS=flaky.flaky_pytest_plugin,xdist.plugin
%{__python3} igor.py zip_mods
%{__python3} igor.py remove_extension
%{__python3} igor.py test_with_core pytrace
%{__python3} igor.py test_with_core ctrace
%{__python3} igor.py test_with_core sysmon
%endif

%if %{with doc}
sphinx-build-3 -b html -aqE doc doc/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt NOTICE.txt README.rst
%attr(755,root,root) %{_bindir}/coverage
%attr(755,root,root) %{_bindir}/coverage3
%attr(755,root,root) %{_bindir}/coverage-%{py3_ver}
%dir %{py3_sitedir}/coverage
%attr(755,root,root) %{py3_sitedir}/coverage/tracer.cpython-*.so
%{py3_sitedir}/coverage/*.py
%{py3_sitedir}/coverage/*.pyi
%{py3_sitedir}/coverage/py.typed
%{py3_sitedir}/coverage/__pycache__
%{py3_sitedir}/coverage/htmlfiles
%{py3_sitedir}/coverage-%{version}-py*.egg-info
