with import <nixpkgs> {};

mkShell {
  nativeBuildInputs = [
    python3
  ];

  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
    stdenv.cc.cc
  ];

  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";

  shellHook = ''
    export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH

    VENV_DIR=".venv"

    if [ ! -d "$VENV_DIR" ]; then
      echo "Creating virtual environment..."
      python3 -m venv $VENV_DIR
    fi

    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
  '';
}
