#!/usr/bin/env python3
"""
Complete Story Generation Example

This example demonstrates generating a multi-chapter story
with images for each chapter.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src import StoryGeneratorApp
from src.utils import configure_network_settings, get_sample_prompts


def main():
    """Generate a complete multi-chapter story."""
    print("🚀 Complete Story Generation Example")
    print("=" * 50)
    
    # Configure network settings
    configure_network_settings()
    
    # Show sample prompts
    sample_prompts = get_sample_prompts()
    print("\n🎲 Available sample prompts:")
    for i, prompt in enumerate(sample_prompts[:5], 1):
        print(f"{i}. {prompt}")
    
    # Choose a prompt
    chosen_prompt = sample_prompts[2]  # Steampunk city
    
    print(f"\n📚 Generating complete story with prompt:")
    print(f"'{chosen_prompt}'")
    print("-" * 50)
    
    # Initialize the app
    print("Initializing story generator app...")
    app = StoryGeneratorApp()
    
    # Generate complete story
    story_data = app.generate_complete_story(
        initial_prompt=chosen_prompt,
        num_chapters=3,
        chapter_length=100,
        temperature=0.8,
        art_style="steampunk art, detailed, Victorian era"
    )
    
    print("\n" + "=" * 60)
    print("📊 Story Generation Summary")
    print("=" * 60)
    print(f"Chapters generated: {len(story_data['chapters'])}")
    print(f"Images generated: {len(story_data['images'])}")
    print(f"Total words: ~{len(story_data['full_text'].split())}")
    
    # Save story to file
    with open("generated_complete_story.txt", "w", encoding="utf-8") as f:
        f.write("AI GENERATED STORY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Prompt: {chosen_prompt}\n\n")
        f.write(story_data['full_text'])
        f.write(f"\n\n--- Generated {len(story_data['chapters'])} chapters with {len(story_data['images'])} images ---")
    
    print("✅ Complete story saved as: generated_complete_story.txt")
    
    # Save images
    for i, image_info in enumerate(story_data['images']):
        image_path = f"story_chapter_{image_info['chapter']}_scene_{image_info['scene']}.png"
        image_info['image'].save(image_path)
        print(f"✅ Image saved: {image_path}")
    
    print("\n🎉 Complete story generation finished!")
    print("📁 Check the generated files:")
    print("  - generated_complete_story.txt (story text)")
    print("  - story_chapter_*.png (generated images)")


if __name__ == '__main__':
    main()