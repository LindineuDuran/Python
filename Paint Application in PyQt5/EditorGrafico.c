#include <GL/glut.h>
#include <GL/gl.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

// Constantes
#define LINHA     1
#define QUADRADO  2
#define RETANGULO 3
#define TRIANGULO 4
#define CIRCULO   5

GLfloat r, g, b;
GLfloat t, u, v;
GLint primitiva;

int xIni, xFim, yIni, yFim;
int draw = 0;
char texto[30];

struct coord
{
    int x; /* Eixo x */
    int y; /* Eixo y */
};

struct cor
{
   GLfloat r;
   GLfloat g;
   GLfloat b;
};

typedef struct tipo_forma
{
    char nome[15];     /* Nome da Primitiva */
    struct coord ini;  /* Início */
    struct coord fim;  /* Fim */
    struct cor tinta;  /*Cor do desenho*/
    //struct tipo_forma *proximo; /* Proximo elemento da lista encadeada de Produtos */
}  TForma;

// Desenha linha preenchida com a cor corrente
void DesenhaLinha(void)
{
     glBegin(GL_LINES);
	   glVertex2i(xIni, yIni);
	   glVertex2i(xFim, yFim);
     glEnd();
}

// Função que desenha um quadrado
void DesenhaQuadrado(void)
{
     int meioLado;
     //int x, y;
     if (xFim-xIni > yFim-yIni)
     {
         meioLado= xFim-xIni;
     }
     else
     {
         meioLado= yFim-yIni;
     }
     glBegin(GL_QUADS);
       glVertex2f(xIni-meioLado, yIni-meioLado);
       glVertex2f(xIni-meioLado, yIni+meioLado);
       glVertex2f(xIni+meioLado, yIni+meioLado);
       glVertex2f(xIni+meioLado, yIni-meioLado);
     glEnd();
}

// Função que desenha um retângulo
void DesenhaRetangulo(void)
{
     glBegin(GL_QUADS);
       glVertex2f(xIni, yIni);
       glVertex2f(xIni, yFim);
       glVertex2f(xFim, yFim);
       glVertex2f(xFim, yIni);
     glEnd();
}

// Função que desenha um triângulo
void DesenhaTriangulo(void)
{
     int raio;
     int x1, y1, x2, y2;
     if (xFim-xIni > yFim-yIni)
     {
         raio= xFim-xIni;
     }
     else
     {
         raio= yFim-yIni;
     }


     x1=(raio*sin((M_PI*30)/180)+(xIni));
     y1=(raio*cos((M_PI*30)/180)+(yIni));

     x2=(raio*sin((M_PI*-30)/180)+(xIni));
     y2=(raio*cos((M_PI*-30)/180)+(yIni));

     glBegin(GL_TRIANGLES);
       glVertex2f(x1, y1);
       glVertex2f(xIni, yIni);
       glVertex2f(x2, y2);
     glEnd();
}

// Desenha circunferência
void DesenhaCirculo(void)
{
     int raio;
     int angulo;
     int x, y;
     if (xFim-xIni > yFim-yIni)
     {
         raio= xFim-xIni;
     }
     else
     {
         raio= yFim-yIni;
     }
     for(angulo=0; angulo<360;angulo++)
     {
        x=(raio*sin((M_PI*angulo)/180)+(xIni));
        y=(raio*cos((M_PI*angulo)/180)+(yIni));

        // Desenha pontos preenchidos com a cor corrente
        glBegin(GL_POINTS);
           glVertex2i(x, y);
        glEnd();
     }
}

// Função callback chamada para fazer o desenho
void Desenha(void)
{
     glMatrixMode(GL_MODELVIEW);
     glLoadIdentity();

     // Define a cor de fundo da janela de visualização como branca
     glClearColor(t, u, v, 1.0f);
     glClear(GL_COLOR_BUFFER_BIT);

     // Define a cor do desenho
     glColor3f(r,g,b);

     // Desenha uma primitiva
     switch (primitiva)
     {
            case LINHA:     DesenhaLinha();
                            break;
            case QUADRADO:  DesenhaQuadrado();
                            break;
            case RETANGULO: DesenhaRetangulo();
                            break;
            case TRIANGULO: DesenhaTriangulo();
                            break;
            case CIRCULO:   DesenhaCirculo();
                            break;
     }

     DesenhaTexto(texto);
     glFlush();
}

