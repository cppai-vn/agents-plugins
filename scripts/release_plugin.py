#!/usr/bin/env python3
"""Release a plugin of this marketplace in one step: bump version, CHANGELOG, validate, commit,
push and refresh the local install.

Usage (from anywhere inside the repository):
    python3 scripts/release_plugin.py <plugin> <patch|minor|major|X.Y.Z> -n "change" [-n "change" ...]
                                      [-m "commit subject"] [--push] [--install] [--yes]

Without --yes it only prints the plan. With --yes it:
  1. sets "version" in <plugin>/.claude-plugin/plugin.json,
  2. adds a "## <version> — <date>" entry with the notes to <plugin>/CHANGELOG.md,
  3. runs `claude plugin validate --strict` on the marketplace and the plugin and
     compiles every Python file,
  4. commits all pending changes in the repository with the subject
     (default "release(<plugin>): <version>") and the notes as body,
  5. --push: pushes the current branch,
  6. --install: `claude plugin marketplace update <marketplace>` and
     `claude plugin update <plugin>@<marketplace>`, so a new session runs the release
     (installed plugins run from a per-version cache).
Stops at the first failing step; nothing is committed if validation fails.
"""
import argparse
import ast
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True,
                      cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
SEMVER = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')


def run(cmd, check=True):
    print('  $ ' + ' '.join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (result.stdout + result.stderr).strip()
    if out:
        print('    ' + out.replace('\n', '\n    ')[-1500:])
    if check and result.returncode != 0:
        raise SystemExit(f'failed: {" ".join(cmd)} (exit {result.returncode})')
    return result


def check_python_syntax():
    """Parse every Python file (no bytecode written); the VCS folder is skipped."""
    vcs_dir = os.path.join(ROOT, '.' + 'git')
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if dirpath.startswith(vcs_dir):
            continue
        for name in filenames:
            if name.endswith('.py'):
                path = os.path.join(dirpath, name)
                try:
                    ast.parse(open(path, encoding='utf-8').read(), path)
                except SyntaxError as err:
                    raise SystemExit(f'Python syntax error: {err}')


def next_version(current, bump):
    if SEMVER.match(bump):
        return bump
    major, minor, patch = (int(x) for x in SEMVER.match(current).groups())
    if bump == 'major':
        return f'{major + 1}.0.0'
    if bump == 'minor':
        return f'{major}.{minor + 1}.0'
    if bump == 'patch':
        return f'{major}.{minor}.{patch + 1}'
    raise SystemExit(f'bad bump {bump!r}: use patch, minor, major or X.Y.Z')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('plugin')
    parser.add_argument('bump')
    parser.add_argument('-n', '--note', action='append', required=True, help='CHANGELOG bullet (repeatable)')
    parser.add_argument('-m', '--message', help='commit subject')
    parser.add_argument('--push', action='store_true')
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--yes', action='store_true')
    args = parser.parse_args()

    plugin_dir = os.path.join(ROOT, args.plugin)
    manifest_path = os.path.join(plugin_dir, '.claude-plugin', 'plugin.json')
    changelog_path = os.path.join(plugin_dir, 'CHANGELOG.md')
    marketplace = json.load(open(os.path.join(ROOT, '.claude-plugin', 'marketplace.json'), encoding='utf-8'))
    if not os.path.isfile(manifest_path):
        raise SystemExit(f'no plugin manifest at {os.path.relpath(manifest_path, ROOT)}')
    if args.plugin not in [p['name'] for p in marketplace['plugins']]:
        raise SystemExit(f'{args.plugin} is not listed in marketplace.json')
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    current = manifest.get('version', '0.0.0')
    version = next_version(current, args.bump)
    if version == current:
        raise SystemExit(f'version is already {current}')
    changelog = open(changelog_path, encoding='utf-8').read() if os.path.isfile(changelog_path) else f'# Changelog — {args.plugin} plugin\n\n'
    if re.search(rf'^## {re.escape(version)}\b', changelog, re.M):
        raise SystemExit(f'CHANGELOG already has {version}')
    subject = args.message or f'release({args.plugin}): {version}'
    market = marketplace['name']

    print(f'Release {args.plugin} {current} -> {version} (marketplace {market})')
    print('  notes: ' + ' | '.join(args.note))
    print(f'  commit: {subject}')
    print(f"  then: {'push' if args.push else 'no push'}, {'refresh local install' if args.install else 'no install refresh'}")
    pending = run(['git', 'status', '--short'], check=False).stdout.strip()
    if not args.yes:
        print('\ndry run: re-run with --yes to release')
        return 0
    if not pending:
        print('  note: no pending changes besides the version bump')

    manifest['version'] = version
    with open(manifest_path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    entry = f'## {version} — {datetime.date.today().isoformat()}\n\n' + ''.join(f'- {n}\n' for n in args.note) + '\n'
    first = re.search(r'^## ', changelog, re.M)
    changelog = changelog[:first.start()] + entry + changelog[first.start():] if first else changelog.rstrip('\n') + '\n\n' + entry
    with open(changelog_path, 'w', encoding='utf-8') as fh:
        fh.write(changelog)
    print(f'  ✓ version {version} and CHANGELOG entry written')

    try:
        run(['claude', 'plugin', 'validate', '.', '--strict'])
        run(['claude', 'plugin', 'validate', args.plugin, '--strict'])
        check_python_syntax()
        print('  ✓ validation passed')
    except SystemExit:
        print('  validation failed: version and CHANGELOG were changed but nothing was committed; fix and re-run, '
              'or revert with: git checkout -- ' + os.path.relpath(manifest_path, ROOT) + ' ' + os.path.relpath(changelog_path, ROOT))
        raise

    run(['git', 'add', '-A'])
    run(['git', 'commit', '-q', '-m', subject, '-m', '\n'.join(f'- {n}' for n in args.note)])
    print('  ✓ committed')
    if args.push:
        run(['git', 'push', '-q'])
        print('  ✓ pushed (CI validates on GitHub)')
    if args.install:
        run(['claude', 'plugin', 'marketplace', 'update', market])
        run(['claude', 'plugin', 'update', f'{args.plugin}@{market}'])
        print('  ✓ local install refreshed — start a new agent session to load it')
    return 0


if __name__ == '__main__':
    sys.exit(main())
