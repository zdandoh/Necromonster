self.greeting = "All your blacksmithing needs!"

self.text.setText(self.text.root, 'ARE YOU SCREWING THE SHEEP?')
op2 = self.text.addOption(self.text.root, "No", "Oh, okay")
op1 = self.text.addOption(self.text.root, "Yes", "YOU'RE GOING TO DIE")
self.text.setAction(op1, "self.terminated = True")
self.text.setAction(op2, "self.terminated = True")