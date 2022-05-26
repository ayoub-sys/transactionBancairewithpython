ce projet intitulé transaction bancaire gère bien évidemment les transactions bancaires:




il y a 3 principaux fichiers:

    client.py avec interface graphique et un fichier application.kivy 

    server.py : qui va traiter les transactions effectués par le client

    traitement.py: qui va gérer les fichiers (ouverture, lecture,écriture,mis à jour etc..)




Notons bien: l'obligation de créer un table "credential" qui a comme colonne pass(pour le password), client(indique le nom du client ),er ref(indique l'id du client

préalablement créé dans le fichier account.txt(qui gère le copmte en global)

cet table va nous servir à l'authentification du client 





Aussi les fichier.txt:(account.txt,transaction.txt,invoice.txt)


un logo.png 