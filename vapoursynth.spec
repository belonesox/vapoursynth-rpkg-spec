# vim: syntax=spec

# git_dir_name returns repository name derived from remote Git repository URL
Name:       vapoursynth

# git_dir_version returns version based on commit and tag history of the Git project
Version:    54

# This can be useful later for adding downstream patches
Release:    1%{?dist}
Summary:    Video processing framework with simplicity in mind
License:    LGPLv2
URL:        http://www.vapoursynth.com

Source0:    https://github.com/%{name}/%{name}/archive/R%{version}/%{name}-R%{version}.tar.gz
Patch0:     %{name}-version-info.patch
Patch1:     %{name}-gcc11.patch

BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  nasm
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  pkgconfig(zimg)
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-setuptools

%{?_with_tests:
BuildRequires:  %{name}-devel
BuildRequires:  python3dist(pytest)
}

%{?_with_ImageMagick:
BuildRequires:  pkgconfig(Magick++) >= 7.0
}

%{?_with_subtitles:
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
}

%description
VapourSynth is an application for video manipulation. Or a plugin. Or a library.
Itâ€™s hard to tell because it has a core library written in C++ and a Python
module to allow video scripts to be created.


%package        libs
Summary:        VapourSynth's core library with a C++ API
Obsoletes:      lib%{name} < %{version}-%{release}
Provides:       lib%{name} == %{version}-%{release}

%description    libs
VapourSynth's core library with a C++ API.


%package -n     python3-%{name}
Summary:        Python interface for VapourSynth

%description -n python3-%{name}
Python interface for VapourSynth/VSSCript.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%package        tools
Summary:        Extra tools for VapourSynth

%description    tools
This package contains the vspipe tool for interfacing with VapourSynth.


%package        plugins
Summary:        VapourSynth plugins
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    plugins
VapourSynth plugins.


%prep
%autosetup -p1 -n %{name}-R%{version}


%build
autoreconf -vif
%configure \
    --disable-static \
    --enable-x86-asm \
    --enable-core \
    --enable-vsscript \
    --enable-vspipe \
    --enable-python-module \
    --enable-eedi3 \
    --%{?_with_ImageMagick:enable}%{!?_with_ImageMagick:disable}-imwri \
    --enable-miscfilters \
    --enable-morpho \
    --enable-ocr \
    --enable-removegrain \
    --%{?_with_subtitles:enable}%{!?_with_subtitles:disable}-subtext \
    --enable-vinverse \
    --enable-vivtc \

%make_build


%install
%py3_install
%make_install
find %{buildroot} -type f -name "*.la" -delete

# Let RPM pick up docs in the files section
rm -fr %{buildroot}%{_docdir}/%{name}

%ldconfig_scriptlets libs
%ldconfig_scriptlets -n python3-%{name}


%{?_with_tests:
%check
%{python3} -m pytest -v
}


%files libs
%doc ChangeLog
%license COPYING.LESSER
%dir %{_libdir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}-script.so.*

%files -n python3-%{name}
%{python3_sitearch}/%{name}.so
%{python3_sitearch}/VapourSynth-*.egg-info

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}-script.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-script.pc

%files tools
%{_bindir}/vspipe

%files plugins
%{_libdir}/%{name}/lib*.so
