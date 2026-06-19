## Adapteur DustTrak 
Cet adapteur peut fonctionner de deux façons: mode openfactory ou mode csv. Cela change la façon dont sont exportées les données du capteur. Il est aussi possible de changer la fréquence de lecture des données dans le même [fichier de configuration](config.json).

### Prérequis
Pour que l'initialisation de l'adapteur fonctionne, il faut s'assurer d'avoir un répertoire nommé `templates` et d'inclure des captures d'écran de chacun des éléments suivants.

- `dust_trak_shortcut.png` : capture d'écran du raccourci de l'application Environmental DustTrak Checkout sur le bureau.
  - Vérifiez que le raccourci existe sur votre bureau.
  - Si l'image dans `templates/dust_trak_shortcut.png` ne correspond pas à votre propre raccourci, remplacez-la par une nouvelle capture d'écran.
  - L'adapteur utilise cette image pour lancer l'application depuis le bureau.

  ![alt text](examples/dust_trak_shortcut.png)

- `dust_trak_task_bar.png` : capture d'écran du logo de l'application dans la barre des tâches.
  - Cette image permet d'identifier si l'application est déjà ouverte et d'éviter de lancer plusieurs instances.
  - Si votre interface Windows ou vos icônes sont différentes, remplacez `templates/dust_trak_task_bar.png` par une capture d'écran actualisée.
  - L'adapteur clique sur cette icône si l'application est déjà ouverte.

  ![alt text](examples/dust_trak_task_bar.png)

- `play_btn.png` : capture d'écran du bouton `play` dans l'interface DustTrak.
- `stop_btn.png` : capture d'écran du bouton `stop` dans l'interface DustTrak.
- `data_tab.png` : capture d'écran de l'onglet `Data` ou de l'élément permettant d'accéder aux données.
- `connect_tab.png` : capture d'écran de l'onglet `Connect` ou de l'élément de connexion.
- `connect_btn.png` : capture d'écran du bouton `Connect`.
- `connect_to_instrument_btn.png` : capture d'écran du bouton `Connect to Instrument`.
- `disconnect_btn.png` : capture d'écran du bouton `Disconnect`.
- `readings_nb_input.png` : capture d'écran du champ de saisie du nombre de lectures.
- `set_btn.png` : capture d'écran du bouton `Set`.

Ces images sont utilisées par le script d'initialisation pour détecter et cliquer sur les éléments de l'application DustTrak.

Conseils :
- Ouvrez l'application Environmental DustTrak Checkout une première fois manuellement pour vérifier que le raccourci, la barre des tâches et les autres éléments correspondent aux captures d'écran.
- Ne déplacez pas ou ne renommez pas les fichiers `templates/*.png` après les avoir configurés.
- Assurez-vous que Windows n'affiche pas de fenêtres modales ou de boîtes de dialogue bloquantes au démarrage de l'initialisation.
