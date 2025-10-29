# Contributing to CrewAI Video Study Guide Generator

Thank you for your interest in contributing! 🎉

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a new branch for your feature
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/crewai-video-study-guide.git
cd crewai-video-study-guide

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys
```

## 📝 Code Style

- Use **clear, descriptive variable names**
- Add **docstrings** to functions
- Keep functions **focused and small**
- Use **type hints** where helpful
- Follow **PEP 8** style guidelines

## 🧪 Testing

Before submitting:

1. **Test with different video types**:
   - Short videos (< 5 minutes)
   - Long videos (> 1 hour)
   - Educational content
   - Different languages

2. **Verify cleanup works**:
   - Run multiple times
   - Check screenshot folder cleanup
   - Ensure no content mixing

3. **Check error handling**:
   - Invalid URLs
   - Network issues
   - Missing API keys

## 🎯 Areas for Contribution

### 🔥 High Priority
- **Performance optimizations**
- **Better error handling**
- **Support for more video platforms**
- **Improved content extraction**

### 💡 Feature Ideas
- **Batch processing** multiple videos
- **Different output formats** (PDF, HTML)
- **Custom templates** for study guides
- **Multi-language support**
- **Integration with learning platforms**

### 🐛 Bug Fixes
- **Platform-specific issues**
- **Edge cases in video processing**
- **Memory optimization**
- **API rate limiting**

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style
- [ ] Tests pass with different videos
- [ ] Documentation updated if needed
- [ ] No sensitive data (API keys) committed

### PR Description Template
```markdown
## 🎯 What does this PR do?
Brief description of changes

## 🧪 How to test?
Steps to test the changes

## 📸 Screenshots (if applicable)
Before/after comparisons

## ✅ Checklist
- [ ] Tested with multiple videos
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Follows code style
```

## 🏷️ Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "feat: add batch processing for multiple videos"
git commit -m "fix: handle permission errors in screenshot cleanup"
git commit -m "docs: update installation instructions"

# Avoid
git commit -m "fix stuff"
git commit -m "update"
```

## 🎨 Code Examples

### Adding a New Feature
```python
def new_feature_function(param: str) -> str:
    """
    Brief description of what this function does.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    # Implementation here
    return result
```

### Error Handling
```python
try:
    # Risky operation
    result = process_video(url)
except VideoProcessingError as e:
    print(f"⚠️  Video processing failed: {e}")
    # Graceful fallback
    result = create_basic_guide(url)
```

## 🤝 Community Guidelines

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** and best practices
- **Give constructive feedback**
- **Celebrate successes** together

## 📞 Getting Help

- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Report bugs via GitHub Issues
- 📧 **Direct contact**: For sensitive matters

## 🏆 Recognition

Contributors will be:
- **Listed** in the README
- **Credited** in release notes
- **Thanked** in the community

Thank you for making this project better! 🙏