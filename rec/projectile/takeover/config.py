def onCollide(self):
	self.setDead()
	self.game.EntityHandler.monsters[self.monster_index].hp = self.game.EntityHandler.monsters[self.monster_index].maxhp
	self.game.Player.takeOver(self.game.EntityHandler.monsters[self.monster_index])

self.onCollide = onCollide
self.speed = 10