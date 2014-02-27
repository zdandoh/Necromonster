self.greeting = "All your blacksmithing needs!"

self.text.setText(self.text.root, 'Want to buy some stuff?')
op2 = self.text.addOption(self.text.root, "No", "Oh, okay")
op1 = self.text.addOption(self.text.root, "Yes", "WOW RUDE OKEY")
self.text.setAction(op1, "self.terminated = True")
self.text.setAction(op2, "self.terminated = True")