#!/usr/bin/env python3
"""Lay out the print edition of A Young Delegate's Notebook in InDesign.

Rebuilds the manuscript with build.py, then runs indesign/layout.jsx in
InDesign 2026 through its Windows scripting interface. Run from the book root,
with InDesign closed:

    python indesign.py

The run starts InDesign and quits it afterward, unless documents are open.
A layout run in a session that's already in use can crash it and lose unsaved
work, so the run stops if InDesign is already open. Pass --reuse to run in
that session anyway.

This writes three files into indesign/: young-delegates-notebook.indd,
young-delegates-notebook-print.pdf for the printer (no live links, but link
text is blue), and young-delegates-notebook.pdf for screens (live links in
blue, plus bookmarks). Each run
starts from a blank document and overwrites them. Pass --out DIR to write
them somewhere else.
"""
from __future__ import annotations

import argparse
import base64
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import build

LAYOUT = build.INDESIGN / "layout.jsx"

# The layout's settings go in as DoScript arguments rather than pasted into
# the code, so no path ever needs escaping. Script args are how one InDesign
# script hands values to another, and the "headless" one turns off the alert
# the layout shows when it's run from the Scripts panel. 1852776480 is
# SaveOptions.NO, and the wait keeps the next run from finding InDesign still
# open.
POWERSHELL = r"""
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$running = [bool](Get-Process InDesign -ErrorAction SilentlyContinue)
if ($running -and -not $env:YDN_REUSE) { exit 2 }
try {
    $app = New-Object -ComObject InDesign.Application.2026
    $code = "app.scriptArgs.clear();" +
        "app.scriptArgs.setValue('src', arguments[0]);" +
        "app.scriptArgs.setValue('out', arguments[1]);" +
        "app.scriptArgs.setValue('log', arguments[3]);" +
        "app.scriptArgs.setValue('headless', '1');" +
        "`$.evalFile(new File(arguments[2]));"
    $result = $app.DoScript($code, 1246973031, [object[]]@($env:YDN_SRC, $env:YDN_OUT, $env:YDN_LAYOUT, $env:YDN_LOG))
    [Console]::Out.WriteLine($result)
    if ($running) {
        [Console]::Out.WriteLine("note: InDesign was already running, so it was left running")
    } elseif ($app.Documents.Count) {
        [Console]::Out.WriteLine("note: InDesign was left running, because documents are open in it")
    } else {
        $process = Get-Process InDesign | Select-Object -First 1
        $app.Quit(1852776480)
        if (-not $process.WaitForExit(60000)) { [Console]::Out.WriteLine("note: InDesign is still quitting") }
    }
} catch {
    [Console]::Out.WriteLine($_.Exception.Message)
    exit 1
}
"""

LOG = Path(tempfile.gettempdir()) / "young-delegates-notebook-layout.log"


def run_layout(out: Path, reuse: bool = False) -> str:
    LOG.unlink(missing_ok=True)
    env = {
        **os.environ,
        "YDN_SRC": str(build.INDESIGN),
        "YDN_OUT": str(out),
        "YDN_LAYOUT": str(LAYOUT),
        "YDN_LOG": str(LOG),
        "YDN_REUSE": "1" if reuse else "",
    }
    command = base64.b64encode(POWERSHELL.encode("utf-16-le")).decode("ascii")
    done = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-OutputFormat", "Text", "-EncodedCommand", command],
        env=env,
        capture_output=True,
        text=True,
        errors="replace",
    )
    if done.returncode == 2:
        raise SystemExit(
            "InDesign is already running. Save your work and quit it, then run this again,\n"
            "or pass --reuse to run in that session anyway."
        )
    if done.returncode:
        steps = LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []
        raise SystemExit(
            f"InDesign scripting failed: {done.stdout.strip() or done.stderr.strip()}\n"
            f"last finished layout step: {steps[-1] if steps else 'none'}"
        )
    return done.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=build.INDESIGN, help="folder for the .indd and PDFs")
    parser.add_argument("--reuse", action="store_true", help="run in an InDesign that is already open")
    args = parser.parse_args()
    build.build()
    result = run_layout(args.out.resolve(), args.reuse)
    print(result)
    if result.startswith("FAILED") or "\nproblems:" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
