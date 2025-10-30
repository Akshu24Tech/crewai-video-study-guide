#!/bin/bash

echo "🚀 Committing CrewAI deployment structure fixes..."
echo

echo "✅ Adding all new files..."
git add .

echo "✅ Committing changes..."
git commit -m "Fix CrewAI deployment structure

- Add pyproject.toml for proper CrewAI deployment
- Create src/crew.py entry point required by CrewAI
- Add proper CrewAI project structure with agents.yaml and tasks.yaml
- Restructure video tools for deployment compatibility
- Add requirements.txt and Dockerfile for multiple deployment options
- Keep original main.py working alongside new structure
- Fix deployment errors: Cannot find pyproject.toml and src/crew.py

Resolves deployment issues while maintaining all existing functionality."

echo "✅ Pushing to repository..."
git push

echo
echo "🎉 All changes committed and pushed!"
echo "🚀 Your project is now ready for CrewAI deployment!"
echo