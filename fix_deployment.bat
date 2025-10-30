@echo off
echo 🔧 Fixing deployment issues...
echo.

echo ✅ Cleaning up test files...
if exist test_local.py del test_local.py

echo ✅ Adding deployment fixes...
git add .

echo ✅ Committing fixes...
git commit -m "Fix deployment build issues

- Update pyproject.toml with correct package structure and compatible versions
- Use opencv-python-headless for Docker compatibility
- Improve Dockerfile with better dependency handling
- Add .dockerignore to reduce build size
- Create fallback crew implementation without decorators
- Fix import paths for deployment environment

Fixes: Building your image failed error"

echo ✅ Pushing fixes...
git push

echo.
echo 🎉 Deployment fixes committed and pushed!
echo 🚀 Try deploying again - the build should now work!
echo.
pause