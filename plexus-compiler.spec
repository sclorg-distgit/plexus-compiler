%global pkg_name plexus-compiler
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global parent  plexus

Name:       %{?scl_prefix}%{pkg_name}
Version:    2.2
Release:    7.9%{?dist}
Epoch:      0
Summary:    Compiler call initiators for Plexus
# extras subpackage has a bit different licensing
# parts of compiler-api are ASL2.0/MIT
License:    MIT and ASL 2.0
URL:        http://plexus.codehaus.org/

Source0:    https://github.com/sonatype/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:    http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:    LICENSE.MIT

BuildArch:      noarch
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix}plexus-classworlds
BuildRequires:  %{?scl_prefix_java_common}ecj
BuildRequires:  %{?scl_prefix}plexus-containers-container-default
BuildRequires:  %{?scl_prefix}plexus-utils
BuildRequires:  %{?scl_prefix}plexus-containers-component-metadata
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix}plexus-pom
BuildRequires:  %{?scl_prefix}maven-gpg-plugin


%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{pkg_name}-extras package.

%package extras
Summary:        Extra compiler support for %{pkg_name}
# ASL 2.0: src/main/java/org/codehaus/plexus/compiler/util/scan/
#          ...codehaus/plexus/compiler/csharp/CSharpCompiler.java
# ASL 1.1/MIT: ...codehaus/plexus/compiler/jikes/JikesCompiler.java
License:        MIT and ASL 2.0 and ASL 1.1

%description extras
Additional support for csharp, eclipse and jikes compilers

%package pom
Summary:        Maven POM files for %{pkg_name}

%description pom
This package provides %{summary}.

%package javadoc
Summary:        Javadoc for %{pkg_name}
License:        MIT and ASL 2.0 and ASL 1.1

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x

cp %{SOURCE1} LICENSE
cp %{SOURCE2} LICENSE.MIT

%pom_disable_module plexus-compiler-aspectj plexus-compilers/pom.xml

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test
%pom_remove_dep :plexus-compiler-test plexus-compilers
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_package ":plexus-compiler{,s}" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE LICENSE.MIT
%files extras -f .mfiles-extras
%files pom -f .mfiles-pom

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.MIT

%changelog
* Thu Jan 15 2015 Michal Srb <msrb@redhat.com> - 2.2-7.9
- Fix directory ownership

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:2.2-7.8
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:2.2-7.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7.4
- Mass rebuild 2014-02-18

* Fri Feb 14 2014 Michael Simacek <msimacek@redhat.com> - 0:2.2-7.3
- SCL-ize BR

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 02.2-7
- Mass rebuild 2013-12-27

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-7
- Remove dependency on plexus-compiler-test
- Add missing BR: maven-gpg-plugin

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-5
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Apr 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-4
- Fix license tag
- Install MIT license file

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-3
- Remove auxiliary aliases

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-2
- Add auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.2-1
- Update to upstream version 2.2
- Add license file (Resolves: #903268)

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-3
- Remove auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-2
- Build with original POM files

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-1
- Update to upstream version 2.1
- Build with xmvn

* Wed Dec 5 2012 Michal Srb <msrb@redhat.com> - 0:1.9.2-3
- Replaced dependency to plexus-container-default with plexus-containers-container-default

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.2-2
- Fix up licensing properly

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-1
- Update to upstream version 1.9.2

* Wed Aug  8 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-3
- Fix FTBFS by adding ignoreOptionalProblems function
- Use new pom_ macros instead of patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-1
- Update to upstream 1.9.1 release

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-1
- Update to upstream 1.8.3 release.
- For some reason junit is strong (not test) dependency.

* Thu Dec  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-3
- Build with maven 3
- Don't install compiler-test module (nothing should use it anyway)
- Fixes accoding to current guidelines
- Install depmaps into extras separately

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-1
- Update to latest version (1.8)
- Create extras subpackage with optional compilers
- Provide maven depmaps
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-2.3
- drop repotag

* Thu Mar 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.2
- Fix bug in spec that prevented unversioned symlink creation

* Thu Mar 08 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.1
- Fix license
- Disable aspectj compiler until we can put that into Fedora
- Remove vendor and distribution tags
- Removed javadoc post and postuns, with dirs being marked %%doc now
- Fix buildroot per Fedora spec

* Fri Jun 02 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-2jpp
- Fix jar naming to previous plexus conventions

* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-1jpp
- First JPackage build
