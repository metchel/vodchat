from django.test import TestCase
from videos.models import Video

# Create your tests here.
class VideoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Video.objects.create(title='A video', description='This is a video')

    def test_title_max_length(self):
        video = Video.objects.get(title='A video')
        max_length = video._meta.get_field('title').max_length
        self.assertEquals(max_length, 256)

    def test_description_max_length(self):
        video = Video.objects.get(title='A video')
        max_length = video._meta.get_field('description').max_length
        self.assertEquals(max_length, 4096)

    def test_date_created_editable_false(self):
        video = Video.objects.get(title='A video')
        is_editable = video._meta.get_field('date_created').editable
        self.assertFalse(is_editable)

    def test_videofile_upload_to(self):
        video = Video.objects.get(title='A video')
        upload = video._meta.get_field('videofile').upload_to
        self.assertEquals(upload, 'videos/')

    def test_thumbnailfile_upload_to(self):
        video = Video.objects.get(title='A video')
        upload = video._meta.get_field('thumbnailfile').upload_to
        self.assertEquals(upload, 'thumbnails/')
