def onCollide(self):
	self.setDead()
	self.game.Player.takeOver(self.last_monster)

self.onCollide = onCollide
self.speed = 10