import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloudinary_url = os.getenv('CLOUDINARY_URL')
)

def upload_place_image(file_path):
    """
    Uploads a place image to Cloudinary and returns the secure URL.
    """
    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder="hbnb_places",
            use_filename=True,
            unique_filename=True
        )
        return response.get('secure_url')
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None
    