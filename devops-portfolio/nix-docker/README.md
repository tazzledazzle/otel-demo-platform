# Nix and Docker at Scale

This directory demonstrates Nix and Docker for reproducible builds and managing image/package sets.

## Nix

- **`flake.nix`**: Defines a dev shell (Go, Node, Bazel, Nix, Docker) and packages (`hello-portfolio`, `hello-portfolio-verbose`). Multiple package variants illustrate many derivations and Nix store caching.
- **Usage**: From repo root, run `nix develop nix-docker#default` (or `cd nix-docker && nix develop`) to enter the dev shell. Build packages with `nix build nix-docker#hello-portfolio` etc.

## Docker

- **Multi-stage Dockerfiles** in this repo build the CLI and remote-exec server with a build stage and minimal runtime image.
- **Optional Nix-built image**: See `nix-docker/docker-nix.nix` for building a Docker image from Nix via `dockerTools`.
- **Large set**: `scripts/build-images.sh` builds multiple images (CLI, remote-exec) and documents tagging and layer reuse.

## When to use Nix vs Docker

- **Nix**: Reproducible dev environments and hermetic builds; great for caching many store paths in CI and sharing via binary cache.
- **Docker**: Runtime isolation, deployment artifacts, and ecosystem (registries, K8s). Use multi-stage builds to keep images small and layer reuse for many variants.

## Scaling

For large image/package sets: use a Nix binary cache (e.g. Cachix or S3), tag Docker images by content hash or version, and in CI cache Nix store paths and Docker layers to avoid redundant work.
