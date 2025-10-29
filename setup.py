from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crewai-video-study-guide",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Fast, AI-powered study guide generation from YouTube videos using CrewAI and Google Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crewai-video-study-guide",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "crewai-video-study=main_crew:main",
        ],
    },
    keywords="crewai, ai, video, study-guide, education, youtube, gemini, automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/crewai-video-study-guide/issues",
        "Source": "https://github.com/yourusername/crewai-video-study-guide",
        "Documentation": "https://github.com/yourusername/crewai-video-study-guide#readme",
    },
)