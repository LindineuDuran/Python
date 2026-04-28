import wx, io, os
from core.commands import *
from utils.hash_utils import generate_hash
from ui.drag_drop import FileDropTarget
from core.entities.image_entity import ImageEntity


class AppController:
    def __init__(self, frame, pdf, ocr):
        self.frame = frame
        self.pdf = pdf
        self.ocr = ocr

        self.lst_images = []
        self.images = []
        self.mode = None  # "pdf" ou "dir"

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
        self.mode = "pdf"
        self.path = path
        self.images = []  # 🔥 LIMPA diretório

        # Zera painel de thumnails
        self.frame.thumbnail.sizer.Clear(True)
        self.frame.thumbnail.thumbs.clear()
        self.frame.thumbnail.selected = None
        self.frame.thumbnail.cache.clear()  # 🔥 MUITO IMPORTANTE

        self.frame.set_status_temp("Processando imagens do PDF...")
        self.images = self.pdf.extract_images(self.path)
        self.lst_images = []


        for i, img in enumerate(self.images):
            if "bytes" not in img:
                continue

            if not isinstance(img.get("bytes"), (bytes, bytearray)):
                continue

            entity = ImageEntity(
                name=f"img_{i:03d}",
                data=img,
                hash_id=generate_hash(img["bytes"])
            )

            self.lst_images.append(entity)

        if not self.lst_images:
            print("[ERRO] Nenhuma imagem válida encontrada no PDF")
            return

        # 🔥 thumbnails (PDF)
        self.frame.thumbnail.load_images(self.path, self.lst_images)
        self.frame.thumbnail.select(0)

        # 🔥 imagem inicial (PDF)
        img = self._entity_to_wx_image(self.lst_images[0])
        self.frame.image_panel.load_pdf_images(self.lst_images)

        self.frame.set_status_temp("")

    # ==========================================
    # 📂 LOAD DIRECTORY
    # ==========================================
    def load_directory(self, directory):
        self.mode = "dir"
        self.directory = directory
        self.lst_images = []  # 🔥 LIMPA PDF

        self.images = [
            f for f in os.listdir(directory)
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp'))
        ]

        self.frame.image_panel.load_directory(directory)
        self.frame.thumbnail.load_images(directory, self.images)

        if self.images:
            self.frame.thumbnail.select(0)

    # ==========================================
    # 📄 SAVE IMAGES FROM PDF
    # ==========================================
    def save_images_pdf(self, path):
        self.path = path

        self.frame.set_status_temp("Salvando imagens do PDF...")
        self.frame.set_status(f"\n💾 Salvando imagens em: {self.path}", 1)
        self.images = self.frame.image_panel.imageList
        self.pdf.save_images(self.images, self.path)
        self.frame.set_status("", 1)

    # ==========================================
    # 🖼️ CLICK THUMB
    # ==========================================
    def on_thumbnail(self, index):
        # 🔥 caso seja PDF
        if self.mode == "pdf":
            if index >= len(self.lst_images):
                return

            self.frame.image_panel.imageIndx = index
            self.frame.image_panel.scale = 1.0
            self.frame.image_panel.rotation = 0

            img = self._entity_to_wx_image(self.lst_images[index])
            self.frame.image_panel.load_current_image(img)

        # 🔥 caso seja diretório
        elif self.mode == "dir":
            if index >= len(self.images):
                return

            self.frame.image_panel.imageIndx = index
            self.frame.image_panel.scale = 1.0
            self.frame.image_panel.rotation = 0

            self.frame.image_panel.load_current_image()

        self.frame.thumbnail.select(index)

    # ==========================================
    # 🧲 DRAG & DROP
    # ==========================================
    def on_drop(self, files):
        if len(files) == 1 and os.path.isdir(files[0]):
            self.load_directory(files[0])
        else:
            self.directory = os.path.dirname(files[0])
            self.images = [os.path.basename(f) for f in files]

            self.frame.image_panel.imageList = self.images
            self.frame.image_panel.directory = self.directory
            self.frame.image_panel.imageIndx = 0

            self.frame.image_panel.scale = 1.0
            self.frame.image_panel.rotation = 0

            self.frame.image_panel.load_current_image()
            self.frame.thumbnail.load_images(self.directory, self.images)

            if self.images:
                self.frame.thumbnail.select(0)

    # ==========================================
    # 🔍 OCR
    # ==========================================
    def run_ocr(self):
        img = self.frame.image_panel.original_image

        if img is None:
            return

        text = self.frame.txt_output.GetValue()
        text += self.ocr.extract_text(
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
            print("imagem está vazia!")
            return

        text = self.frame.txt_output.GetValue()
        text += self.ocr.extract_region(
            img,
            rect,
            rotation=self.frame.image_panel.rotation
        )

        self.frame.txt_output.SetValue(text)

    # ==========================================
    # 🔥 HELPER CENTRAL
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
            print(f"[ERRO] Falha ao converter imagem: {e}")
            return None