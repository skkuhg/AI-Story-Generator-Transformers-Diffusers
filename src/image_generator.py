"""Image generation module using diffusers."""

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


class ImageGenerator:
    """Handles AI image generation using Stable Diffusion."""
    
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        """
        Initialize the image generator.
        
        Args:
            model_id (str): Hugging Face model ID for Stable Diffusion
        """
        self.model_id = model_id
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_loaded = False
    
    def load_model(self):
        """Load the Stable Diffusion model with fallback options."""
        print("Loading image generation model...")
        
        # Try multiple model options with fallbacks
        model_options = [
            "runwayml/stable-diffusion-v1-5",
            "CompVis/stable-diffusion-v1-4", 
            "stabilityai/stable-diffusion-2-1-base"
        ]
        
        for model_id in model_options:
            try:
                print(f"Attempting to load: {model_id}")
                
                self.pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=self.torch_dtype,
                    use_safetensors=True,
                    resume_download=True,
                    local_files_only=False,
                    use_auth_token=False,
                    low_cpu_mem_usage=True
                )
                
                self.pipeline = self.pipeline.to(self.device)
                
                # Enable memory efficient attention if using GPU
                if torch.cuda.is_available():
                    self.pipeline.enable_attention_slicing()
                    self.pipeline.enable_model_cpu_offload()
                
                print("✅ Image generation model loaded successfully!")
                print(f"Model: {model_id}")
                print(f"Device: {self.device}")
                self.model_loaded = True
                self.model_id = model_id
                break
                
            except Exception as e:
                print(f"❌ Failed to load {model_id}: {str(e)[:100]}...")
                continue
        
        if not self.model_loaded:
            print("⚠️ Could not load any Stable Diffusion model.")
            print("Image generation will use placeholder images.")
    
    def generate_image(self, prompt, style="fantasy art, detailed, high quality", 
                      negative_prompt="blurry, low quality, distorted"):
        """
        Generate an image based on a text description.

        Args:
            prompt (str): Text description to generate image from
            style (str): Art style specification
            negative_prompt (str): What to avoid in the image

        Returns:
            PIL.Image: Generated image
        """
        if not self.model_loaded or not self.pipeline:
            print("⚠️ Image generator not available. Creating placeholder image...")
            return self.create_placeholder_image(prompt)

        try:
            # Enhance the prompt with style information
            enhanced_prompt = f"{prompt}, {style}"

            # Generate image with timeout handling
            with torch.no_grad():
                image = self.pipeline(
                    enhanced_prompt,
                    negative_prompt=negative_prompt,
                    num_inference_steps=20,  # Reduced for faster generation
                    guidance_scale=7.5,
                    height=512,
                    width=512
                ).images[0]

            return image

        except Exception as e:
            print(f"Error generating image: {str(e)[:100]}...")
            return self.create_placeholder_image(prompt)
    
    def create_placeholder_image(self, text, size=(512, 512)):
        """
        Create a simple placeholder image with text when image generation fails.

        Args:
            text (str): Text to display on placeholder
            size (tuple): Image size

        Returns:
            PIL.Image: Placeholder image
        """
        # Create a light blue background
        img = Image.new('RGB', size, color='lightblue')
        draw = ImageDraw.Draw(img)

        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()

        # Add placeholder text
        placeholder_text = "🖼️ IMAGE PLACEHOLDER\n\n" + text[:60] + "..."

        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), placeholder_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2

        # Draw text with shadow effect
        draw.text((x+2, y+2), placeholder_text, fill='gray', font=font, align='center')
        draw.text((x, y), placeholder_text, fill='black', font=font, align='center')

        return img
    
    def display_image_with_caption(self, image, caption, max_width=400):
        """
        Display an image with a caption.

        Args:
            image (PIL.Image): Image to display
            caption (str): Caption text
            max_width (int): Maximum display width
        """
        plt.figure(figsize=(max_width/100, max_width/100))
        plt.imshow(image)
        plt.axis('off')
        plt.title(caption, fontsize=12, wrap=True)
        plt.tight_layout()
        plt.show()
    
    def generate_story_images(self, scene_descriptions, art_style="fantasy art, detailed, high quality"):
        """
        Generate multiple images for story scenes.
        
        Args:
            scene_descriptions (list): List of scene descriptions
            art_style (str): Art style for all images
            
        Returns:
            list: List of generated images with metadata
        """
        images = []
        
        print(f"🎨 Generating {len(scene_descriptions)} image(s)...")
        
        for i, scene in enumerate(scene_descriptions):
            try:
                image = self.generate_image(scene, style=art_style)
                image_info = {
                    'scene': i + 1,
                    'description': scene,
                    'image': image
                }
                images.append(image_info)
                
                # Display image
                self.display_image_with_caption(
                    image,
                    f"Scene {i+1}: {scene[:50]}..."
                )
                
            except Exception as e:
                print(f"❌ Error generating image for scene {i+1}: {e}")
        
        return images