// Desenha um texto na janela GLUT
void DesenhaTexto(char *string)
{
  	glPushMatrix();
    // Posição no universo onde o texto será colocado
    glRasterPos2f(10,470);
    // Exibe caracter a caracter
    while(*string)
    glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24,*string++);
	glPopMatrix();
}


// Inicializa parâmetros de rendering
void Inicializa (void)
{
    // Define a cor de fundo da janela de visualização como branca
    t = 1.0f;
    u = 1.0f;
    v = 1.0f;
    glClearColor(t, u, v, 1.0f);
    gluOrtho2D (0.0f, 480.0f, 480.0f, 0.0f);

    // Define a cor do desenho como preta
    r = 0.0f;
    g = 0.0f;
    b = 0.0f;
    primitiva = QUADRADO;
    strcpy(texto, "(0,0)");
}

// Função callback chamada quando o tamanho da janela é alterado
void AlteraTamanhoJanela(GLsizei w, GLsizei h)
{
   // Evita a divisao por zero
   if(h == 0) h = 1;

   // Especifica as dimensões da Viewport
   glViewport(0, 0, w, h);

   // Inicializa o sistema de coordenadas
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();

   // Estabelece a janela de seleção (left, right, bottom, top)
   if (w <= h)
       gluOrtho2D (0.0f, 480.0f, 480.0f*h/w, 0);
   else
       gluOrtho2D (0.0f, 480.0f*w/h, 480.0f, 0.0f);
}

// Gerenciamento do menu com as opções de cores
void MenuCor(int op)
{
   switch(op)
   {
        case 0:
                 r = 0.0f;
                 g = 0.0f;
                 b = 0.0f;
                 break;
        case 1:
                 r = 1.0f;
                 g = 1.0f;
                 b = 1.0f;
                 break;
        case 2:
                 r = 1.0f;
                 g = 0.0f;
                 b = 0.0f;
                 break;
        case 3:
                 r = 0.0f;
                 g = 1.0f;
                 b = 0.0f;
                 break;
        case 4:
                 r = 0.0f;
                 g = 0.0f;
                 b = 1.0f;
                 break;
    }
    glutPostRedisplay();
}

void MenuFundo(int op)
{
   switch(op)
   {
        case 0:
                 t = 0.0f;
                 u = 0.0f;
                 v = 0.0f;
                 break;
        case 1:
                 t = 1.0f;
                 u = 1.0f;
                 v = 1.0f;
                 break;
        case 2:
                 t = 1.0f;
                 u = 0.0f;
                 v = 0.0f;
                 break;
        case 3:
                 t = 0.0f;
                 u = 1.0f;
                 v = 0.0f;
                 break;
        case 4:
                 t = 0.0f;
                 u = 0.0f;
                 v = 1.0f;
                 break;
    }
    glutPostRedisplay();
}

// Gerenciamento do menu com as opções de cores
void MenuPrimitiva(int op)
{
   switch(op)
   {
        case 0:
                 primitiva = LINHA;
                 xIni=0;
                 xFim=0;
                 yIni=0;
                 yFim=0;
                 break;
        case 1:
                 primitiva = QUADRADO;
                 xIni=0;
                 xFim=0;
                 yIni=0;
                 yFim=0;
                 break;
        case 2:
                 primitiva = RETANGULO;
                 xIni=0;
                 xFim=0;
                 yIni=0;
                 yFim=0;
                 break;
        case 3:
                 primitiva = TRIANGULO;
                 xIni=0;
                 xFim=0;
                 yIni=0;
                 yFim=0;
                 break;
        case 4:
                 primitiva = CIRCULO;
                 xIni=0;
                 xFim=0;
                 yIni=0;
                 yFim=0;
                 break;
    }
    glutPostRedisplay();
}

// Gerenciamento do menu principal
void MenuPrincipal(int op)
{

}

