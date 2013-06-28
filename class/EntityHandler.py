class EntityHandler():
    def __init__(self, game):
        self.game = game
        self.monsters = []
        self.projectiles = []
        self.all_entities = []

    def blitAll(self):
        self.game.Player.blitPlayer()
        for index, entity in enumerate(self.all_entities):
            entity.blit()

    def updateAll(self):
        self.game.Player.update()
        self.all_entities = self.monsters + self.projectiles
        for lst in [self.monsters, self.projectiles]:
            for index, entity in enumerate(lst):
                if entity.update():
                    del lst[index]

    def clear(self):
        self.monsters = []
        self.projectiles = []