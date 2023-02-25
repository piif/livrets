# livrets

Outil minimaliste pour réordonner un pdf en livrets

On part d'un document de N pages, et on en fait une série de feuilles qu'il faut replier pour obtenir les pages dans le bon ordre (1, 2, N-1, N par exemple)

Une option permet de le faire par petits livrets (séries de 4 feuilles de 16 pages par exemple)

## Utilisation :
`livrets -i fichier_d_entree -o fichier_de_sortie [ -l | -s ] [ -n N ]`
 * `-i` : nom du fichier pdf en entrée
 * `-o` : nom du fichier pdf en sortie
 * `-l` : organiser pour une impression recto/verso sur le bord long
 * `-s` : organiser pour une impression recto/verso sur le bord court (short)
 * `-n N` : organiser par paquets de N feuilles (donc N*4 pages)
