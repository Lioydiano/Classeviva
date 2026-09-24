# Releasing a version

1. Set `VERSION` in `setup.py` to the new version (for example, `1.2.11rc1`). Do this **before** creating the tag; the package version comes from this file.
2. Commit the change, then tag that commit with `v` plus the version:

   ```sh
   git add setup.py
   git commit -m "Release 1.2.11rc1"
   git tag v1.2.11rc1
   git push origin main v1.2.11rc1
   ```

3. Build and check the package from the tagged commit:

   ```sh
   python -m venv .venv
   .venv/bin/python -m pip install build twine
   .venv/bin/python -m build --sdist
   .venv/bin/python -m twine check dist/classeviva_py-1.2.11rc1.tar.gz
   ```

4. Upload the new archive to PyPI. Use a PyPI API token as the password; never commit it:

   ```sh
   .venv/bin/python -m twine upload --username __token__ dist/classeviva_py-1.2.11rc1.tar.gz
   ```

5. Create a GitHub release from the tag. Mark release candidates as **pre-releases**. Verify that the GitHub tag and the version on [PyPI](https://pypi.org/project/Classeviva.py/) match.

If you created a tag but the underlying code was not ready (e.g. you outran a merge on main, or you forgot to update the version in setup.py), run `git push origin --delete v1.2.11rc1` and `git tag -d v1.2.11rc1` before step 2. Recreate the tag only after committing the version change. If you cannot do so because the main branch is protected, then just abort that release candidate and bump the rc version by one.
