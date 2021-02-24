from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

import sys
from PIL import Image
from io import BytesIO


class Photo(models.Model):

    # Store in S3 bucket:
    # if user uploaded: freshi-app/media/photos/users/user_id/
    file_name = models.ImageField(
        upload_to='media/photos/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self):
        # Opening the uploaded image
        image = Image.open(self.file_name)

        # Save original aspect ratio.
        original_width, original_height = image.size
        aspect_ratio = float(original_width / original_height)

        # Use ratio to determine desired height/width in pixels.
        desired_height = 800
        desired_width = round(desired_height * aspect_ratio)

        # Resize the image
        image = image.resize((desired_width, desired_height))

        # for PNG images discarding the alpha channel and
        # fill it with some color.
        if image.mode in ('RGBA', 'LA'):
            background = Image.new(image.mode[:-1], image.size, '#fff')
            background.paste(image, image.split()[-1])
            image = background

        # after modifications, save it to new_image as jpg
        new_image = BytesIO()
        image.save(new_image, format='JPEG', quality=90)
        new_image.seek(0)

        # Get file name with appropriate file extension
        file_name = self.file_name.name.split('.')[0]
        file_path = f'{file_name}.jpg'

        # change the imagefield value to be the newley modifed image value
        self.file_name = InMemoryUploadedFile(
            new_image,
            'ImageField',
            file_path,
            'image/jpeg',
            sys.getsizeof(new_image),
            None)

        super(Photo, self).save()

    # Django admin display name
    def __str__(self):
        return str(self.file_name)

    class Meta:
        db_table = 'media_photos'
