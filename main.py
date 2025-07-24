#!/usr/bin/env python3
"""
AI Story Generator with Transformers and Diffusers

Main application script for running the story generator.
"""

import argparse
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import StoryGenerator, ImageGenerator, StoryGeneratorApp
from src.utils import configure_network_settings, get_sample_prompts, display_usage_tips


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="AI Story Generator with Transformers and Diffusers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive                    # Launch interactive app
  python main.py --generate "Once upon a time"   # Generate single chapter
  python main.py --complete "Magic kingdom" -c 3 # Generate complete story
  python main.py --samples                       # Show sample prompts
        """
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Launch interactive Jupyter widget app'
    )
    
    parser.add_argument(
        '--generate', '-g',
        type=str,
        help='Generate a single chapter from prompt'
    )
    
    parser.add_argument(
        '--complete', '-c',
        type=str,
        help='Generate complete story from prompt'
    )
    
    parser.add_argument(
        '--chapters', '-n',
        type=int,
        default=3,
        help='Number of chapters for complete story (default: 3)'
    )
    
    parser.add_argument(
        '--length', '-l',
        type=int,
        default=150,
        help='Chapter length in tokens (default: 150)'
    )
    
    parser.add_argument(
        '--creativity', '-t',
        type=float,
        default=0.8,
        help='Creativity/temperature setting (0.1-1.5, default: 0.8)'
    )
    
    parser.add_argument(
        '--style', '-s',
        type=str,
        default='fantasy art, detailed, high quality',
        help='Art style for image generation'
    )
    
    parser.add_argument(
        '--no-images',
        action='store_true',
        help='Skip image generation (text only)'
    )
    
    parser.add_argument(
        '--samples',
        action='store_true',
        help='Show sample story prompts'
    )
    
    parser.add_argument(
        '--tips',
        action='store_true',
        help='Show usage tips'
    )
    
    args = parser.parse_args()
    
    # Show samples
    if args.samples:
        print("🎲 Sample Story Prompts:")
        print("=" * 50)
        for i, prompt in enumerate(get_sample_prompts(), 1):
            print(f"{i:2d}. {prompt}")
        return
    
    # Show tips
    if args.tips:
        display_usage_tips()
        return
    
    # Configure network settings
    configure_network_settings()
    
    # Launch interactive app
    if args.interactive:
        print("🚀 Launching Interactive Story Generator...")
        try:
            app = StoryGeneratorApp()
            print("✅ App initialized successfully!")
            print("\n" + "="*60)
            print("📱 Interactive Story Generator Ready!")
            print("="*60)
            app.display_app()
            display_usage_tips()
        except Exception as e:
            print(f"❌ Error launching interactive app: {e}")
            return 1
    
    # Generate single chapter
    elif args.generate:
        print(f"📖 Generating single chapter from: '{args.generate}'")
        try:
            story_gen = StoryGenerator()
            chapter_text = story_gen.generate_chapter(
                args.generate,
                max_length=args.length,
                temperature=args.creativity
            )
            
            print("\n" + "="*60)
            print("📚 Generated Chapter:")
            print("="*60)
            print(chapter_text)
            
            # Generate images if requested
            if not args.no_images:
                print("\n🎨 Generating images...")
                image_gen = ImageGenerator()
                image_gen.load_model()
                
                scene_descriptions = story_gen.extract_scene_descriptions(chapter_text)
                if scene_descriptions:
                    images = image_gen.generate_story_images(scene_descriptions, args.style)
                    print(f"✅ Generated {len(images)} images")
                else:
                    print("ℹ️ No visual scenes detected for image generation")
            
        except Exception as e:
            print(f"❌ Error generating chapter: {e}")
            return 1
    
    # Generate complete story
    elif args.complete:
        print(f"📚 Generating {args.chapters}-chapter story from: '{args.complete}'")
        try:
            if args.no_images:
                # Text only
                story_gen = StoryGenerator()
                story_data = story_gen.generate_complete_story(
                    args.complete,
                    num_chapters=args.chapters,
                    chapter_length=args.length,
                    temperature=args.creativity
                )
                print(f"✅ Generated {len(story_data['chapters'])} chapters")
            else:
                # Text and images
                app = StoryGeneratorApp()
                story_data = app.generate_complete_story(
                    args.complete,
                    num_chapters=args.chapters,
                    chapter_length=args.length,
                    temperature=args.creativity,
                    art_style=args.style
                )
                print(f"✅ Generated {len(story_data['chapters'])} chapters and {len(story_data['images'])} images")
                
        except Exception as e:
            print(f"❌ Error generating complete story: {e}")
            return 1
    
    else:
        # No specific action, show help
        parser.print_help()
        print("\n💡 Quick start:")
        print("  python main.py --interactive    # Launch interactive app")
        print("  python main.py --samples        # Show sample prompts")
        print("  python main.py --tips           # Show usage tips")
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)