# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:32:40 2022

@author: Seldon
"""

import pandas as pd
import numpy as np
import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout,\
    QHBoxLayout, QWidget, QLabel, QMessageBox

# user defined variables    
guess_path = "C:/Users/Seldon/Dropbox/WomenFederalGovt/data/Job title cleaning/guess.csv"

class ParentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Guess Confirm')
        # buttons
        self.confirm_button = QPushButton("Confirm")
        self.reject_button = QPushButton("Reject")
        self.hard_reject_button = QPushButton("Bad String")
        self.undo_button = QPushButton("Undo")
        
        # vars
        self.index_num = np.nan
        self.last_mask_list = []
        # labels
        self.data_new_label = QLabel(" dsifj navy 312 3")
        self.title_guess_label = QLabel('navy')
        self.remaining_guesses_label = QLabel("Remaining Guesses: ")
        
        self.layout = QVBoxLayout()
        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout1.addWidget(self.data_new_label)
        self.layout1.addWidget(self.title_guess_label)
        self.layout2.addWidget(self.hard_reject_button)
        self.layout2.addWidget(self.reject_button)
        self.layout2.addWidget(self.confirm_button)
        self.layout2.addWidget(self.undo_button)
        self.layout3.addWidget(self.remaining_guesses_label)
    
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)

        self.setLayout(self.layout)
        
        self.confirm_button.clicked.connect(self.confirm)
        self.reject_button.clicked.connect(self.reject)
        self.hard_reject_button.clicked.connect(self.hard_reject)
        self.undo_button.clicked.connect(self.undo)
        # user vars, may change later
        self.guess_path = guess_path
        self.guess_df = self.load_data(self.guess_path)
        self.setup_guess()
        
    def confirm(self):
        # mark same guesses as correct
        guess = self.guess_df.loc[self.index_num,'guess']
        mask = self.guess_df['guess']==guess
        self.guess_df.loc[mask,'correct'] = 1
        
        self.last_mask_list.append(mask)
        self.setup_guess()
        
    def reject(self):        
        # mark same guesses as incorrect
        guess = self.guess_df.loc[self.index_num,'guess']
        mask = self.guess_df['guess']==guess
        self.guess_df.loc[mask,'correct'] = 0

        self.last_mask_list.append(mask)
        self.setup_guess()
    
    def hard_reject(self):
        # set string to bad
        # Note: hard reject ONLY rejects current string
        mask = self.index_num
        self.guess_df.loc[mask,'correct'] = -1
    
        self.last_mask_list.append(mask)
        self.setup_guess()
        
    def undo(self):
        if len(self.last_mask_list) > 0:
            
            mask = self.last_mask_list[-1]
            self.guess_df.loc[mask,'correct'] = np.nan
            self.last_mask_list = self.last_mask_list[:-1]
            self.setup_guess()
        
        
    def load_data(self,path):
        data = pd.read_csv(path)
        return(data)
    
    def setup_guess(self):
        indices = np.where(self.guess_df.correct.isna())[0]
        if len(indices) > 0:
            self.index_num = indices[0]
            
            string = self.guess_df.loc[self.index_num,'string']
            guess = self.guess_df.loc[self.index_num,'guess']
            self.data_new_label.setText(str(string))
            self.title_guess_label.setText(str(guess))
            
        self.update_remaining_guess_label()
            
    def update_remaining_guess_label(self):
        remaining_guesses = self.guess_df.correct.isna().sum()
        self.remaining_guesses_label.setText("Remaining Guesses: " + str(remaining_guesses))
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.hard_reject()
        elif event.key() == Qt.Key_D:
            self.confirm()
        elif event.key() == Qt.Key_W:
            self.reject()

        event.accept()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Would you like to save your progress?", QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
            self.guess_df.to_csv(self.guess_path,index=False)
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

        


if __name__ == "__main__":
    App = QApplication(sys.argv)
    MyWindow= ParentWindow()
    MyWindow.show()
    App.exec()