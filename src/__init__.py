"""AI Story Generator with Transformers and Diffusers

A Python package for generating stories with AI-generated images using
Hugging Face's transformers and diffusers libraries.
"""

__version__ = "1.0.0"
__author__ = "AI Story Generator"
__description__ = "Generate stories with AI-powered text and images"

from .story_generator import StoryGenerator
from .image_generator import ImageGenerator
from .story_app import StoryGeneratorApp

__all__ = [
    'StoryGenerator',
    'ImageGenerator', 
    'StoryGeneratorApp'
]