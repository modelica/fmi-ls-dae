"""Merge per-platform FMUs into a single multi-platform FMU.

Each per-platform build produces an FMU containing only the binary for that
platform.  This script extracts and merges the binaries/ directories from all
platform FMUs into one combined FMU that contains all platforms.

Usage:
    python merge_fmus.py

Expected directory layout (created by the GitHub Actions workflow):
    dist-x86_64-linux/SimpleDAE.fmu
    dist-aarch64-linux/SimpleDAE.fmu
    dist-x86_64-windows/SimpleDAE.fmu
    dist-aarch64-windows/SimpleDAE.fmu
    dist-x86_64-darwin/SimpleDAE.fmu
    dist-aarch64-darwin/SimpleDAE.fmu

Output:
    dist-merged/SimpleDAE.fmu
"""

import os
import zipfile

FMU_NAMES = ["SimpleDAE"]

PLATFORMS = [
    "x86_64-linux",
    "aarch64-linux",
    "x86_64-windows",
    "aarch64-windows",
    "x86_64-darwin",
    "aarch64-darwin",
]

os.makedirs("dist-merged", exist_ok=True)

for fmu_name in FMU_NAMES:
    filename = f"{fmu_name}.fmu"
    staging = f"dist-merged/{fmu_name}"
    os.makedirs(staging, exist_ok=True)

    base_platform = PLATFORMS[0]
    base_fmu = f"dist-{base_platform}/{filename}"

    # Extract the full FMU structure from the first (base) platform
    with zipfile.ZipFile(base_fmu, "r") as zf:
        zf.extractall(staging)

    # Add binaries/ from remaining platforms
    for platform in PLATFORMS[1:]:
        platform_fmu = f"dist-{platform}/{filename}"
        if not os.path.exists(platform_fmu):
            print(f"Warning: {platform_fmu} not found, skipping.")
            continue
        with zipfile.ZipFile(platform_fmu, "r") as zf:
            for name in zf.namelist():
                if name.startswith("binaries/"):
                    zf.extract(name, staging)

    # Repack as FMU
    out_path = f"dist-merged/{filename}"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as merged:
        for root, _dirs, files in os.walk(staging):
            for file in files:
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, staging)
                merged.write(full, arcname)

    print(f"Created {out_path}")
