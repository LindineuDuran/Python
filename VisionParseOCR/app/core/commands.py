from app.infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
import wx
import threading

class Command:
    def execute(self):
        pass

class OpenFileCommand(Command):
    def __init__(self, controller):
        self.controller = controller
        self.images = []

    def execute(self):
        self.controller.frame.set_status_temp("Abrir um arquivo PDF")

        frame = self.controller.frame

        with wx.FileDialog(frame, "Selecionar PDF", wildcard="*.pdf") as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return  # ✅ sai cedo (clean code)

            path = dlg.GetPath()
            self.controller.frame.set_status(f"\n📄 Processando PDF: {path}", 1)

        self.controller.load_pdf(path)

class OpenDirectoryCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        dlg = wx.DirDialog(self.controller.frame, "Escolha pasta")
        
        if dlg.ShowModal() == wx.ID_OK:
            self.controller.frame.set_status(f"\n📄 Pasta Escolhida: {dlg.GetPath()}", 1)
            self.controller.load_directory(dlg.GetPath())
            
class SaveOCRResultCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Salvar resultado OCR")

        """Pega texto obtido"""
        value = self.controller.frame.txt_output.GetValue()

        """Browse for directory"""
        fdlg = wx.FileDialog(None, "Entre com o caminho para o arquivo de resultado", "", "", "text files(*.txt)|*.*", wx.FD_SAVE)

        if fdlg.ShowModal() == wx.ID_OK:
            self.save_path = fdlg.GetPath() + ".txt"

            ocrFile = open(self.save_path, 'w', encoding="utf-8")
            ocrFile.write(value+'\r\n')
            ocrFile.close()

        fdlg.Destroy()

class SaveImagesCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Salvar imagens do PDF")
        dlg = wx.DirDialog(self.controller.frame, "Escolha pasta")
        
        if dlg.ShowModal() == wx.ID_OK:
            self.controller.frame.set_status(f"\n📄 Pasta Escolhida: {dlg.GetPath()}", 1)
            self.controller.save_images_pdf(dlg.GetPath())

class ExitCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        """Close the frame, terminating the application."""
        self.controller.frame.set_status_temp("Encerrar o aplicativo")
        self.controller.frame.Close(True)


class OCRCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Obtendo o texto...")

        threading.Thread(target=self.controller.run_ocr).start()


class ClearTextCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Limpando a caixa de textos...")
        self.controller.frame.txt_output.SetValue("")

class RotateRightCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Rodando imagem para a direita...")
        self.controller.frame.image_panel.rotate_right()


class RotateLeftCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Rodando imagem para a esquerda...")
        self.controller.frame.image_panel.rotate_left()

class ZoomInCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Zoon in...")
        self.controller.frame.image_panel.zoom_in()


class ZoomOutCommand(Command):
    def __init__(self, controller):
        self.controller = controller

    def execute(self):
        self.controller.frame.set_status_temp("Zoon out...")
        self.controller.frame.image_panel.zoom_out()


class AboutCommand(Command):
    def execute(self):
        wx.MessageBox("""VisionParse OCR

Desenvolvido por Lindineu Duran
Contato: lduran355@gmail.com

VisionParse é uma solução avançada de OCR (Optical Character Recognition) 
projetada para transformar imagens e documentos PDF em dados estruturados.

Principais recursos:
• Visualização de imagens e PDFs
• Navegação com zoom e panorâmica
• Rotação e manipulação de imagens
• Extração de texto com OCR
• Preparação de dados para processamento posterior

Versão: 1.0""", "Sobre o VisionParse")
        
class HelpCommand(Command):
    def execute(self):
        wx.MessageBox("""VisionParse OCR — Comandos

📂 Arquivos
Ctrl+O  → Abrir PDF
Ctrl+F  → Abrir pasta de imagens
Ctrl+S  → Salvar texto extraído
Ctrl+I  → Exportar imagens do PDF
Ctrl+Q  → Sair

🧠 OCR
Ctrl+G  → Executar reconhecimento de texto
Ctrl+L  → Limpar texto extraído

🖼️ Visualização
Ctrl++  → Ampliar imagem
Ctrl+-  → Reduzir imagem
Ctrl+E  → Girar para a esquerda
Ctrl+D  → Girar para a direita

ℹ️ Informações
Ctrl+A  → Sobre o VisionParse
Ctrl+K  → Exibir comandos

VisionParse transforma conteúdo visual em informação estruturada.""", "Comandos")