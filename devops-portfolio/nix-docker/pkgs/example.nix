# Example custom derivation: builds a small artifact to show how we compose
# nixpkgs and scale to many inputs. In CI, cache store paths for fast rebuilds.
{ pkgs }:
pkgs.writeShellScriptBin "portfolio-pkg-demo" ''
  echo "Built from nix-docker/pkgs/example.nix"
  echo "Nix hashes all inputs; changing this file changes the store path."
''