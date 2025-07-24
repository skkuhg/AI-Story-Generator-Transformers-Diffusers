"""Interactive story generator application with widgets."""

import ipywidgets as widgets
from IPython.display import display, clear_output
from .story_generator import StoryGenerator
from .image_generator import ImageGenerator


class StoryGeneratorApp:
    """Interactive story generator application with GUI."""
    
    def __init__(self):
        """Initialize the story generator app."""
        self.story_generator = StoryGenerator()
        self.image_generator = ImageGenerator()
        self.image_generator.load_model()
        
        self.current_story = ""
        self.story_images = []
        self.chapter_count = 0
        
        self._create_widgets()
        self._bind_events()
    
    def _create_widgets(self):
        """Create all the UI widgets."""
        self.story_prompt = widgets.Textarea(
            value="Once upon a time, in a magical kingdom",
            placeholder="Enter your story prompt here...",
            description="Story Prompt:",
            layout=widgets.Layout(width='80%', height='100px'),
            style={'description_width': 'initial'}
        )

        self.chapter_length = widgets.IntSlider(
            value=150,
            min=50,
            max=300,
            step=25,
            description="Chapter Length:",
            style={'description_width': 'initial'}
        )

        self.creativity = widgets.FloatSlider(
            value=0.8,
            min=0.1,
            max=1.5,
            step=0.1,
            description="Creativity:",
            style={'description_width': 'initial'}
        )

        self.art_style = widgets.Dropdown(
            options=[
                'fantasy art, detailed, high quality',
                'realistic, photographic, detailed',
                'anime style, colorful, detailed',
                'watercolor painting, artistic',
                'digital art, vibrant, detailed',
                'oil painting, classical, detailed'
            ],
            value='fantasy art, detailed, high quality',
            description="Art Style:",
            style={'description_width': 'initial'}
        )

        self.generate_button = widgets.Button(
            description="📖 Generate Chapter",
            button_style='primary',
            layout=widgets.Layout(width='200px')
        )

        self.continue_button = widgets.Button(
            description="➡️ Continue Story",
            button_style='info',
            layout=widgets.Layout(width='200px')
        )

        self.reset_button = widgets.Button(
            description="🔄 New Story",
            button_style='warning',
            layout=widgets.Layout(width='200px')
        )

        self.output_area = widgets.Output()
    
    def _bind_events(self):
        """Bind button click events."""
        self.generate_button.on_click(self.generate_chapter)
        self.continue_button.on_click(self.continue_story)
        self.reset_button.on_click(self.reset_story)
    
    def generate_chapter(self, button):
        """Generate a new chapter and corresponding images."""
        with self.output_area:
            clear_output(wait=True)

            prompt = self.story_prompt.value
            if not prompt.strip():
                print("❌ Please enter a story prompt!")
                return

            print("🔄 Generating story chapter...")

            # Generate story text
            chapter_text = self.story_generator.generate_chapter(
                prompt,
                max_length=self.chapter_length.value,
                temperature=self.creativity.value
            )

            self.chapter_count += 1
            self.current_story += f"\\n\\n**Chapter {self.chapter_count}**\\n{chapter_text}"

            # Extract scene descriptions for images
            scene_descriptions = self.story_generator.extract_scene_descriptions(chapter_text)

            # Display the chapter
            print(f"📖 **Chapter {self.chapter_count}**")
            print("-" * 50)
            print(chapter_text)
            print("\\n")

            # Generate and display images
            if scene_descriptions:
                print("🎨 Generating images...")
                chapter_images = self.image_generator.generate_story_images(
                    scene_descriptions, 
                    art_style=self.art_style.value
                )
                
                for image_info in chapter_images:
                    image_info['chapter'] = self.chapter_count
                    self.story_images.append(image_info)

            print("\\n✅ Chapter generated successfully!")

            # Update prompt for continuation
            last_sentence = chapter_text.split('.')[-2] + '.' if '.' in chapter_text else chapter_text[-50:]
            self.story_prompt.value = last_sentence

    def continue_story(self, button):
        """Continue the current story."""
        if not self.current_story:
            with self.output_area:
                print("❌ No story to continue! Generate a chapter first.")
            return

        self.generate_chapter(button)

    def reset_story(self, button):
        """Reset the story and start fresh."""
        self.current_story = ""
        self.story_images = []
        self.chapter_count = 0
        self.story_prompt.value = "Once upon a time, in a magical kingdom"

        with self.output_area:
            clear_output()
            print("🔄 Story reset! Ready for a new adventure.")

    def display_app(self):
        """Display the complete story generator app."""
        # Create layout
        controls = widgets.VBox([
            widgets.HTML("<h3>🎯 Story Settings</h3>"),
            self.story_prompt,
            widgets.HBox([self.chapter_length, self.creativity]),
            self.art_style,
            widgets.HTML("<h3>🎮 Controls</h3>"),
            widgets.HBox([self.generate_button, self.continue_button, self.reset_button]),
            widgets.HTML("<hr>"),
            widgets.HTML("<h3>📚 Generated Story</h3>")
        ])

        # Display the app
        display(controls)
        display(self.output_area)
    
    def generate_complete_story(self, initial_prompt, num_chapters=3, chapter_length=150, 
                              temperature=0.8, art_style="fantasy art, detailed, high quality"):
        """
        Generate a complete story with multiple chapters and images.

        Args:
            initial_prompt (str): Starting prompt for the story
            num_chapters (int): Number of chapters to generate
            chapter_length (int): Length of each chapter
            temperature (float): Creativity level
            art_style (str): Art style for images

        Returns:
            dict: Complete story with text and images
        """
        # Generate story text
        story_data = self.story_generator.generate_complete_story(
            initial_prompt, num_chapters, chapter_length, temperature
        )
        
        # Generate images for each chapter
        all_images = []
        
        for chapter in story_data['chapters']:
            if chapter['scene_descriptions']:
                print(f"\\n🎨 Generating images for Chapter {chapter['number']}...")
                chapter_images = self.image_generator.generate_story_images(
                    chapter['scene_descriptions'], 
                    art_style=art_style
                )
                
                # Add chapter info to each image
                for image_info in chapter_images:
                    image_info['chapter'] = chapter['number']
                    all_images.append(image_info)
        
        story_data['images'] = all_images
        
        print(f"\\n🖼️ Total images generated: {len(all_images)}")
        
        return story_data