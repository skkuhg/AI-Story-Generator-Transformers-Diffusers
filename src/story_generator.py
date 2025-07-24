"""Story text generation module using transformers."""

import torch
import re
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')


class StoryGenerator:
    """Handles story text generation using pre-trained language models."""
    
    def __init__(self, model_name="gpt2-medium"):
        """
        Initialize the story generator.
        
        Args:
            model_name (str): Name of the pre-trained model to use
        """
        self.model_name = model_name
        self.text_generator = None
        self.load_model()
    
    def load_model(self):
        """Load the text generation model."""
        print(f"Loading text generation model: {self.model_name}...")
        
        try:
            self.text_generator = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            print("✅ Text generation model loaded successfully!")
            print(f"Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def generate_chapter(self, prompt, max_length=200, temperature=0.8, num_return_sequences=1):
        """
        Generate a story chapter based on a given prompt.

        Args:
            prompt (str): The starting prompt for the story
            max_length (int): Maximum length of generated text
            temperature (float): Controls randomness (0.1 = conservative, 1.0 = creative)
            num_return_sequences (int): Number of different versions to generate

        Returns:
            str: Generated story text
        """
        if not self.text_generator:
            raise RuntimeError("Text generator not loaded. Call load_model() first.")
        
        try:
            generated = self.text_generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=num_return_sequences,
                pad_token_id=self.text_generator.tokenizer.eos_token_id,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )

            story_text = generated[0]['generated_text']

            # Clean up the text (remove the original prompt and clean formatting)
            if story_text.startswith(prompt):
                story_text = story_text[len(prompt):].strip()

            return story_text

        except Exception as e:
            return f"Error generating story: {str(e)}"
    
    def extract_scene_descriptions(self, text):
        """
        Extract visual scene descriptions from story text for image generation.

        Args:
            text (str): Story text

        Returns:
            list: List of scene descriptions suitable for image generation
        """
        sentences = text.split('.')
        scene_descriptions = []

        # Look for sentences with visual descriptors
        visual_keywords = [
            'looked', 'saw', 'appeared', 'stood', 'walked', 'dark', 'bright',
            'beautiful', 'scary', 'ancient', 'mysterious', 'golden', 'silver',
            'forest', 'castle', 'mountain', 'ocean', 'sky', 'moon', 'sun'
        ]

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in visual_keywords):
                # Clean and format for image generation
                clean_sentence = re.sub(r'[^\w\s,.-]', '', sentence)
                if len(clean_sentence) > 10:
                    scene_descriptions.append(clean_sentence)

        return scene_descriptions[:2]  # Return max 2 scenes per chapter
    
    def generate_complete_story(self, initial_prompt, num_chapters=3, chapter_length=150, temperature=0.8):
        """
        Generate a complete story with multiple chapters.

        Args:
            initial_prompt (str): Starting prompt for the story
            num_chapters (int): Number of chapters to generate
            chapter_length (int): Length of each chapter
            temperature (float): Creativity level

        Returns:
            dict: Complete story data with chapters and metadata
        """
        story_data = {
            'chapters': [],
            'full_text': '',
            'metadata': {
                'initial_prompt': initial_prompt,
                'num_chapters': num_chapters,
                'chapter_length': chapter_length,
                'temperature': temperature
            }
        }

        current_prompt = initial_prompt

        print(f"📚 Generating a {num_chapters}-chapter story...")
        print("=" * 60)

        for chapter_num in range(1, num_chapters + 1):
            print(f"\n🔄 Generating Chapter {chapter_num}...")

            # Generate chapter text
            chapter_text = self.generate_chapter(
                current_prompt,
                max_length=chapter_length,
                temperature=temperature
            )

            # Store chapter
            chapter_data = {
                'number': chapter_num,
                'text': chapter_text,
                'prompt': current_prompt,
                'scene_descriptions': self.extract_scene_descriptions(chapter_text)
            }
            
            story_data['chapters'].append(chapter_data)
            story_data['full_text'] += f"\n\n**Chapter {chapter_num}**\n{chapter_text}"

            # Display chapter
            print(f"\n📖 **Chapter {chapter_num}**")
            print("-" * 40)
            print(chapter_text)

            # Prepare prompt for next chapter
            if chapter_num < num_chapters:
                last_sentences = chapter_text.split('.')[-3:-1]
                transition_prompt = '. '.join(last_sentences) + '. Meanwhile,'
                current_prompt = transition_prompt

            print(f"✅ Chapter {chapter_num} completed!")

        print("\n" + "=" * 60)
        print(f"🎉 Complete story generated successfully!")
        print(f"📊 Total chapters: {len(story_data['chapters'])}")

        return story_data