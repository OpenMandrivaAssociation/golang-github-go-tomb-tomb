%global goipath         github.com/go-tomb/tomb
%global commit          d5d1b5820637886def9eef33e03a27a9f166942c

%global import_path     gopkg.in/v2/tomb
%global import_path_sec gopkg.in/tomb.v2

%global v1_commit          dd632973f1e7218eb1089048e0798ec9ae7dceb8
%global v1_shortcommit     %(c=%{v1_commit}; echo ${c:0:7})
%global v1_import_path     gopkg.in/v1/tomb
%global v1_import_path_sec gopkg.in/tomb.v1

%global devel_main      golang-gopkg-tomb-devel-v2

%gometa

Name:           golang-github-go-tomb-tomb
Version:        0
Release:        15%{?dist}
Summary:        The tomb package helps with clean goroutine termination in the Go language
License:        BSD
URL:            %{gourl}
Source0:        %{gosource}
Source1:        https://%{goipath}/archive/%{v1_commit}/tomb-%{v1_commit}.tar.gz

%description
%{summary}.

%package devel
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

BuildRequires:  golang(gopkg.in/check.v1)
Requires:       golang(gopkg.in/check.v1)

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{v1_import_path} prefix.

%package devel-v2
Summary:        Enables Go programs to comfortably encode and decode YAML values
BuildArch:      noarch

%description devel-v2
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%setup -q -n tomb-%{v1_commit} -T -b 1
%forgesetup

%install
%goinstall
%goinstall -i %{import_path} -o devel.file-list
%goinstall -i %{import_path_sec} -o devel.file-list

cw=$(pwd)
pushd ../tomb-%{v1_commit}
%goinstall -i %{v1_import_path} -o ${cw}/v1_devel.file-list
%goinstall -i %{v1_import_path_sec} -o ${cw}/v1_devel.file-list

# TODO(jchaloup): create rpm macros for this!!!
#github.com/go-tomb/tomb -> gopkg.in/v2/tomb
pushd %{buildroot}/%{gopath}/src/%{import_path}/
sed -i 's/"github\.com\/go-tomb\/tomb/"gopkg\.in\/v2\/tomb/g' \
        $(find . -name '*.go')
#'github.com/go-tomb/tomb -> gopkg.in/tomb.v2
cd %{buildroot}/%{gopath}/src/%{import_path_sec}/
sed -i 's/"github\.com\/go-tomb\/tomb/"gopkg\.in\/tomb\.v2/g' \
        $(find . -name '*.go')
#gopkg.in/v1/tomb -> gopkg.in/tomb.v1
cd %{buildroot}/%{gopath}/src/%{v1_import_path_sec}/
sed -i 's/"gopkg\.in\/v1\/tomb/"gopkg\.in\/tomb\.v1/g' \
        $(find . -name '*.go')
popd

%check
%gochecks
pushd %{buildroot}/%{gopath}/src/%{import_path}/
%gochecks -i %{import_path}
cd %{buildroot}/%{gopath}/src/%{import_path_sec}/
%gochecks
popd

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files devel -f v1_devel.file-list
%license LICENSE
%doc README.md

%files devel-v2 -f devel.file-list
%license LICENSE
%doc README.md

%changelog
* Wed Oct 31 2018 Robert-André Mauchin <zebob.m@gmail.com> - 0.14.20181031gitd5d1b58
- Update to new Go packaging
- Bump to commit dd632973f1e7218eb1089048e0798ec9ae7dceb8 and d5d1b5820637886def9eef33e03a27a9f166942c

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.13.gitd5d1b58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.12.gitd5d1b58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.11.gitd5d1b58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.10.gitd5d1b58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Jan Chaloupka <jchaloup@redhat.com> - 0-0.9.gitd5d1b58
- Bump to upstream d5d1b5820637886def9eef33e03a27a9f166942c
  related: #1249041
  resolves: #1435616

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.8.git14b3d72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.7.git14b3d72
- https://fedoraproject.org/wiki/Changes/golang1.7

* Fri Apr 15 2016 jchaloup <jchaloup@redhat.com> - 0-0.6.git14b3d72
- Extend with gopkg.in/tomb.v1
  related: #1249041

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.git14b3d72
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.4.git14b3d72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Sep 12 2015 jchaloup <jchaloup@redhat.com> - 0-0.3.git14b3d72
- Update to spec-2.1
  related: #1249041

* Fri Jul 31 2015 jchaloup <jchaloup@redhat.com> - 0-0.2.git14b3d72
- Update spec file to spec-2.0
  resolves: #1249041

* Mon Jun 15 2015 Marek Skalický <mskalick@redhat.com> - 0-0.1.git14b3d72
- First package for Fedora
  resolves: #1232221
