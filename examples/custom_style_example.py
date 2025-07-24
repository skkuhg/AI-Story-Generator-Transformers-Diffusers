#!/usr/bin/env python3
"""
Custom Art Style Example

This example demonstrates how to use different art styles
and customize image generation parameters.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src import StoryGenerator, ImageGenerator
from src.utils import configure_network_settings


def main():
    """Demonstrate different art styles for story images."""
    print("🎨 Custom Art Style Example")
    print("=" * 50)
    
    # Configure network settings
    configure_network_settings()
    
    # Initialize generators
    story_gen = StoryGenerator()
    image_gen = ImageGenerator()
    image_gen.load_model()
    
    # Story scenario
    scene_description = "A warrior standing on a cliff overlooking a vast kingdom at sunset"
    
    # Different art styles to try
    art_styles = [
        ("fantasy_art", "fantasy art, detailed, high quality, epic"),
        ("realistic", "realistic, photographic, detailed, cinematic"),
        ("anime", "anime style, colorful, detailed, manga art"),
        ("watercolor", "watercolor painting, artistic, soft colors"),
        ("digital_art", "digital art, vibrant, modern, stylized"),
        ("oil_painting", "oil painting, classical, detailed, Renaissance style")
    ]
    
    print(f"🖼️ Generating images for scene: '{scene_description}'")
    print("Using different art styles...\n")
    
    for style_name, style_prompt in art_styles:
        print(f"🎨 Generating {style_name} style...")
        
        try:
            # Generate image with specific style
            image = image_gen.generate_image(
                scene_description,
                style=style_prompt,
                negative_prompt="blurry, low quality, distorted, ugly"
            )
            
            # Save image
            image_path = f"warrior_scene_{style_name}.png"
            image.save(image_path)
            print(f"✅ Saved: {image_path}")
            
        except Exception as e:
            print(f"❌ Error generating {style_name}: {e}")
    
    print("\n" + "=" * 50)
    print("🎭 Advanced Style Examples")
    print("=" * 50)
    
    # Advanced style combinations
    advanced_styles = {
        "cyberpunk_noir": {
            "scene": "A detective in a neon-lit alley during a thunderstorm",
            "style": "cyberpunk, noir, neon lights, dark atmosphere, futuristic",
            "negative": "bright, sunny, medieval, fantasy"
        },
        "cosmic_horror": {
            "scene": "An ancient temple floating in space surrounded by tentacled creatures",
            "style": "cosmic horror, Lovecraftian, eldritch, dark space, tentacles",
            "negative": "cute, bright colors, cheerful, simple"
        },
        "steampunk_adventure": {
            "scene": "An airship captain navigating through floating islands",
            "style": "steampunk, Victorian era, brass and copper, mechanical, adventure",
            "negative": "modern, digital, plastic, futuristic technology"
        }
    }
    
    for name, config in advanced_styles.items():
        print(f"\n🌟 Generating {name} style...")
        print(f"Scene: {config['scene']}")
        
        try:
            image = image_gen.generate_image(
                config['scene'],
                style=config['style'],
                negative_prompt=config['negative']
            )
            
            image_path = f"advanced_{name}.png"
            image.save(image_path)
            print(f"✅ Saved: {image_path}")
            
        except Exception as e:
            print(f"❌ Error generating {name}: {e}")
    
    print("\n🎉 Custom style generation completed!")
    print("📁 Check the generated image files to see the different styles.")


if __name__ == '__main__':
    main()