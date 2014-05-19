class EntityHandler():
    def __init__(self, game):
        """
        Class used for updating/managing all entities.
        """
        self.game = game
        self.active = True
        self.world_items = []
        self.monsters = []
        self.projectiles = []
        self.misc = []
        self.all_entities = []

    def blitAll(self):
        """
        Draws every active entity to the screen object.
        """
        for index, entity in enumerate(self.all_entities):
            entity.draw()
        self.game.Player.blitPlayer()

    def updateAll(self, ttime):
        """
        Updates every entity, if entity update funtion returns True, deletes the entity.
        """
        #call default update function of all entities
        self.all_entities = self.world_items + self.monsters + self.projectiles + self.misc
        for lst in [self.world_items, self.monsters, self.projectiles, self.misc]:
            for index, entity in enumerate(lst):
                if entity.update(index, ttime):
                    del lst[index]
        self.game.Player.update(ttime)

    def clear(self):
        """
        Clears all entities from the map and memory
        """
        self.monsters = []
        self.projectiles = []
        self.world_items = []
        self.game.shadows = []
        self.misc = []