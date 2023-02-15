import base64
from unittest import TestCase

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from rest_framework.exceptions import ValidationError

from utils.helpers import validate_image

class ImageValidateTest(TestCase):
    def setUp(self):
        super().setUp()
        image_64 = """
            /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8MlBGQUZaVVBfeMiCeG5uePWvuZHI////////
            ////////////////////////////////////////////2wBDAVVaWnhpeOuCguv/////////////
            ////////////////////////////////////////////////////////////wAARCABkAGQDASIA
            AhEBAxEB/8QAGQAAAwEBAQAAAAAAAAAAAAAAAAIDBAEF/8QAKRAAAgIBAwMEAgIDAAAAAAAAAAEC
            EQMSITEEIkETUWFxIzKBkUKhsf/EABcBAQEBAQAAAAAAAAAAAAAAAAABAgP/xAAWEQEBAQAAAAAA
            AAAAAAAAAAAAARH/2gAMAwEAAhEDEQA/AGUPg7oGs7ZULopE5ZIxdLdjZslRaRnivL5Cmnl/gm5v
            ywkt9ziVkHU7G+xa8o6mA0Xp3RaElL7IM4m1umFa1F2DVnMWXXHflD2VkmlewD2AC+m/dh6bS5LH
            JNJW+AMWR1t7ixYZJapuX+hFuyNKVdsVvktCPayWSNEMJYX5QrAo7YXRz6BMC2B/kRs0I8+L0u0e
            hjkpwUl5ESuaAHAqOkOpnpgXMnWcxQIz+LZfFipKT4ItcL3ZulUY78IzWom8iT4FdSOZM0V/i9/J
            2HdwFLLHERxivBaSaJucYcpsCUoeUhGalNS2qiebHStBETb0su2vdWYTV0j3KlawACsgzdW12+5p
            MnUJuYWIreSfyejVo86HKR6EHcVZltPJj1Phf0NDHpQzaRz1FGre7ICcUSljvwmvod5It03R1MBY
            wr2Ezr8bKtksruLAxlennpyb8PYSaoIq2/o0j0gFxyuCfwBWTEcsd7Ks5PeNAZcsK7lyWwz147fK
            dEc077VwhemyaZuL4l/0zWo1PcJaEtzkvgl6T1W5/wBkaOtF8jPbgjKG37JfQ0U1y7ApZHPLTDbm
            ylmXPPVOvCKlI5OTtspjXciSL41cU14Ky1RTUaAIzpUwKhyeRvheSgkwSMk1TaRPTTL5qjNJctbk
            qtkaWw5dVRnz4fuWcU0ZarMvgvboyruhIG0kI5MXd8hQ3ZCa72aUhZQTasIhTRXp5pScX5ON1Okv
            J2UO7bk0y1LgCKySpbWA0xqS8kpc/wAgBK1GXM362QZJbAAqQ01+UfwAEaKwQAA6Ff7MAASSXNb2
            LVNbv3ADbm7PaWwABFf/2Q==
        """

        image_data = base64.b64decode(image_64)
        image_file = ContentFile(image_data)
        self.image = UploadedFile(
            file = image_file,
            name = 'image.jpg',
            content_type = 'image/jpg',
            size=image_file.size
        )
        


    def test_validate_image_success(self):
        self.assertIsNone(validate_image(self.image, 1024))

    def test_validate_image_fail(self):
        with self.assertRaises(ValidationError) as img_err:
            validate_image(self.image, 100)
        self.assertEqual(
            'File too large max size is 0MB',
            img_err.exception.detail[-1]
        )
