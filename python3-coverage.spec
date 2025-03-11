# TODO: finish doc and tests (where dependencies available in PLD)
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define 	module	coverage
Summary:	Tool for measuring code coverage of Python programs
Summary(pl.UTF-8):	Narzędzie do szacowania pokrycia kodu programów w Pythonie
Name:		python3-%{module}
Version:	7.6.11
Release:	3
License:	Apache v2.0
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/coverage/
Source0:	https://files.pythonhosted.org/packages/source/c/coverage/%{module}-%{version}.tar.gz
# Source0-md5:	ceffbc1c0eeb3001969f6a1c50c4ddbd
URL:		http://coverage.readthedocs.org/
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 1:42.0.2
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	python3-eventlet >= 0.25.1
BuildRequires:	python3-flaky >= 3.7.0
BuildRequires:	python3-greenlet >= 0.4.15
BuildRequires:	python3-hypothesis >= 4.57.1
BuildRequires:	python3-pycontracts >= 1.8.12
BuildRequires:	python3-pytest >= 4.6.11
BuildRequires:	python3-pytest-xdist >= 1.34.0
BuildRequires:	python3-unittest-mixins >= 1.6
%endif
%if %{with doc}
BuildRequires:	python3-doc8 >= 0.8.1
BuildRequires:	python3-pyenchant >= 3.2.0
BuildRequires:	python3-sphinx_autobuild >= 2020.9.1
BuildRequires:	python3-sphinx_rtd_theme >= 0.5.1
BuildRequires:	python3-sphinx_tabs >= 2.0.0
BuildRequires:	python3-sphinxcontrib-restbuilder >= 0.3
BuildRequires:	python3-sphinxcontrib-spelling >= 7.1.0
BuildRequires:	sphinx-pdg-3 >= 3.4.3
%endif
Requires:	python3-modules >= 1:3.9
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

%if %{with tests}
%{__python3} igor.py test_with_tracer py
%{__python3} igor.py test_with_tracer c
%endif

%if %{with doc}
sphinx-build -b html -aqE doc doc/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst CONTRIBUTORS.txt NOTICE.txt README.rst
%attr(755,root,root) %{_bindir}/coverage3
%attr(755,root,root) %{_bindir}/coverage-%{py3_ver}
%dir %{py3_sitedir}/coverage
%attr(755,root,root) %{py3_sitedir}/coverage/tracer.cpython-*.so
%{py3_sitedir}/coverage/*.py
%{py3_sitedir}/coverage/__pycache__
%{py3_sitedir}/coverage/htmlfiles
%{py3_sitedir}/coverage-%{version}-py*.egg-info
