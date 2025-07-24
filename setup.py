"""Setup script for AI Story Generator package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-story-generator-transformers-diffusers",
    version="1.0.0",
    author="AI Story Generator Team",
    author_email="contact@example.com",
    description="Generate stories with AI-powered text and images using Transformers and Diffusers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-story-generator-transformers-diffusers",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Text Processing :: Creative",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.0.0",
        ],
        "gpu": [
            "torch[cuda]",
            "xformers",
        ],
    },
    entry_points={
        "console_scripts": [
            "story-generator=main:main",
        ],
    },
    keywords="ai, story, generation, transformers, diffusers, stable-diffusion, gpt2, huggingface",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-story-generator-transformers-diffusers/issues",
        "Source": "https://github.com/yourusername/ai-story-generator-transformers-diffusers",
        "Documentation": "https://github.com/yourusername/ai-story-generator-transformers-diffusers#readme",
    },
)