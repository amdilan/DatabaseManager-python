from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle, QApplication
from PyQt6.QtGui import QTextDocument, QPalette
from PyQt6.QtCore import QRect, QSize, Qt, QSizeF

class HTMLDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Get the style options
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        # Get the style
        style = options.widget.style() if options.widget else QApplication.style()
        
        # Create a text document with HTML content
        doc = QTextDocument()
        doc.setHtml(options.text)
        
        # Draw the item without text (we'll handle that separately)
        options.text = ""
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, options, painter)
        
        painter.save()
        
        # Calculate the text rectangle
        text_rect = style.subElementRect(QStyle.SubElement.SE_ItemViewItemText, options, options.widget)
        margin = style.pixelMetric(QStyle.PixelMetric.PM_FocusFrameHMargin, None, options.widget) + 1
        text_rect.adjust(margin, 0, -margin, 0)
        
        # Draw the HTML content
        painter.translate(text_rect.topLeft())
        doc.setPageSize(QSizeF(text_rect.size()))  # Use QSizeF for document sizing
        doc.drawContents(painter)
        
        painter.restore()
    
    def sizeHint(self, option, index):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        
        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        
        # Convert float dimensions to integers for QSize
        width = int(doc.idealWidth())
        height = int(doc.size().height())
        
        return QSize(width, height)