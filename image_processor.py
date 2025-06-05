import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from typing import Optional, Tuple

class ImageProcessor:
    """Class for preprocessing cow images for disease detection"""
    
    def __init__(self):
        self.target_size = (224, 224)  # Standard input size for most ML models
        self.max_file_size_mb = 10
    
    def preprocess_image(self, image: Image.Image) -> Optional[np.ndarray]:
        """
        Preprocess uploaded image for ML model prediction
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image as numpy array or None if processing fails
        """
        try:
            # Check if image is valid
            if not self._validate_image(image):
                return None
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image quality
            enhanced_image = self._enhance_image(image)
            
            # Resize image
            resized_image = self._resize_image(enhanced_image)
            
            # Normalize pixel values
            normalized_image = self._normalize_image(resized_image)
            
            # Convert to numpy array
            image_array = np.array(normalized_image)
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None
    
    def _validate_image(self, image: Image.Image) -> bool:
        """Validate if the image meets basic requirements"""
        try:
            # Check image dimensions
            width, height = image.size
            if width < 50 or height < 50:
                return False
            
            # Check if image is too large
            if width > 4000 or height > 4000:
                return False
            
            return True
            
        except Exception:
            return False
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better disease detection"""
        try:
            # Enhance contrast
            contrast_enhancer = ImageEnhance.Contrast(image)
            image = contrast_enhancer.enhance(1.2)
            
            # Enhance sharpness
            sharpness_enhancer = ImageEnhance.Sharpness(image)
            image = sharpness_enhancer.enhance(1.1)
            
            # Reduce noise with a slight blur
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
            
            return image
            
        except Exception:
            return image
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """Resize image to target size while maintaining aspect ratio"""
        try:
            # Calculate aspect ratio
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            
            # Determine new dimensions
            if aspect_ratio > 1:  # Landscape
                new_width = self.target_size[0]
                new_height = int(self.target_size[0] / aspect_ratio)
            else:  # Portrait or square
                new_height = self.target_size[1]
                new_width = int(self.target_size[1] * aspect_ratio)
            
            # Resize image
            resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create new image with target size and paste resized image
            final_image = Image.new('RGB', self.target_size, (128, 128, 128))
            
            # Calculate position to center the image
            x_offset = (self.target_size[0] - new_width) // 2
            y_offset = (self.target_size[1] - new_height) // 2
            
            final_image.paste(resized, (x_offset, y_offset))
            
            return final_image
            
        except Exception:
            return image.resize(self.target_size, Image.Resampling.LANCZOS)
    
    def _normalize_image(self, image: Image.Image) -> Image.Image:
        """Normalize image pixel values"""
        try:
            # Convert to numpy array for processing
            img_array = np.array(image, dtype=np.float32)
            
            # Normalize to 0-1 range
            img_array = img_array / 255.0
            
            # Apply standard normalization (ImageNet standards)
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            
            img_array = (img_array - mean) / std
            
            # Convert back to 0-255 range for PIL
            img_array = ((img_array * std + mean) * 255).astype(np.uint8)
            
            return Image.fromarray(img_array)
            
        except Exception:
            return image
    
    def extract_features(self, image: Image.Image) -> dict:
        """Extract basic features from the image for analysis"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            
            features = {
                'brightness': np.mean(img_array),
                'contrast': np.std(img_array),
                'size': image.size,
                'mode': image.mode
            }
            
            # Color analysis
            if len(img_array.shape) == 3:
                features['red_mean'] = np.mean(img_array[:, :, 0])
                features['green_mean'] = np.mean(img_array[:, :, 1])
                features['blue_mean'] = np.mean(img_array[:, :, 2])
            
            return features
            
        except Exception as e:
            return {'error': str(e)}
    
    def detect_image_quality(self, image: Image.Image) -> dict:
        """Assess image quality for diagnosis accuracy"""
        try:
            img_array = np.array(image)
            
            # Convert to grayscale for analysis
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Calculate blur level using Laplacian variance
            blur_level = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = np.std(gray)
            
            quality_assessment = {
                'blur_level': blur_level,
                'is_blurry': blur_level < 100,
                'brightness': brightness,
                'is_too_dark': brightness < 50,
                'is_too_bright': brightness > 200,
                'contrast': contrast,
                'is_low_contrast': contrast < 30,
                'overall_quality': 'good'
            }
            
            # Determine overall quality
            issues = []
            if quality_assessment['is_blurry']:
                issues.append('blurry')
            if quality_assessment['is_too_dark']:
                issues.append('too dark')
            if quality_assessment['is_too_bright']:
                issues.append('too bright')
            if quality_assessment['is_low_contrast']:
                issues.append('low contrast')
            
            if len(issues) > 2:
                quality_assessment['overall_quality'] = 'poor'
            elif len(issues) > 0:
                quality_assessment['overall_quality'] = 'fair'
            
            quality_assessment['issues'] = issues
            
            return quality_assessment
            
        except Exception as e:
            return {'error': str(e), 'overall_quality': 'unknown'}
