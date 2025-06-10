from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize


def ScaleAndCropCenter(pixmap: QPixmap, target_size: QSize) -> QPixmap:
    target_width = target_size.width()
    target_height = target_size.height()

    # Scale the pixmap preserving aspect ratio, covering the target size (Zoom then crop)
    scaled_pixmap = pixmap.scaled(
        target_size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
    )

    # Calculate cropping rectangle (centered)
    x_offset = (scaled_pixmap.width() - target_width) // 2
    y_offset = (scaled_pixmap.height() - target_height) // 2

    cropped = scaled_pixmap.copy(x_offset, y_offset, target_width, target_height)
    return cropped