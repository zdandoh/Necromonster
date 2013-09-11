class EntityHandler():
    def __init__(self, game):
        self.game = game
        self.world_items = []
        self.monsters = []
        self.projectiles = []
        self.misc = []
        self.all_entities = []

    def blitAll(self):
        for index, entity in enumerate(self.all_entities):
            entity.blit()
        self.game.Player.blitPlayer()

    def updateAll(self, ttime):
        self.all_entities = self.world_items + self.monsters + self.projectiles + self.misc
        for lst in [self.world_items, self.monsters, self.projectiles, self.misc]:
            for index, entity in enumerate(lst):
                if entity.update(index, ttime):
                    del lst[index]
        self.game.Player.update(ttime)

    def clear(self):
        self.monsters = []
        self.projectiles = []
        self.world_items = []
        self.misc = []