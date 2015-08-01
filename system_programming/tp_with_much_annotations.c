#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>
#include <time.h>

/* New by FAR */
#define NB_VALEURS_ALEATOIRES 30
/*
 * Variables globales car devant etre accedees depuis un handler
 * Ah mais en fait, avec ma conception, no need. On les fout dans le main.
 */
/* Ancien code 
int t[2];
int max = 0;
*/
/*
 * Handler appele quand le fils recoit SIGUSR1. Auparavant, elle servait 
 * seulement a ce que le max soit affiche. Maintenant, je m'en sert juste pour
 * que le fils ne soit pas tue par SIGUSR1.
 */
 /* Ancien code
void MaFonction () {
    printf("La valeur max est %i \n",max);
    close(t[0]);
}
*/
/* New by FAR */
void monHandlerSigUSR1()
{
    ;
}


/* Seriously, un main, en C, même s'il termine jamais le prototype c'est 
int main(void) ou int main(int argc, char *argv[]) ou un autre mais JAMAIS
"<rien> main()". Enfin, je dis ca, je dis rien */
int main() {

    /* 
     * Declaration des variables de compteur (pour la boucle), et de valeur 
     * temporaire. 
     */
    int cpt;
    pid_t p;
    /* Je n'utilise pas val (un int) mais un tableau d'int 
    int val; 
    */
    
    /* New by FAR : creation d'un tableau, d'un tableau d'int qui va recueillir
     * le pipe et de la variable "max" 
     */
    int tabval[NB_VALEURS_ALEATOIRES];
    int t[2];
    int max = 0;
    /*
     * On cree notre pipe.
     * t contient maintenant un descripteur en lecture et un en ecriture
     * t[0] sert a lire et t[1] a ecrire.
     */
    pipe(t);
    
    /*
     * Bim, on cree le fils
     */
    p = fork();
    
    if (p > 0) {
        /* 
         * Si on est dans le pere, pas besoin de la lecture du pipe. 
         */
        close(t[0]);
        
        /* 
         * On genere 30 nombres aleatoires
         */
        
        /* MISSED : on initialise la graine de nombres aleatoires */
        srand(time(NULL));
        /* END MISSED */
        /*
         * On ecrit chaque nombre genere dans le pipe un par un.
         * Eh mais attend... ca fait tout plein d'I/O, ca, et les I/O
         * c'est lent... Vient genre on le stocke dans un tableau d'int
         * et on envoie que lui. 
         */
         
        /* Ancien code 
         for (cpt=1 ; cpt <= 30; cpt++){

            val = rand() % 1000000;
            printf("La valeur d'index %i est %i \n",cpt,val); //(1)
            
            write(t[1], &val, sizeof(int));
        }
        */
        
        /* New by FAR */
        
        for (cpt = 0 ; cpt < NB_VALEURS_ALEATOIRES; cpt++){

            tabval[cpt] = rand() % 1000000;
            printf("Dans le pere : %i -> %i .\n", cpt, tabval[cpt]); //(1)
        }
        
        /* BIM ! On envoie tout dans le pipe */
        write(t[1], tabval, sizeof(tabval));
        /* On le ferme en ecriture par pur principe */
        close(t[1]);
        
        /* On envoie SIGUSR1 au fils pour lui dire qu'on a termine d'ecrire
         dans le pipe. Le sleep(1) est la pour faire une tempo. C'est 
         legerement degueulasse et moralement abject mais on a pas appris les
         semaphores. En fait, je crois que les printf() en boucle au dessus
         etaient censes faire la tempo mais je ne peux rien affirmer. */
        printf("Envoi de SIGUSR1 dans une seconde.\n");
        sleep(1);
        kill(p, SIGUSR1);
        
        /*On attend que le fils se termine */
        wait(NULL);
        
        /* New by FAR */
        printf ("OMFG ! Mon fils est mort !\n");
    }


    if(p == 0) {
        /* Si on est dans le fils, on change vite son handler pour SIGUSR1
         * histoire de ne pas le tuer quand il le recoit (action par default)
         */
        signal(SIGUSR1, monHandlerSigUSR1);
        
        /* On ferme le pipe en ecriture : on souhaite seulement le lire. */
        close(t[1]);
        
        /* Eh mais... j'ai qu'un seul element dans mon pipe, moi, si t'as
         * suivi : un tableau d'int. Alors du coup, no need de faire une boucle
         * pour le lire. Et puis, 'faut pas oublier : je ne peux lire le pipe
         * que s'il y a quelque chose dedans. Je mets donc une pause et le pere
         * enverra un signal quand il en aura termine.
         */
         /* Ancien code 
        for (cpt=1;cpt<= 30;cpt++){

            read(t[0],&val,sizeof(int));
            printf("la %d valeur dans le fils est %d \n",cpt,val); //(2)

            if(max<val){max=val;}


        }*/
        /* New by FAR */
        pause();
        read(t[0], tabval, sizeof(tabval));
        /*
         * On boucle pour trouver le maximum et le mettre dans la variable
         * global 'max'.
         */
        for (cpt = 0 ; cpt < NB_VALEURS_ALEATOIRES ; cpt++) {
            printf("Dans le fils : %i -> %i .\n", cpt, tabval[cpt]);
            if (max < tabval[cpt]){   
                max = tabval[cpt];
            }
            
        }
        
        printf("La valeur max est %i \n",max);
        /* On peut close le descripteur en lecture. */
        close(t[0]);
        printf("Fin du fils.\n");
    }

    return 0;
}