// Criacao do Menu
void CriaMenu()
{
    int menu,submenu1,submenu2,submenu3;

	submenu1 = glutCreateMenu(MenuCor);
	glutAddMenuEntry("Preto",0);
	glutAddMenuEntry("Branco",1);
	glutAddMenuEntry("Vermelho",2);
	glutAddMenuEntry("Verde",3);
	glutAddMenuEntry("Azul",4);

	submenu2 = glutCreateMenu(MenuFundo);
	glutAddMenuEntry("Preto",0);
	glutAddMenuEntry("Branco",1);
	glutAddMenuEntry("Vermelho",2);
	glutAddMenuEntry("Verde",3);
	glutAddMenuEntry("Azul",4);

    submenu3 = glutCreateMenu(MenuPrimitiva);
    glutAddMenuEntry("Linha",0);
	glutAddMenuEntry("Quadrado",1);
	glutAddMenuEntry("Retangulo",2);
	glutAddMenuEntry("Triangulo",3);
	glutAddMenuEntry("Circulo",4);

    menu = glutCreateMenu(MenuPrincipal);
	glutAddSubMenu("Cor do Desenho",submenu1);
	glutAddSubMenu("Cor do Fundo",submenu2);
    glutAddSubMenu("Primitivas",submenu3);

	glutAttachMenu(GLUT_RIGHT_BUTTON);
}

// Função callback chamada para gerenciar eventos de teclado
void GerenciaTeclado(unsigned char key, int x, int y)
{
    switch (key)
    {
        case 'R':
        case 'r':// muda a cor corrente para vermelho
                 glColor3f(1.0f, 0.0f, 0.0f);
                 break;
        case 'G':
        case 'g':// muda a cor corrente para verde
                 glColor3f(0.0f, 1.0f, 0.0f);
                 break;
        case 'B':
        case 'b':// muda a cor corrente para azul
                 glColor3f(0.0f, 0.0f, 1.0f);
                 break;
        case 27: exit(0);
                 break;
    }
    glutPostRedisplay();
}

// Função callback chamada para gerenciar eventos do mouse
void GerenciaMouse(int button, int state, int x, int y)
{
    if (button == GLUT_LEFT_BUTTON)
         if (state == GLUT_DOWN)
         {
            xIni=x;
            xFim=x;
            yIni=y;
            yFim=y;
            draw=1;
            sprintf(texto, "(%d,%d)", x, y);
         }

    if (button == GLUT_RIGHT_BUTTON)
         if (state == GLUT_DOWN)
            CriaMenu();

    glutPostRedisplay();
}

// Função callback chamada sempre que o mouse é movimentado sobre a janela GLUT com um botão pressionado
void MoveMouseBotaoPressionado(int x, int y)
{
     xFim=x;
     yFim=y;
     sprintf(texto, "(%d,%d)", xFim, yFim);
     glutPostRedisplay();
}

// Função callback chamada sempre que o mouse é movimentado sobre a janela GLUT
void MoveMouse(int x, int y)
{
     sprintf(texto, "(%d,%d)", x, y);

     if (draw==1)
     {
        xFim=x;
        yFim=y;
        draw=0;

        // Pega Primitiva
        char nome[10];/*
        switch (primitiva)
        {
            case LINHA:     strncpy(nome, "LINHA",5);
                            break;
            case QUADRADO:  strncpy(nome, "QUADRADO",8);
                            break;
            case RETANGULO: strncpy(nome, "RETANGULO",9);
                            break;
            case TRIANGULO: strncpy(nome, "TRIANGULO",9);
                            break;
            case CIRCULO:   strncpy(nome, "CIRCULO",7);
                            break;
        }*/
        struct tipo_forma figura;
        strncpy(figura.nome, nome, 10);
        figura.ini.x = xIni;
        figura.ini.y = yIni;
        figura.fim.x = xFim;
        figura.fim.y = yFim;
        figura.tinta.r = r;
        figura.tinta.g = g;
        figura.tinta.b = b;
        printf("Nome: %s, xIni: %d, yIni: %d, xFim: %d, yFim: %d, Cor: %f, %f, %f\n", figura.nome, figura.ini.x, figura.ini.y, figura.fim.x, figura.fim.y,figura.tinta.r = r, figura.tinta.g = g, figura.tinta.b = b);
     }
     glutPostRedisplay();
}

// Programa Principal
int main(int argc, char** argv)
{
     glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
     glutInit(&argc, argv);
     glutInitWindowSize(640,480);
     glutInitWindowPosition(350,150);
     glutCreateWindow("Editor Grafico");
     glutDisplayFunc(Desenha);
     glutReshapeFunc(AlteraTamanhoJanela);
     glutMotionFunc(MoveMouseBotaoPressionado);
     glutPassiveMotionFunc(MoveMouse);
     glutMouseFunc(GerenciaMouse);
     glutKeyboardFunc(GerenciaTeclado);
     Inicializa();
     glutMainLoop();
}
