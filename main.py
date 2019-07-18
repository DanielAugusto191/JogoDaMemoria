# -*- coding: utf-8 -*-
#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *
from math import floor
from math import ceil
from PIL import Image, ImageTk
import os
import random
from threading import Timer


class Application():

    def __init__(self, window, player, numpecas=2, timeToSee=1):
        caminho = "_imgs/"
        imagens = [f for f in os.listdir(caminho)]
        self.viewCard = []
        self.newobj = None
        self.seconds = 0
        self.oldID = -1
        self.PecasAcertadas = 0

        def endGame():
            print("Thanks for Play!")
            file = open("HighScores.txt", "a+")
            file.write("({}-{}:{})\n".format(player,
                                             self.tempoMin, self.tempoSeg))
            file.close()
            killProcess()

        def killProcess():
            print("See you next time!")
            self.time.cancel()
            window.destroy()
            main()

        def toggleCard(obj, img, reset):
            obj.configure(image=img)
            obj.image = img
            if (reset):
                obj.configure(state=NORMAL)
                self.viewCard.clear()

        def IDVerify(id, obj, sizeX, sizeY, reference):
            if len(self.viewCard) == 2 or self.oldID == id:
                pass
            else:
                self.oldID = id
                self.viewCard.append(reference)
                path = caminho+imagens[reference]
                img = Image.open(path)
                img = img.resize((floor(sizeX), floor(sizeY)), Image.ANTIALIAS)
                img2 = ImageTk.PhotoImage(img)
                # obj.configure(state=DISABLED)
                toggleCard(obj, img2, False)

                if (len(self.viewCard) == 1):
                    self.newobj = obj
                elif(len(self.viewCard) == 2):
                    if(self.viewCard[0] == self.viewCard[1]):
                        self.PecasAcertadas += 1
                        obj.configure(state=DISABLED)
                        self.newobj.configure(state=DISABLED)
                        self.Pecas[id] = 0
                        self.viewCard.clear()
                        if self.PecasAcertadas >= (self.numPecas**2)/2:
                            endGame()
                    else:
                        img = Image.open("_Default/X.png")
                        img = img.resize(
                            (floor(sizeX), floor(sizeY)), Image.ANTIALIAS)
                        img2 = ImageTk.PhotoImage(img)
                        t = Timer(float(timeToSee), toggleCard,
                                  [obj, img2, True])
                        t.start()
                        t2 = Timer(float(timeToSee), toggleCard,
                                   [self.newobj, img2, True])
                        t2.start()

        # Declarando Variaveis
        window.configure(background="#060040")
        # Tamanhos
        windowWidth = 1000
        windowHeight = 750
        window.geometry("{}x{}".format(windowWidth, windowHeight))
        window.resizable(0, 0)
        sizeGameScreen = 800
        sizeGameScreenY = 700
        # Cores
        corTitulo = "#072140"
        corPlacar = "#0E4180"
        corGame = "#1562BF"
        corRodape = "#042780"

        # Pontos
        self.pontos = 0

        # |Frames

        # |Styles
        # |-Frames
        # |--Title
        TitleMainConfig = Style()
        TitleMainConfig.configure(
            "menuMainFrameStyle.TFrame", background=corTitulo)
        TextMainConfig = Style()
        TextMainConfig.configure(
            "titleMainStyle.TLabel", background=corTitulo, foreground="#fff")
        # |--Placar
        TitlePlacarConfig = Style()
        TitlePlacarConfig.configure(
            "menuPlacarFrameStyle.TFrame", background=corPlacar)
        TextMainConfig = Style()
        TextMainConfig.configure(
            "titlePlacarStyle.TLabel", background=corPlacar, foreground="#fff")
        # |--Rodape
        RodapeScreen = Style()
        RodapeScreen.configure("backRodapeStyle.TFrame", background=corRodape)
        RodapeTitle = Style()
        RodapeTitle.configure("rodapeText.TLabel",
                              background=corRodape, foreground="#fff")
        # |--Game
        gameScreen = Style()
        gameScreen.configure("backGameStyle.TFrame", background=corGame)

        # |-Buttons
        # |--Peças
        pecasStyle = Style()
        pecasStyle.configure("backPecaStyle.TButton",
                             background=corGame, borderwidth=0)

        self.lbf_titulo = Frame(window, width=windowWidth,
                                height=50, style="menuMainFrameStyle.TFrame")
        self.lbf_titulo.grid(row=0, column=0, columnspan=2)
        self.lbf_placar = Frame(
            window, width=200, height=600, style="menuPlacarFrameStyle.TFrame")
        self.lbf_placar.grid(row=1, column=1)
        self.lbf_game = Frame(window, width=sizeGameScreen,
                              height=sizeGameScreenY, style="backGameStyle.TFrame")
        self.lbf_game.grid(row=1, column=0, rowspan=2)
        self.lbf_rodape = Frame(
            window, width=200, height=100, style="backRodapeStyle.TFrame")
        self.lbf_rodape.grid(row=2, column=1)

        # |MainTitulo
        self.mainTitle = Label(self.lbf_titulo, text="Jogo da Memoria",
                               style="titleMainStyle.TLabel", font=('Arial-Rounded', 20))
        self.mainTitle.grid(row=0, column=0)
        self.mainTitle.place(x=windowWidth/2, y=10, anchor='n')
        # |PlacarTitulo
        self.tempoSeg = 0
        self.tempoMin = 0
        self.PlacarTitulo = Label(self.lbf_placar, text="Tempo",
                                  style="titlePlacarStyle.TLabel", font=('Arial-Rounded', 30))
        self.PlacarTitulo.grid(row=0, column=0, columnspan=2)
        self.PlacarTitulo.place(x=100, y=10, anchor='n')
        self.Points = Label(self.lbf_placar, text=self.tempoSeg,
                            style="titlePlacarStyle.TLabel", font=("Arial", 20))
        self.Points.grid(row=1, column=1, columnspan=2)
        self.Points.place(x=100, y=50, anchor='n')

        def Timming():
            self.tempoSeg += 1
            if(self.tempoSeg >= 60):
                self.tempoSeg = 0
                self.tempoMin += 1
            self.Points.config(text="{}:{}".format(
                self.tempoMin, self.tempoSeg))
            self.time = Timer(1, Timming)
            self.time.start()
        Timming()

        # |Game
        # |-Peças
        # |--Tamanho
        self.numPecas = int(int(numpecas)**(1/2))
        self.refPeca = 2*[x for x in range(int((self.numPecas**2)/2))]
        self.posX = 0
        self.posY = 0
        self.pad = 10
        self.NewPos = 0
        self.NewPosY = 0
        self.tamanhoPecaX = (
            (sizeGameScreen - (self.pad * (self.numPecas+1)))/self.numPecas)
        self.tamanhoPecaY = (
            (sizeGameScreenY - (self.pad * (self.numPecas+1)))/self.numPecas)
        # |--Imagem Padrao
        self.loadImg = Image.open('_Default/X.png')
        self.loadImg = self.loadImg.resize(
            (floor(self.tamanhoPecaX), floor(self.tamanhoPecaY)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(self.loadImg)

        # |-- Posicionamento
        self.Pecas = []
        self.PecaId = 0
        for i in range(self.numPecas):
            self.NewPosY = (self.NewPosY + self.pad + self.posY)
            for j in range(self.numPecas):
                self.NewPos = (self.NewPos + self.pad + self.posX)
                self.posX = self.tamanhoPecaX
                self.initRef = random.choice(self.refPeca)
                self.refPeca.remove(self.initRef)
                self.Pecas.append(Button(self.lbf_game, image=img, style="backPecaStyle.TButton", command=lambda x=self.PecaId,
                                         y=self.initRef: IDVerify(x, self.Pecas[x], self.tamanhoPecaX, self.tamanhoPecaY, y)))
                self.Pecas[-1].image = img
                self.Pecas[-1].grid(row=0, column=0)
                self.Pecas[-1].place(x=self.NewPos,
                                     y=self.NewPosY, anchor='nw')
                self.PecaId += 1
            self.posY = self.tamanhoPecaY
            self.NewPos = 0
            self.posX = 0

        #|Rodape
        self.email = Label(self.lbf_rodape, text="Daniel.Augusto191@gmail.com",
                           style="rodapeText.TLabel", font=("Arial", 10))
        self.email.grid(row=0, column=0)
        self.email.place(x=10, y=70)

        # Caso a janela feche!
        window.protocol("WM_DELETE_WINDOW", killProcess)


class MainMenu():
    def __init__(self, window):
        window.configure(background="#060040")
        # Tamanhos
        windowWidth = 920
        windowHeight = 750
        window.resizable(0,0)
        window.geometry("{}x{}".format(windowWidth, windowHeight))
        # Styles
        self.mainTitleStyle = Style()
        self.mainTitleStyle.configure(
            "mainTitleStyle.TLabel", foreground="#fff", background="#060040")
        self.configStyleFrames = Style()
        self.configStyleFrames.configure(
            "frameStyle.TFrame", background="#1562BF", foreground="#fff")
        self.fullFrameStyle = Style()
        self.fullFrameStyle.configure(
            "fullFrameStyle.TFrame", background="#060040")
        self.msgLabelStyle = Style()
        self.msgLabelStyle.configure("msgLabelStyle.TLabel",  background="#1562BF", font=(
            "Arial", 14), foreground="#fff")

        # Frames
        self.FrameFull = Frame(window, width=windowWidth,
                               style="fullFrameStyle.TFrame")
        self.FrameFull.grid(row=0, column=0)
        self.controlButtonsFrame = Frame(
            self.FrameFull, style="frameStyle.TFrame", width=300, height=350)
        self.controlButtonsFrame.grid(row=1, column=0, padx=5)
        self.controlConfigsFrame = Frame(
            self.FrameFull,  style="frameStyle.TFrame", width=300, height=350)
        self.controlConfigsFrame.grid(row=1, column=1)
        self.highscoreFrame = Frame(
            self.FrameFull,  style="frameStyle.TFrame", width=300, height=350)
        self.highscoreFrame.grid(row=1, column=2, padx=5)
        # Title
        self.mainTitle2 = Label(self.FrameFull, text="JOGO DA MEMORIA",
                                style="mainTitleStyle.TLabel", font=("Arial", 48))
        self.mainTitle2.grid(row=0, column=0,  columnspan=3, pady=40)

        #Control Buttons Frame
        self.YourName = Label(
            self.controlButtonsFrame, text="Coloque seu nome: ", style="msgLabelStyle.TLabel")
        self.YourName.place(x=80, y=60, anchor="nw")

        def Start():
            if (len(self.NickName.get()) > 15):
                self.Aviso['text'] = "Nick deve ter no maximo 15 Caracteres!"
            else:
                Application.__init__(self, window, (self.NickName.get(
                )), (self.quantidadeDePecas.get()), (self.TimeCount.get()))
                self.FrameFull.destroy()

        self.buttonStart = Button(
            self.controlButtonsFrame, width=10, text="Começar!", command=lambda: Start())
        self.buttonStart.place(x=110, y=150, anchor="nw")

        self.NickName = Entry(self.controlButtonsFrame, width=20)
        self.NickName.place(x=75, y=90, anchor="nw")
        self.Aviso = Label(self.controlButtonsFrame, text="",
                           style="msgLabelStyle.TLabel", font=("Arial", 10))
        self.Aviso.place(x=40, y=120, anchor="nw")
        self.buttonExit = Button(
            self.controlButtonsFrame, width=10, text="Sair :'(", command=lambda: exit())
        self.buttonExit.place(x=110, y=185, anchor="nw")

        # Configuralções
        self.escolhePeca = Label(
            self.controlConfigsFrame, text="Escolha a quantidade de Peças:", style="msgLabelStyle.TLabel")
        self.escolhePeca.place(x=25, y=35, anchor="nw")
        self.quantidadeDePecas = Combobox(
            self.controlConfigsFrame, textvariable="1")
        self.quantidadeDePecas['values'] = (
            '4', '16', '36', '64', '100', '144', '196')
        self.quantidadeDePecas.current(0)
        self.quantidadeDePecas.place(x=70, y=60, anchor="nw")
        self.escolheTempo = Label(
            self.controlConfigsFrame, text="Escolha quanto tempo para ver\n a carta quanto errar. (segundos)", style="msgLabelStyle.TLabel")
        self.escolheTempo.place(x=15, y=140, anchor="nw")
        self.TimeCount = Combobox(self.controlConfigsFrame, textvariable="2")
        self.TimeCount['values'] = ('0', '0.5', '1', '2')
        self.TimeCount.current(2)
        self.TimeCount.place(x=70, y=200, anchor="nw")

        # Highscore

        self.HighscoreLabel = Label(
            self.highscoreFrame, text="HIGHSCORES", style="msgLabelStyle.TLabel", font=("Arial", 20))
        self.HighscoreLabel.place(x=65, y=20, anchor="nw")
        try:
            self.file = open("HighScores.txt", "r")
            self.lines = self.file.readlines()
            pontos = []
            for i in self.lines:
                nome = i.split('-')[0].replace('(', '')
                tempPonto = i.split('-')[1].replace(')\n', '').replace(')', '')
                pontos.append([nome, tempPonto])
            pontos = dict(pontos)
            pontos = (sorted(pontos.items(), key=lambda x: x[1]))
            self.nome = []
            self.scoreplace = []
            distanciaNome = 65
            for i in range(len(pontos)):
                self.nome.append(Label(self.highscoreFrame, text="{} - {}".format(i +
                                                                                1, pontos[i][0]), style=("msgLabelStyle.TLabel")))
                self.nome[i].place(x=20, y=distanciaNome, anchor='nw')
                self.scoreplace.append(
                    Label(self.highscoreFrame, text=pontos[i][1], style="msgLabelStyle.TLabel"))
                self.scoreplace[i].place(x=200, y=distanciaNome, anchor="nw")
                distanciaNome += 25
        except IOError as e:
            print("Não há arquivo para HighScore. Será criado após a primeira partida!")

def main():
    root = Tk()
    MainMenu(root)
    root.mainloop()


if __name__ == "__main__":

    main()
