
display_name_prefix = 'HZK Pixel'
unique_name_prefix = 'HZK-Pixel'
output_name_prefix = 'hzk-pixel'
style_name = 'Regular'
version = '1.2.0'
description = 'HZK pixel font.'
vendor_url = 'https://hzk-pixel-font.takwolf.com'


class VerticalMetrics:
    def __init__(self, ascent, descent, x_height, cap_height):
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height


class FontConfig:
    def __init__(self, px, box_origin_y_px, x_height_px, cap_height_px, source_names, px_units=100):
        self.px = px
        self.box_origin_y_px = box_origin_y_px
        self.x_height_px = x_height_px
        self.cap_height_px = cap_height_px
        self.source_names = source_names
        self.px_units = px_units

        self.display_name = f'{display_name_prefix} {px}px'
        self.unique_name = f'{unique_name_prefix}-{px}px'
        self.output_name = f'{output_name_prefix}-{px}px'
        self.preview_image_file_name = f'preview-{px}px.png'

    def get_name_strings(self):
        return {
            'familyName': self.display_name,
            'styleName': style_name,
            'uniqueFontIdentifier': f'{self.unique_name}-{style_name};{version}',
            'fullName': self.display_name,
            'version': version,
            'psName': f'{self.unique_name}-{style_name}',
            'description': description,
            'vendorURL': vendor_url,
        }

    def get_units_per_em(self):
        return self.px * self.px_units

    def get_box_origin_y(self):
        return self.box_origin_y_px * self.px_units

    def get_vertical_metrics(self):
        ascent = self.box_origin_y_px * self.px_units
        descent = (self.box_origin_y_px - self.px) * self.px_units
        x_height = self.x_height_px * self.px_units
        cap_height = self.cap_height_px * self.px_units
        return VerticalMetrics(ascent, descent, x_height, cap_height)
