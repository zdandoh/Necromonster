from globals import *

class HUD():
    def __init__(self, game):
        self.game = game
        self.xpbar = pygame.image.load(self.game.main_path + '\\rec\\gui\\xpbar.png').convert_alpha()
        self.hpbar = pygame.image.load(self.game.main_path + '\\rec\\gui\\hpbar.png').convert_alpha()

    def blitHUD(self):
        #hp bar creation
        blit_surface = pygame.Surface((392 * (float(self.game.Player.player_stats['hp']) / self.game.Player.player_stats['maxhp']), 24), pygame.SRCALPHA)
        blit_surface.fill((234, 0, 0, 213))
        self.game.screen.blit(blit_surface, (254, 589))

        #xp bars
        blit_surface = pygame.Surface((497 * (float(self.game.Player.player_stats['mxp']) / self.game.Player.player_stats['maxmxp']), 12), pygame.SRCALPHA)
        blit_surface.fill((72, 196, 19, 221))
        self.game.screen.blit(blit_surface, (201, 636))
        blit_surface = pygame.Surface((497 * (float(self.game.Player.player_stats['pxp']) / self.game.Player.player_stats['maxpxp']), 12), pygame.SRCALPHA)
        blit_surface.fill((229, 102, 18, 221))
        self.game.screen.blit(blit_surface, (201, 622))

        self.game.screen.blit(self.xpbar, [200, 636])
        self.game.screen.blit(self.xpbar, [200, 622])
        self.game.screen.blit(self.hpbar, [250, 585])