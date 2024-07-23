{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    nixpkgs_master.url = "github:NixOS/nixpkgs/master";
    systems.url = "github:nix-systems/default";
    flake-utils.url = "github:numtide/flake-utils";
    flake-utils.inputs.systems.follows = "systems";
  };

  outputs = { self, nixpkgs, flake-utils, systems, ... } @ inputs:
      flake-utils.lib.eachDefaultSystem (system:
        let
            pkgs = import nixpkgs {
              system = system;
              config.allowUnfree = true;
            };
          in
          with pkgs;
        rec {
          packages = import ./nix {inherit pkgs;};
          apps = {
            cellprofiler = {
              type = "app";
              program = "${packages.cellprofiler}/bin/cellprofiler";
            };
          };
          devShells = {
              default = let 
                python_with_pkgs = (pkgs.python3.withPackages(pp: [
                  packages.cellprofiler
                  packages.cellprofiler-core
                  packages.cellprofiler-library
                ]));
              in mkShell {
                    NIX_LD = runCommand "ld.so" {} ''
                        ln -s "$(cat '${pkgs.stdenv.cc}/nix-support/dynamic-linker')" $out
                      '';
                    NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
                      # Add needed packages here
                      stdenv.cc.cc
                      libGL
                      zlib
                      libxcrypt-legacy
                      libmysqlclient
                      mariadb
                      glib
                    ];
                    packages = [
                      python_with_pkgs
                      python3Packages.venvShellHook
                      git
                      gtk3
                      glib
                      pkg-config
                      rye
                      jdk
                      maven
                      libmysqlclient
                      mariadb
                      duckdb
                    ];
                    venvDir = "./.venv";
                    postVenvCreation = ''
                        unset SOURCE_DATE_EPOCH
                      '';
                    postShellHook = ''
                        unset SOURCE_DATE_EPOCH
                      '';
                    shellHook = ''
                        export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
                        runHook venvShellHook
                        export PYTHONPATH=${python_with_pkgs}/${python_with_pkgs.sitePackages}:$PYTHONPATH
                    '';
                  };
              };
        }
      );
}
