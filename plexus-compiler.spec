%{?scl:%scl_package plexus-compiler}
%{!?scl:%global pkg_name %{name}}

%bcond_without eclipse

Name:       %{?scl_prefix}plexus-compiler
Epoch:      0
Version:    2.8.1
Release:    4.1%{?dist}
Summary:    Compiler call initiators for Plexus
# extras subpackage has a bit different licensing
# parts of compiler-api are ASL2.0/MIT
License:    MIT and ASL 2.0
URL:        https://github.com/codehaus-plexus/plexus-compiler
BuildArch:  noarch

Source0:    https://github.com/codehaus-plexus/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz
Source1:    http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:    LICENSE.MIT

# https://github.com/codehaus-plexus/plexus-compiler/pull/25
Patch0:     0001-Copy-input-map-in-setCustomCompilerArguments-AsMap.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
%if %{with eclipse}
BuildRequires:  mvn(org.eclipse.tycho:org.eclipse.jdt.core)
%endif

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

%patch0 -p1

cp %{SOURCE1} LICENSE
cp %{SOURCE2} LICENSE.MIT

%pom_disable_module plexus-compiler-aspectj plexus-compilers
# missing com.google.errorprone:error_prone_core
%pom_disable_module plexus-compiler-javac-errorprone plexus-compilers

%if %{without eclipse}
%pom_disable_module plexus-compiler-eclipse plexus-compilers
%endif

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test

# don't install sources jars
%mvn_package ":*::sources:" __noinstall

%mvn_package ":plexus-compiler{,s}" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras

# don't generate requires on test dependency (see #1007498)
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='plexus-compiler-test']]" plexus-compilers

%pom_remove_plugin :maven-site-plugin

%build
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%doc LICENSE LICENSE.MIT

%files extras -f .mfiles-extras

%files pom -f .mfiles-pom

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.MIT

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 0:2.8.1-4.1
- Automated package import and SCL-ization

* Thu May 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.8.1-4
- Add eclipse build-conditional

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 02 2016 Michael Simacek <msimacek@redhat.com> - 0:2.8.1-2
- Add patch to fix tycho compatibility

* Mon Oct 31 2016 Michael Simacek <msimacek@redhat.com> - 0:2.8.1-1
- Update to upstream version 2.8.1

* Fri Jul  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-3
- Remove unneeded build-requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-1
- Update to upstream version 2.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-2
- Update upstream URL

* Mon Oct 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Update to upstream version 2.4

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-6
- Fix build-requires on POM packages

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-4
- Rebuild to regenerate Maven auto-requires

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.3-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-2
- Fix unowned directory
- Regenerate build-requires

* Fri Sep 13 2013 Michal Srb <msrb@redhat.com> - 0:2.3-1
- Update to upstream version 2.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
