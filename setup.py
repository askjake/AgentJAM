#!/usr/bin/env python3
"""
Setup script for AgentJAM
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="agentjam",
    version="0.1.0",
    author="Jake (askjake)",
    author_email="jake@example.com",
    description="Multi-model AI agent with intelligent reasoning mode routing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askjake/AgentJAM",
    project_urls={
        "Bug Tracker": "https://github.com/askjake/AgentJAM/issues",
        "Documentation": "https://github.com/askjake/AgentJAM/tree/main/docs",
        "Source Code": "https://github.com/askjake/AgentJAM",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "black>=23.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentjam=agentjam.__main__:main",
        ],
    },
)
