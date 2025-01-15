import sys
import random
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QSpinBox)
import os
import textwrap

def wrap_text(text, max_width, font_size):
    chars_per_line = max_width // (font_size // 2)
    return textwrap.wrap(text, width=chars_per_line-5)

def generate_svg_grid(title, strings, grid_width, grid_height, square_size, spacing, output_file="grid.svg", font_size=None):
    spacing = spacing-40
    title_height = square_size  
    border_padding = square_size // 10  
    svg_elements = []

    svg_width = grid_width * square_size + (grid_width - 1) * spacing + 2 * border_padding
    svg_height = grid_height * square_size + (grid_height - 1) * spacing + title_height + 2 * border_padding

    svg_elements.append(f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">')

    # outer rim
    svg_elements.append(f'<rect width="{svg_width - 4}" height="{svg_height - 4}" x="2" y="2" fill="none" stroke="black" stroke-width="4" />')

    # Dynamic bingo box for title
    svg_elements.append(f'''
    <rect width="{svg_width - 2 * border_padding}" height="{title_height}" x="{border_padding}" y="{border_padding}" fill="none" stroke="black" stroke-width="4" />
    <text x="{svg_width // 2}" y="{border_padding + title_height // 2}" font-size="{square_size // 2}" font-family="Courier New, monospace" fill="black" text-anchor="middle" dominant-baseline="middle">
        {title}
    </text>
    ''')
    
    for i in range(grid_height):
        for j in range(grid_width):
            index = i * grid_width + j
            text = strings[index] if index < len(strings) else ""
            x_offset = j * (square_size + spacing) + border_padding
            y_offset = i * (square_size + spacing) + title_height + border_padding  # Adjust for title and padding
            
            # Set font size or adjust dynamically
            max_font_size = square_size // 5
            adjusted_font_size = font_size if font_size else max(max_font_size - (len(text) * 2), 20)
            wrapped_lines = wrap_text(text, square_size - 50, adjusted_font_size)
            
            text_elements = ""
            total_text_height = len(wrapped_lines) * adjusted_font_size
            start_y = (square_size // 2) - (total_text_height // 2) + adjusted_font_size // 2

            for line_num, line in enumerate(wrapped_lines):
                y_line_offset = start_y + (line_num * adjusted_font_size)
                text_elements += f'<text x="{(square_size // 2)}" y="{y_line_offset}" font-size="{adjusted_font_size}" font-family="Courier New, monospace" fill="black" text-anchor="middle" dominant-baseline="middle">{line}</text>'

            square = f'''
            <g transform="translate({x_offset}, {y_offset})">
                <rect width="{square_size - 50}" height="{square_size - 50}" x="25" y="25" fill="none" stroke="black" stroke-width="4" />
                {text_elements}
            </g>'''
            svg_elements.append(square)

    svg_elements.append('</svg>')

    # Write to the output file
    with open(output_file, 'w') as f:
        f.write("\n".join(svg_elements))

    print(f"SVG grid saved to {os.path.abspath(output_file)}")



class SVGGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sebs Bingo Generator')
        self.setWindowIcon(QIcon("./icon.ico")) 

        self.title = QLabel("Title")
        self.title_input = QLineEdit("Bingo")

        self.label_input = QLabel('Enter text (comma-separated):')
        self.text_input =  QTextEdit()

        self.label_grid_x = QLabel('Grid Width:')
        self.grid_x_input = QSpinBox()
        self.grid_x_input.setValue(5)
        self.grid_x_input.setMinimum(1)

        self.label_grid_y = QLabel('Grid Height:')
        self.grid_y_input = QSpinBox()
        self.grid_y_input.setValue(5)
        self.grid_y_input.setMinimum(1)

        self.label_square_size = QLabel('Square Size:')
        self.square_size_input = QSpinBox(maximum=500)
        self.square_size_input.setValue(200)

        self.label_spacing = QLabel('Spacing:')
        self.spacing_input = QSpinBox()
        self.spacing_input.setValue(10)

        self.font_size = QLabel("Font Size:")
        self.font_size_input = QSpinBox()
        self.font_size_input.setValue(20)
        
        self.shuffle_button = QPushButton('Shuffle List')
        self.shuffle_button.clicked.connect(self.shuffle_list)

        self.generate_button = QPushButton('Generate SVG')
        self.generate_button.clicked.connect(self.generate_svg)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.title_input)
        layout.addWidget(self.label_input)
        layout.addWidget(self.text_input)

        grid_layout = QHBoxLayout()
        grid_layout.addWidget(self.label_grid_x)
        grid_layout.addWidget(self.grid_x_input)
        grid_layout.addWidget(self.label_grid_y)
        grid_layout.addWidget(self.grid_y_input)
        layout.addLayout(grid_layout)

        layout.addWidget(self.label_square_size)
        layout.addWidget(self.square_size_input)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.spacing_input)
        layout.addWidget(self.font_size)
        layout.addWidget(self.font_size_input)
        layout.addWidget(self.shuffle_button)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def shuffle_list(self):
        items = self.text_input.toPlainText().replace("\r","").replace("\n","").split(',')
        random.shuffle(items)
        self.text_input.setPlainText(','.join(items))

    def generate_svg(self):
        title = self.title_input.text()
        items = self.text_input.toPlainText().replace("\n","").replace("\r","").split(',')
        grid_x = self.grid_x_input.value()
        grid_y = self.grid_y_input.value()
        square_size = self.square_size_input.value()
        spacing = self.spacing_input.value()
        fontsize = self.font_size_input.value()
        if fontsize == 0:
            fontsize = None
        file_name, _ = QFileDialog.getSaveFileName(self, "Save SVG", "", "SVG Files (*.svg)")
        if file_name:
            generate_svg_grid(title,items, grid_x, grid_y, square_size, spacing, file_name, fontsize)
            QMessageBox.information(self, "Success", f"SVG saved to {file_name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SVGGeneratorApp()
    window.show()
    sys.exit(app.exec_())
