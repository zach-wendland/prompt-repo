from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptlab",
    version="1.0.0",
    author="PromptLab Team",
    author_email="",
    description="A genetic approach to prompt engineering - breed, mutate, and evolve AI prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zach-wendland/prompt-repo",
    packages=find_packages(),
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
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "promptlab=promptlab.cli:cli",
        ],
    },
)
