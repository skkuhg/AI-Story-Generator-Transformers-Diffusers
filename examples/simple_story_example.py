#!/usr/bin/env python3
"""
Simple Story Generation Example

This example demonstrates basic usage of the story generator
for creating a single chapter with images.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src import StoryGenerator, ImageGenerator
from src.utils import configure_network_settings


def main():
    """Generate a simple story with images."""
    print("🚀 Simple Story Generation Example")
    print("=" * 50)
    
    # Configure network settings
    configure_network_settings()
    
    # Initialize generators
    print("Initializing story generator...")
    story_gen = StoryGenerator()
    
    print("Initializing image generator...")
    image_gen = ImageGenerator()
    image_gen.load_model()
    
    # Story prompt
    prompt = "In a enchanted library where books floated through the air"
    
    print(f"\n📖 Generating story from prompt: '{prompt}'")
    print("-" * 50)
    
    # Generate story text
    chapter_text = story_gen.generate_chapter(
        prompt,
        max_length=120,
        temperature=0.8
    )
    
    print("Generated Chapter:")
    print(chapter_text)
    
    # Extract visual scenes
    scenes = story_gen.extract_scene_descriptions(chapter_text)
    print(f"\n🎬 Found {len(scenes)} visual scenes:")
    for i, scene in enumerate(scenes, 1):
        print(f"{i}. {scene}")
    
    # Generate images for scenes
    if scenes:
        print(f"\n🎨 Generating {len(scenes)} images...")
        for i, scene in enumerate(scenes):
            print(f"\nGenerating image {i+1}: {scene[:50]}...")
            image = image_gen.generate_image(
                scene, 
                style="fantasy art, magical, detailed"
            )
            
            # Save image
            image_path = f"generated_image_{i+1}.png"
            image.save(image_path)
            print(f"✅ Image saved as: {image_path}")
    
    print("\n🎉 Story generation completed!")


if __name__ == '__main__':
    main()