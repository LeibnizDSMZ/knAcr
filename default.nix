with import <nixpkgs> { };

pkgs.mkShell {
  name = "config-shell";
  nativeBuildInputs = with pkgs; [
    git
    # python
    python313
    virtualenv
    # python build requirements
    pyenv
    gcc
    gnumake
    zlib
    libffi
    readline
    bzip2
    openssl
    ncurses
    # format
    nixfmt-rfc-style
  ];

  shellHook = ''
    export PATH=$HOME/.local/bin/:$PWD/.venv/bin/:$PATH
    export PYTHONPATH=$PWD/.venv/:$PYTHONPATH
    export RUFF=${pkgs.ruff}/bin/ruff

    export SOURCE_DATE_EPOCH=$(date +%s)
    export PYENV_ROOT="$HOME/.pyenv";
    export RUFF=${pkgs.ruff}/bin/ruff

    # pyenv flags to be able to install Python
    export CPPFLAGS="-I${pkgs.zlib.dev}/include -I${pkgs.libffi.dev}/include -I${pkgs.readline.dev}/include -I${pkgs.bzip2.dev}/include -I${pkgs.openssl.dev}/include";
    export CXXFLAGS="-I${pkgs.zlib.dev}/include -I${pkgs.libffi.dev}/include -I${pkgs.readline.dev}/include -I${pkgs.bzip2.dev}/include -I${pkgs.openssl.dev}/include";
    export CFLAGS="-I${pkgs.openssl.dev}/include";
    export LDFLAGS="-L${pkgs.zlib.out}/lib -L${pkgs.libffi.out}/lib -L${pkgs.readline.out}/lib -L${pkgs.bzip2.out}/lib -L${pkgs.openssl.out}/lib";
    export CONFIGURE_OPTS="-with-openssl=${pkgs.openssl.dev}";
    export PYENV_VIRTUALENV_DISABLE_PROMPT="1";
  '';
}
