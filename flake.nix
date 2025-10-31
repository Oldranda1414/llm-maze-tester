{
  description = "Dev environment for maze solver project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs = { self , nixpkgs ,... }: let
    system = "x86_64-linux";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs {
        inherit system;
      };
    in pkgs.mkShell {
      packages = with pkgs; [
        # modern command runner
        just
        # modern python package manager
        uv
        # local llm server
        ollama
      ];

      shellHook = ''
        echo "Run 'just' to see available commands."
      '';
    };
  };
}
