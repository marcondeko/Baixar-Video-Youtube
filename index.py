from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont  # Adicionando a importação do QFont

from pytube import YouTube

class DownloadThread(QThread):
    download_completed = pyqtSignal()
    download_error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, url, filename, parent=None):
        super(DownloadThread, self).__init__(parent)
        self.url = url
        self.filename = filename

    def run(self):
        try:
            video = YouTube(self.url).streams.first()
            video.download(filename=self.filename)
            self.download_completed.emit()
        except Exception as e:
            self.download_error.emit(str(e))

        self.finished.emit()


class YoutubeDownloader(QMainWindow):
    def __init__(self):
        super(YoutubeDownloader, self).__init__()

        self.setWindowTitle("Baixador de Vídeos do YouTube")
        self.setFixedSize(780, 500)

        # Layout principal da janela
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Widgets de rótulo
        intro_label = QLabel("Baixador de Vídeos do YouTube")
        intro_font = QFont("Arial", 26)
        intro_font.setItalic(True)
        intro_font.setBold(True)
        intro_label.setFont(intro_font)
        intro_label.setStyleSheet("color: red")
        layout.addWidget(intro_label)

        url_label = QLabel("Digite o Link do YouTube")
        url_font = QFont("Sans Serif", 16)
        url_label.setFont(url_font)
        layout.addWidget(url_label)

        self.url_box = QLineEdit()
        url_box_font = QFont("Arial", 30)
        self.url_box.setFont(url_box_font)
        layout.addWidget(self.url_box)

        # Botão de download
        download_button = QPushButton("BAIXAR")
        download_button_font = QFont("Sans Serif", 25)
        download_button.setFont(download_button_font)
        download_button.clicked.connect(self.iniciar_download)
        layout.addWidget(download_button)

        self.status_bar = self.statusBar()

    def iniciar_download(self):
        url = self.url_box.text()
        if not url:
            QMessageBox.warning(self, "Erro", "Por favor, digite um link do YouTube.")
            return

        # Abrir o diálogo de arquivo
        filename, _ = QFileDialog.getSaveFileName(self, "Salvar Vídeo", "", "Arquivos MP4 (*.mp4);;Todos os Arquivos (*.*)")
        if not filename:
            return

        self.thread_download = DownloadThread(url, filename)
        self.thread_download.download_completed.connect(self.download_concluido)
        self.thread_download.download_error.connect(self.erro_download)
        self.thread_download.finished.connect(self.thread_download.quit)
        self.thread_download.start()
        self.status_bar.showMessage("Baixando...")

    def download_concluido(self):
        self.status_bar.clearMessage()
        QMessageBox.information(self, "Sucesso", "Download concluído!")

    def erro_download(self, error):
        self.status_bar.clearMessage()
        QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {error}")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    janela = YoutubeDownloader()
    janela.show()
    sys.exit(app.exec_())
