# Maintainer guide

## Change flow

1. Work on a branch.
2. Run `python3 scripts/check_all.py` — **from an environment with the pinned
   dependencies installed**, on Python 3.11 or later:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   python3 -m pip install --requirement requirements.lock
   ```

   Both prerequisites now fail fast and name the remedy: a too-old interpreter
   is rejected before any gate runs, and a missing dependency stops the run at
   the gate that needs it. Neither is a broken checkout.
3. Review the privacy report and generated-file status.
4. Open a pull request and let required checks finish.
5. Squash merge after conversations are resolved.

## Generated artifacts

Run `make docs` after changing any canonical Markdown paired with DOCX. Run
`make media` after changing the demonstration storyboard. Commit source and
generated artifacts together only after parity and privacy checks pass.

The captioned MP4 is built from the same synthetic frames as the README GIF.
On macOS, `make media` uses the system Swift and AVFoundation frameworks; it
does not require a global video package. Other platforms may keep the committed
MP4 and run the portable validation gates without regenerating it.

## Release flow

1. Update `CHANGELOG.md`, `CITATION.cff`, compatibility evidence, and benchmark
   limitations.
2. Run `make release-check`.
3. Create and push the signed annotated version tag.
4. Trigger the manual release workflow; it creates or refreshes a draft release.
5. Inspect and download every draft artifact.
6. Verify `SHA256SUMS.txt`, the release manifest, and an artifact attestation.
7. Publish the draft release manually.
8. Reopen the release and verify the public downloads.

The release workflow prepares assets and the GitHub draft; it does not publish
the release.

## Versioning

Use semantic versions for the repository release. The context schema has its
own version and changes only when the public document contract changes.
