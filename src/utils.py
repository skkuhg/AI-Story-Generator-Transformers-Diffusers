"""Utility functions for the story generator."""

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def configure_network_settings():
    """Configure network settings for better model download stability."""
    os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'  # 5 minutes
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Avoid warnings
    
    print("✅ Network configuration applied for stable downloads")


def configure_requests_retry():
    """Configure retry strategy for network requests."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_sample_prompts():
    """Get a list of sample story prompts."""
    return [
        "In a mystical forest where ancient trees whispered secrets",
        "On a distant planet where two moons cast silver light",
        "In a steampunk city where gears and magic coexisted",
        "Deep in the ocean where mermaids guarded ancient treasures",
        "In a floating castle above the clouds where wizards studied",
        "In a cyberpunk city where AI and humans coexist",
        "On a space station orbiting a dying star",
        "In a magical school hidden in the mountains",
        "During the last day on Earth before evacuation",
        "In a world where books come to life"
    ]


def display_usage_tips():
    """Display usage tips for the story generator."""
    tips = """
🎯 How to use the Story Generator:

1. **Enter a Story Prompt**: Write your story beginning in the text area
2. **Adjust Settings**:
   - Chapter Length: Controls how long each chapter will be
   - Creativity: Higher values = more creative/unpredictable stories
   - Art Style: Choose the visual style for generated images

3. **Generate Chapter**: Click to create the first chapter with images
4. **Continue Story**: Add more chapters to your story
5. **New Story**: Reset and start a completely new story

🎨 **Art Styles Available**:
- Fantasy Art: Magical, mystical scenes
- Realistic: Photographic quality images
- Anime Style: Colorful, animated look
- Watercolor: Artistic, painted effect
- Digital Art: Modern, vibrant style
- Oil Painting: Classical, detailed artwork

⚡ **Performance Tips**:
- Image generation may take 10-30 seconds per image
- Use shorter chapters for faster generation
- Lower creativity settings generate more coherent text
- GPU acceleration will significantly speed up image generation

🎭 **Story Ideas to Try**:
- "In a cyberpunk city where AI and humans coexist..."
- "On a space station orbiting a dying star..."
- "In a magical school hidden in the mountains..."
- "During the last day on Earth before evacuation..."
- "In a world where books come to live..."
"""
    print(tips)


def display_troubleshooting_info():
    """Display troubleshooting information."""
    info = """
🔧 Troubleshooting & Information

### System Requirements
- **Memory**: At least 8GB RAM (16GB recommended for image generation)
- **GPU**: CUDA-compatible GPU recommended for faster image generation
- **Storage**: ~5GB free space for model downloads

### Common Issues & Solutions

**1. Out of Memory Errors**
- Reduce chapter length or image resolution
- Enable model CPU offloading (already implemented)
- Use lower precision (float16 vs float32)

**2. Slow Generation**
- First run downloads models (~4GB), subsequent runs are faster
- GPU acceleration significantly improves speed
- Reduce number of inference steps for images (already optimized)

**3. Poor Quality Output**
- Adjust creativity/temperature settings
- Try different art styles
- Modify prompts to be more descriptive

### Model Information
- **Text Model**: GPT-2 Medium (~350M parameters)
- **Image Model**: Stable Diffusion v1.5 (~860M parameters)
- **Total Download**: ~4-5GB on first run

### Legal & Ethical Considerations
- Generated content is for personal/educational use
- Be mindful of content guidelines when sharing
- Models may reflect biases from training data
- Always review generated content before sharing
"""
    print(info)