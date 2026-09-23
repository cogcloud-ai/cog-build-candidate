"""Materialize one validated snapshot; never author, evaluate, or execute it."""
import fcntl
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(WORKSPACE / 'cog-workbench/src'))
from workbench_suite import Suite, digest, package_digest, require


def check_input(bundle):
    import cog_core
    request = bundle.get('author_request', {})
    contract = request.get('contract', {})
    if contract.get('kind') != 'code' or request.get('operation') not in ('author', 'revise'):
        return [cog_core.problem('build-contract', 'This slice requires accepted pure-code author/revise input.')]
    if bundle.get('accepted_contract_sha256') != digest(contract):
        return [cog_core.problem('build-contract', 'Accepted contract digest differs from the supplied contract.')]
    return []


def materialize(bundle, suite):
    request, envelope = bundle['author_request'], bundle['author_envelope']
    snapshot = suite.source_snapshot(request, envelope)
    source_sha = digest({'contract': snapshot['contract'], 'files': sorted(snapshot['files'], key=lambda f: f['path'])})
    parent = suite.root(bundle['output_dir'])
    # All writes are confined to the explicit caller-selected artifact directory.
    parent.mkdir(parents=True, exist_ok=True)
    destination = parent / request['identity']['name']
    receipt = parent / 'materialization.json'
    lock = parent / '.materialization.lock'
    require(not receipt.is_symlink() and not lock.is_symlink(), 'Artifact control paths may not be symlinks.')
    request_sha = digest(bundle)
    with lock.open('a+') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        if receipt.exists():
            saved = json.loads(receipt.read_text())
            require(saved['request_sha256'] == request_sha, 'Artifact directory belongs to another build request.')
            result = saved['result']
            require(result['source_sha256'] == source_sha and result['path'] == str(destination), 'Materialization receipt mismatch.')
            require(package_digest(destination) == result['package_sha256'], 'Materialized package changed; start a fresh candidate.')
            return result
        packaged = suite.package(request, envelope, destination)
        result = {'path': packaged['path'], 'source_sha256': source_sha,
                  'package_sha256': package_digest(destination), 'plan_request': snapshot,
                  'package_check': packaged['check'], 'authority_use': [],
                  'status': 'packaged-not-runtime-tested'}
        # A crash before this receipt leaves a collision, not permission to overwrite.
        with receipt.open('x') as output:
            json.dump({'request_sha256': request_sha, 'result': result}, output, indent=2)
        return result


def run(bundle, grant, journal):
    return materialize(bundle, Suite(workspace=WORKSPACE)), []


def check_output(payload, bundle):
    import cog_core
    expected = digest({'contract': bundle['author_request']['contract'],
                       'files': sorted(payload['plan_request']['files'], key=lambda f: f['path'])})
    return [] if payload['source_sha256'] == expected else [cog_core.problem('source-identity', 'Expanded source fingerprint mismatch.')]
