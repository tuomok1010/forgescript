# Forgescript

A lightweight cross-platform build system for C and C++ projects.

Forgescript is implemented in Python and configured with TOML. Its goal is to provide a simple, transparent build workflow without requiring large external build systems.

## Current Features

- TOML-based project configuration
- Debug and Release build profiles
- Command-line configuration overrides
- Recursive source file discovery
- Automatic build directory creation
- Compilation of C and C++ source files
- Executable linking
- Project-relative path handling
- Preserved source tree structure in object directories

## Example Project Structure

```text
hello_world/
├── forge.toml
├── src/
│   └── main.cpp
├── include/
├── build/
└── log/
```

## Example Configuration

```toml
[project]
name = "Hello World"

[compiler]
executable = "clang++"

[source]
source_dirs = ["src"]
include_dirs = ["include"]

[linker]
libs = []
lib_dirs = []

[logging]
enabled = true
log_dir = "log"

[profiles.debug.output]
output_name = "hello_world"
build_dir = "build/debug"
obj_dir = "build/debug/obj"

[profiles.debug.compiler]
flags = [
    "-std=c++20",
    "-g",
    "-Wall",
    "-Wextra"
]

[profiles.debug.linker]
flags = []

[profiles.release.output]
output_name = "hello_world"
build_dir = "build/release"
obj_dir = "build/release/obj"

[profiles.release.compiler]
flags = [
    "-std=c++20",
    "-O3",
    "-DNDEBUG",
    "-Wall",
    "-Wextra"
]

[profiles.release.linker]
flags = []
```

## Usage

### Build (Debug)

```bash
forge build
```

### Build (Release)

```bash
forge build --profile release
```

### Use a Custom Configuration File

```bash
forge build --config my_project.toml
```

### Override Compiler

```bash
forge build --compiler gcc
```

### Override Compiler Flags

```bash
forge build \
    --compiler-flags \
    -O0 \
    -Wall
```

## Configuration Precedence

Forge resolves configuration using the following precedence order:

```text
CLI Overrides
        ↓
Selected Profile
        ↓
forge.toml
        ↓
Built-in Defaults
```

Higher levels override lower levels.

## Path Resolution

All paths are resolved relative to the directory containing the configuration file.

Example:

```toml
[source]
source_dirs = ["src"]
```

If the configuration file is located at:

```text
/home/user/my_project/forge.toml
```

then Forge resolves the source directory as:

```text
/home/user/my_project/src
```

This ensures builds behave consistently regardless of the current working directory.

## Current Status

Forge is currently capable of:

```text
forge.toml
      ↓
Load configuration
      ↓
Apply profile
      ↓
Apply CLI overrides
      ↓
Discover source files
      ↓
Compile source files
      ↓
Link executable
```

The build pipeline has been verified by successfully building and running a C++ Hello World application.

## Planned Features

- Incremental compilation
- Clean command
- Run command
- Improved logging
- Cross-platform compiler support
- Library projects
- Shared libraries
- Static libraries
- Emacs integration
- Build caching

## Philosophy

Forge aims to be:

- Simple
- Transparent
- Scriptable
- Cross-platform
- Easy to understand

The project favors straightforward build logic and readable configuration over complex DSLs and hidden build behavior.

## License

MIT
