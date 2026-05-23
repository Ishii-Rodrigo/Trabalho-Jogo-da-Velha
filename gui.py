import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from jogo_da_velha import criar_board, faz_movimento, get_input_valido, \
    print_board, verifica_ganhador, verica_movimento

from minimax import movimento_ia, movimento_ia_facil, movimento_ia_medio

pygame.mixer.init()
pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play()

pygame.font.init()

def draw_board(win, board):
    height = 600
    width = 600
    tamanho = 600 // 3

    for i in range(1, 3):
        pygame.draw.line(win, (0, 0, 0), (0, i * tamanho),\
                              (width, i * tamanho), 3)
        
        pygame.draw.line(win, (0, 0, 0), (i * tamanho, 0), \
                         (i * tamanho, height), 3)
        
    for i in range(3):
        for j in range(3):
            font = pygame.font.SysFont('comicsans', 100)

            x = j * tamanho
            y = i * tamanho

            text = font.render(board[i][j], 1, (0, 0, 0))
            text_rect = text.get_rect(center=(x + tamanho // 2, y + tamanho // 2))
            win.blit(text, text_rect)

def redraw_window(win, board, dificuldade):
   
    if dificuldade == "Fácil":
        cor_fundo = (168, 230, 207)    
    elif dificuldade == "Médio":
        cor_fundo = (255, 238, 173)  
    else:
        cor_fundo = (255, 170, 165)    

    win.fill(cor_fundo)
    draw_board(win, board)

def main():
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo da Velha")

    font_titulo = pygame.font.SysFont('comicsans', 50)
    font_opcoes = pygame.font.SysFont('comicsans', 35)
    
    cor_facil = (168, 230, 207)    
    cor_medio = (255, 238, 173)    
    cor_dificil = (255, 170, 165)  

    btn_largura, btn_altura = 250, 55
    
    rect_facil = pygame.Rect(0, 0, btn_largura, btn_altura)
    rect_facil.center = (300, 260)

    rect_medio = pygame.Rect(0, 0, btn_largura, btn_altura)
    rect_medio.center = (300, 340)

    rect_dificil = pygame.Rect(0, 0, btn_largura, btn_altura)
    rect_dificil.center = (300, 420)

    while True:
        dificuldade = None

        while dificuldade is None:
            win.fill((40, 40, 40)) 
            
            text_titulo = font_titulo.render("Escolha a Dificuldade", 1, (255, 255, 255))
            rect_titulo = text_titulo.get_rect(center=(300, 140))
            win.blit(text_titulo, rect_titulo)

            pygame.draw.rect(win, cor_facil, rect_facil, border_radius=12)
            pygame.draw.rect(win, cor_medio, rect_medio, border_radius=12)
            pygame.draw.rect(win, cor_dificil, rect_dificil, border_radius=12)

            text_facil = font_opcoes.render("Fácil", 1, (40, 40, 40))
            text_medio = font_opcoes.render("Médio", 1, (40, 40, 40))
            text_dificil = font_opcoes.render("Difícil", 1, (40, 40, 40))

            win.blit(text_facil, text_facil.get_rect(center=rect_facil.center))
            win.blit(text_medio, text_medio.get_rect(center=rect_medio.center))
            win.blit(text_dificil, text_dificil.get_rect(center=rect_dificil.center))
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if rect_facil.collidepoint(pos):
                        dificuldade = "Fácil"
                    elif rect_medio.collidepoint(pos):
                        dificuldade = "Médio"
                    elif rect_dificil.collidepoint(pos):
                        dificuldade = "Difícil"
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        dificuldade = "Fácil"
                    elif event.key == pygame.K_2:
                        dificuldade = "Médio"
                    elif event.key == pygame.K_3:
                        dificuldade = "Difícil"

        board = criar_board()
        redraw_window(win, board, dificuldade)
        pygame.display.update()

        jogador = 0
        ganhador = verifica_ganhador(board)

        while(not ganhador):
            i = None
            j = None
            print_board(board)

            if jogador == 0:
                jogou = False

                while(not jogou):
                    for event in pygame.event.get():
                        if (event.type == pygame.QUIT):
                            return
                        elif (event.type == pygame.MOUSEBUTTONUP):
                            pos = pygame.mouse.get_pos()
                            i = int(pos[1]//200)
                            j = int(pos[0]//200)
                            jogou = True
            else:
                pygame.time.wait(400)
                
                if dificuldade == "Fácil":
                    i, j = movimento_ia_facil(board, jogador)
                elif dificuldade == "Médio":
                    i, j = movimento_ia_medio(board, jogador)
                elif dificuldade == "Difícil":
                    i, j = movimento_ia(board, jogador)

            if verica_movimento(board, i, j):
                faz_movimento(board, i, j, jogador)
                jogador = (jogador + 1) % 2

            ganhador = verifica_ganhador(board)
            redraw_window(win, board, dificuldade)
            pygame.display.update()

        fim_aguardando = True
        while fim_aguardando:
            redraw_window(win, board, dificuldade)
            
            font_fim = pygame.font.SysFont('comicsans', 22)
            if ganhador == "EMPATE":
                texto_fim = font_fim.render("Empate! Clique para reiniciar.", 1, (255, 255, 255))
            else:
                texto_fim = font_fim.render(f"Jogador {ganhador} venceu! Clique para reiniciar.", 1, (255, 255, 255))
            
            pygame.draw.rect(win, (0, 0, 0), (0, 260, 600, 80))
            text_rect = texto_fim.get_rect(center=(300, 300))
            win.blit(texto_fim, text_rect)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
                    fim_aguardando = False

main()