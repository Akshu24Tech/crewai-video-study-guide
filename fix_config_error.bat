@echo off
echo 🔧 Fixing config directory error...
echo.

echo ✅ Adding config files and decorator-based crew...
git add .

echo ✅ Committing config fix...
git commit -m "Fix config directory error for CrewAI deployment

✅ ADDED:
- src/crewai_video_study_guide/config/agents.yaml - Agent configurations
- src/crewai_video_study_guide/config/tasks.yaml - Task definitions

✅ UPDATED:
- src/crewai_video_study_guide/crew.py - Use @CrewBase decorators
- Restored decorator-based approach that deployment system expects

✅ FIXES:
- Cannot find src/crewai_video_study_guide/config error
- Proper CrewAI project structure with YAML configs
- Standard decorator pattern for agents and tasks

The deployment system now finds all required config files."

echo ✅ Pushing config fix...
git push

echo.
echo 🎉 Config directory error fixed!
echo 🚀 CrewAI deployment should now find all required files!
echo.
echo 📋 Structure now includes:
echo   ✅ src/crewai_video_study_guide/config/agents.yaml
echo   ✅ src/crewai_video_study_guide/config/tasks.yaml
echo   ✅ @CrewBase decorator-based crew class
echo   ✅ Standard CrewAI project format
echo.
echo 💡 Try deploying again - the config error should be resolved!
echo.
pause