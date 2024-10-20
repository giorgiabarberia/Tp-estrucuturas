class AppStore:
    def __init__(self):
        self.apps_descargadas = {
            'Spotify': False,
            'Tetris': False,
            'Salud': False,
            'Instagram': False
        }
    def eliminar_app (self,app):
        if app in self.apps_descargadas and not self.apps_descargadas[app]:
            self.apps_descargadas[app]=True
            print(f'{app} ha sido descargada.')
        if app in self.apps_descargadas and self.apps_descargadas[app]:
            print(f'{app} ya esta descargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')
    
    def cargar_app (self,app):
        if app in self.apps_descargadas and self.apps_descargadas[app]:
            self.apps_descargadas[app]=True
            print(f'{app} ha sido cargada.')
        if app in self.apps_descargadas and not self.apps_descargadas[app]:
            print(f'{app} ya esta cargada.')
        else:
            print(f'{app} no se encuentra en AppStore.')


