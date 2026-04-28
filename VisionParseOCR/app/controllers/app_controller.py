from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

import wx, io, os

from app.core.commands import *
from app.utils.hash_utils import generate_hash
from app.ui.drag_drop import FileDropTarget
from app.core.entities.image_entity import ImageEntity


class AppController:
    def __init__(self, frame, pdf, ocr):
        self.frame = frame
        self.pdf = pdf
        self.ocr = ocr

        # self.lst_images = []
        # self.images = []
        # self.mode = None  # "pdf" ou "dir"

        # ==========================================
        # 🏆 ESTADO PROFISSIONAL ORGANIZADO
        # ==========================================
        self.pdf_images = []         # lista de ImageEntity (PDF)
        self.directory_files = []    # lista de strings (nomes arquivos)
        self.current_items = []      # lista atualmente exibida
        self.current_mode = None     # "pdf" | "dir"

        self.path = None
        self.directory = None

        self.commands = {
            "open": OpenFileCommand(self),
            "folder": OpenDirectoryCommand(self),
            "save": SaveOCRResultCommand(self),
            "export": SaveImagesCommand(self),
            "exit": ExitCommand(self),
            "ocr": OCRCommand(self),
            "clear": ClearTextCommand(self),
            "rotate_left": RotateLeftCommand(self),
            "rotate_right": RotateRightCommand(self),
            "zoom_in": ZoomInCommand(self),
            "zoom_out": ZoomOutCommand(self),
            "about": AboutCommand(),
            "commands": HelpCommand()
        }

        self.frame.menu.bind(self.commands)

        self.frame.thumbnail.callback = self.on_thumbnail
        self.frame.image_panel.on_selection = self.on_selection
        self.frame.image_panel.on_image_change = self.on_thumbnail

        self.frame.on_thumb = self.on_thumbnail

        drop = FileDropTarget(self.on_drop)
        self.frame.SetDropTarget(drop)

    # ==========================================
    # 📄 LOAD PDF
    # ==========================================
    def load_pdf(self, path):
        self.current_mode = "pdf"
        self.path = path

        self.pdf_images.clear()
        self.directory_files.clear()
        self.current_items.clear()

        # Zera painel de thumnails
        self._reset_thumbnails()

        self.frame.set_status_temp("Processando imagens do PDF...")
        extracted = self.pdf.extract_images(path)


        for i, img in enumerate(extracted, start=1):
            if "bytes" not in img:
                continue

            if not isinstance(img["bytes"], (bytes, bytearray)):
                continue

            entity = ImageEntity(
                name=f"img_{i:03d}",
                data=img,
                hash_id=generate_hash(img["bytes"])
            )

            self.pdf_images.append(entity)

        self.current_items = self.pdf_images

        if not self.pdf_images:
            logger.error("Nenhuma imagem válida encontrada no PDF")
            return

        # 🔥 thumbnails (PDF)
        self.frame.thumbnail.load_images(path, self.pdf_images)
        self.frame.thumbnail.select(0)

        # 🔥 imagem inicial (PDF)
        img = self._entity_to_wx_image(self.pdf_images[0])
        self.frame.image_panel.load_pdf_images(self.pdf_images)

        self.frame.set_status_temp("")

    # ==========================================
    # 📂 LOAD DIRECTORY
    # ==========================================
    def load_directory(self, directory):
        self.current_mode = "dir"
        self.directory = directory

        self.pdf_images.clear()
        self.directory_files.clear()
        self.current_items.clear()

        self.directory_files = [
            f for f in os.listdir(directory)
            if f.lower().endswith(("png", "jpg", "jpeg", "bmp"))
        ]

        self.current_items = self.directory_files

        self.frame.image_panel.load_directory(directory)
        self.frame.thumbnail.load_images(directory, self.directory_files)

        if self.directory_files:
            self.frame.thumbnail.select(0)

    # ==========================================
    # 📄 SAVE IMAGES FROM PDF
    # ==========================================
    def save_images_pdf(self, output_dir):
        if self.current_mode != "pdf":
            wx.MessageBox("Exportação disponível apenas para PDFs.")
            return

        self.frame.set_status_temp("Salvando imagens...")

        self.pdf.save_images(self.pdf_images, output_dir)

        self.frame.set_status_temp("Exportação concluída")

    # ==========================================
    # 🖼️ CLICK THUMB
    # ==========================================
    def on_thumbnail(self, index):

        if index < 0 or index >= len(self.current_items):
            return

        self.frame.image_panel.imageIndx = index
        self.frame.image_panel.scale = 1.0
        self.frame.image_panel.rotation = 0

        # PDF MODE
        if self.current_mode == "pdf":
            entity = self.pdf_images[index]

            img = self._entity_to_wx_image(entity)

            if img:
                self.frame.image_panel.load_current_image(img)

        # DIRECTORY MODE
        elif self.current_mode == "dir":
            self.frame.image_panel.load_current_image()

        self.frame.thumbnail.select(index)

    # ==========================================
    # 🧲 DRAG & DROP
    # ==========================================
    def on_drop(self, files):

        if len(files) == 1 and os.path.isdir(files[0]):
            self.load_directory(files[0])
            return

        # Arquivos de imagem soltos
        self.current_mode = "dir"

        self.directory = os.path.dirname(files[0])

        self.directory_files = [
            os.path.basename(f)
            for f in files
            if f.lower().endswith(("png", "jpg", "jpeg", "bmp"))
        ]

        self.current_items = self.directory_files

        self.frame.image_panel.directory = self.directory
        self.frame.image_panel.imageList = self.directory_files
        self.frame.image_panel.imageIndx = 0

        self.frame.image_panel.load_current_image()

        self.frame.thumbnail.load_images(
            self.directory,
            self.directory_files
        )

        if self.directory_files:
            self.frame.thumbnail.select(0)

    # ==========================================
    # 🔍 OCR
    # ==========================================
    def run_ocr(self):
        img = self.frame.image_panel.original_image

        if img is None:
            return

        text = self.ocr.extract_text(
            img,
            rotation=self.frame.image_panel.rotation
        )

        wx.CallAfter(self.frame.txt_output.SetValue, text)

    # ==========================================
    # 🔍 OCR REGIÃO
    # ==========================================
    def on_selection(self, rect):
        img = self.frame.image_panel.original_image

        if img is None:
            return

        text = self.ocr.extract_region(
            img,
            rect,
            rotation=self.frame.image_panel.rotation
        )

        self.frame.txt_output.SetValue(text)

    # ==========================================
    # 🔥 HELPERS CENTRAL
    # ==========================================
    def _entity_to_wx_image(self, entity):
        if not entity or not entity.bytes:
            return None

        try:
            return wx.Image(
                io.BytesIO(entity.bytes),
                wx.BITMAP_TYPE_ANY
            )
        except Exception as e:
            logger.exception("Erro inesperado ao interpretar imagem")
            logger.info(f"[ERRO] Falha ao converter imagem: {e}")
            return None

    def _reset_thumbnails(self):
        self.frame.thumbnail.sizer.Clear(True)
        self.frame.thumbnail.thumbs.clear()
        self.frame.thumbnail.selected = None
        self.frame.thumbnail.cache.clear()