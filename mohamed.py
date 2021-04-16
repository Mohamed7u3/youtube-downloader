from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import urllib.request
import pafy
#import humanize
from main import Ui_MainWindow

import os
from os import path
from pytube import Playlist,YouTube
import webbrowser
#import icon_rc
#ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow , Ui_MainWindow):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.Handel_UI()


    def Handel_UI(self):
        self.setWindowTitle('PyDownloader')
        self.setFixedSize(1004,643)
    def Handel_Buttons(self):
        ## handel all buttons in the app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)

        self.pushButton_27.clicked.connect(self.Get_Video_Data)
        self.pushButton_22.clicked.connect(self.Download_Video)
        self.pushButton_21.clicked.connect(self.Save_Browse)

        self.pushButton_29.clicked.connect(self.Playlist_Download)
        self.pushButton_28.clicked.connect(self.Playlist_Save_Browse)

        self.pushButton_6.clicked.connect(self.Open_Home)
        self.pushButton_5.clicked.connect(self.Open_Download)
        self.pushButton_3.clicked.connect(self.Open_Youtube)
        self.pushButton_4.clicked.connect(self.About_Me)


    def Handel_Progress(self , blocknum , blocksize , totalsize):
        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0 :
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()


    def Handel_Browse(self):
        ## enable browseing to our os , pick save location
        save_location = QFileDialog.getSaveFileName(self , caption="Save as" , directory="." , filter="All Files(*.*)")
        print(save_location)
        self.lineEdit_2.setText(str(save_location[0]))


    def Download(self):
        ## downloading any file
        print('Start Download')

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self , "Data Error" , "Provide a valid URL or save location")
        else:

            try:
                urllib.request.urlretrieve(download_url , save_location , self.Handel_Progress)

            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
                return


        QMessageBox.information(self , "Download Completed" , "The Download Completed Successfully ")

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)




    def Save_Browse(self):
        ## save location in the line edit
        save_location = QFileDialog.getExistingDirectory(self, 'select download directory')

        self.lineEdit_10.setText(save_location)

    def Get_Video_Data(self):

        video_url = self.lineEdit_9.text()
        print(video_url)

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")

        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.allstreams

            for stream in video_streams:
                print(stream.get_filesize())
                #size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} ".format(stream.mediatype, stream.extension, stream.quality)
                self.comboBox.addItem(data)


    def Download_Video(self):
            video_url = self.lineEdit_9.text()
            video = pafy.new(video_url)
            video_stream = video.allstreams
            video_quality = self.comboBox.currentIndex()
            save_locations = self.lineEdit_10.text()
            Quality = self.comboBox.currentIndex()
            download = video_stream[Quality].download(filepath=save_locations,callback=self.Video_Progress )
            self.lineEdit_9.setText('')
            self.lineEdit_10.setText('')
            self.progressBar_2.setValue(0)

    def Playlist_Download(self):
        playlist_url = self.lineEdit_16.text()
        save_location = self.lineEdit_17.text()
        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            os.chdir(save_location)
            if os.path.exists(str(playlist_url['title'])):
                os.chdir(str(playlist_url['title']))

            else:
                os.mkdir(str(playlist_url['title']))
                os.chdir(str(playlist_url['title']))
            playlist = Playlist(playlist_url)
            self.lcdNumber.display(len(playlist.video_urls))
            QApplication.processEvents()
            #print('Number of videos in playlist: %s' % len(playlist.video_urls))
            current_video_in_download = 0
        for video_url in playlist.video_urls:
            current_video_in_download += 1
            self.lcdNumber_2.display(current_video_in_download)
            youtube = YouTube(video_url,on_progress_callback=self.Playlist_Progress)
            video = youtube.streams.first()
            video.download(save_location)

        self.lineEdit_16.setText('')
        self.lineEdit_19.setText('')
        self.progressBar_3.setValue(0)


    def Video_Progress(self , total , received , ratio , rate , time):
        read_data = received
        if total > 0 :
            download_percentage = read_data * 100 / total
            self.progressBar_2.setValue(download_percentage)
            #remaining_time = round(time/60 , 2)

            #self.label_5.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def Playlist_Save_Browse(self):
        ## save location in the line edit
        save_playlist_location = QFileDialog.getExistingDirectory(self, 'select download directory')

        self.lineEdit_17.setText(save_playlist_location)


    def Playlist_Progress(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = (float(abs(bytes_remaining - size) / size)) * float(100)
        self.progressBar_3.setValue(progress)
        QApplication.processEvents()


    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        save_playlist_location = QFileDialog.getExistingDirectory(self, 'show downloads')
        #self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        webbrowser.open('www.youtube.com', new=0, autoraise=True)


    def About_Me(self):
        self.tabWidget.setCurrentIndex(3)
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
