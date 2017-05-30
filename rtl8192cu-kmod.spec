%global RepoName rtl8192cu-fixes

%global buildforkernels akmod
%global debug_package %{nil}

Name:		    rtl8192cu-kmod
Version:	    v4.0.2
Release:	    1%{?dist}
Summary:	    This is a repackaging of Realtek's own 8192CU USB WiFi driver

Group:		    System Environment/Kernel
License:	    GPLv2
URL:		    https://github.com/pvaret/%{RepoName}
Source0:	    https://github.com/pvaret/%{RepoName}/archive/master.tar.gz
Source11:       rtl8192cu-kmod-kmodtool-excludekernel-filterfile

%global AkmodsBuildRequires %{_bindir}/kmodtool
#, elfutils-libelf-devel
BuildRequires:  %{AkmodsBuildRequires}

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name rtl8192cu-newest --obsolete-version "%{?epoch}:%{version}" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This is a repackaging of Realtek's own 8192CU USB WiFi driver.
Compatibility
These devices are known to work with this driver:
* ASUSTek USB-N13 rev. B1 (0b05:17ab)
* Belkin N300 (050d:2103)
* D-Link DWA-121 802.11n Wireless N 150 Pico Adapter [RTL8188CUS]
* Edimax EW-7811Un (7392:7811)
* Kootek KT-RPWF (0bda:8176)
* TP-Link TL-WN821Nv4 (0bda:8178)
* TP-Link TL-WN822N (0bda:8178)
* TP-Link TL-WN823N (only models that use the rtl8192cu chip)
* TRENDnet TEW-648UBM N150
These devices are known not to be supported:
* Alfa AWUS036NHR
* TP-Link WN8200ND
As a rule of thumb, this driver generally works with devices that use the RTL8192CU chipset, and some devices that use the RTL8188CUS, RTL8188CE-VAU and RTL8188RU chipsets too, though it's more hit and miss.
Devices that use dual antennas are known not to work well. This appears to be an issue in the upstream Realtek driver.

%prep
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
tar xzf %{SOURCE0}
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/%{RepoName}-master
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/%{RepoName}-master
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 30 2017 Alexei Panov <me AT elemc DOT name> v4.0.2-1
-  Initial build

