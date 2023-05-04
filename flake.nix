{
  # inputs.nixpkgs.url = "nixpkgs/nixos-22.11";
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    inherit (pkgs) lib;
  in {
    apps.${system} = let
      app = program: {
        type = "app";
        inherit program;
      };
    in {
      default = self.apps.${system}.dev;
      dev = app "${self.packages.${system}.worblehat}/bin/dev";
      scanner = app "${self.packages.${system}.worblehat}/bin/scanner";
    };

    packages.${system} = {
      default = self.packages.${system}.worblehat;
      worblehat = with pkgs.python3Packages; buildPythonPackage {
        pname = "worblehat";
        version = "0.1.0";
        src = ./.;

        format = "pyproject";

        buildInputs = [ poetry-core ];
        propagatedBuildInputs = [
          alembic
          click
          flask
          flask-admin
          flask-sqlalchemy
          isbnlib
          python-dotenv
          sqlalchemy
        ];
      };
    };
  };
}