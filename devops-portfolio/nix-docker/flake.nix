{
  description = "DevOps portfolio: Nix dev shell and packages (Go, Node, Bazel)";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgsFor = system: import nixpkgs { inherit system; };
    in
    {
      devShells = forAllSystems (system:
        let pkgs = pkgsFor system; in
        {
          default = pkgs.mkShell {
            name = "devops-portfolio";
            buildInputs = with pkgs; [
              go_1_22
              nodejs_22
              bazel_7
              nix
              docker
              git
              gnumake
            ];
            shellHook = ''
              echo "DevOps portfolio dev shell: go, node, bazel, nix, docker"
            '';
          };
        });

      packages = forAllSystems (system:
        let
          pkgs = pkgsFor system;
          examplePkg = import ./pkgs/example.nix { inherit pkgs; };
        in
        {
          hello-portfolio = pkgs.writeShellScriptBin "hello-portfolio" ''
            echo "DevOps portfolio suite - Nix-built artifact"
          '';
          hello-portfolio-verbose = pkgs.writeShellScriptBin "hello-portfolio-verbose" ''
            echo "DevOps portfolio suite (verbose)"
            echo "Built with Nix for reproducible artifacts"
          '';
          portfolio-pkg-demo = examplePkg;
          default = self.packages.${system}.hello-portfolio;
        });
    };
}
