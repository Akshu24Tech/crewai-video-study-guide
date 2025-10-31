@echo off
echo 🔧 Fixing crew offline issues...
echo.

echo ✅ Adding debugging and error handling...
git add .

echo ✅ Committing offline fixes...
git commit -m "Fix crew going offline - Add debugging and error handling

✅ IMPROVEMENTS:
- Added comprehensive logging to crew.py
- Added error handling and fallback mechanisms
- Added health check function to diagnose issues
- Added environment variable validation
- Created test_crew.py for debugging

✅ FIXES:
- Handles missing API keys gracefully
- Provides detailed error messages
- Fallback video tool if import fails
- Better logging for troubleshooting
- Health check before running crew

✅ DEBUGGING:
- Logs show exactly what's failing
- Environment variable status checking
- Import validation
- Step-by-step execution tracking

This should help identify why the crew goes offline."

echo ✅ Pushing offline fixes...
git push

echo.
echo 🎉 Debugging improvements committed!
echo 🔍 The crew now has detailed logging to show what's failing!
echo.
echo 📋 What's added:
echo   ✅ Comprehensive error handling
echo   ✅ Environment variable validation  
echo   ✅ Health check function
echo   ✅ Detailed logging
echo   ✅ test_crew.py for debugging
echo.
echo 💡 Deploy again and check the logs to see what's causing offline status!
echo.
pause