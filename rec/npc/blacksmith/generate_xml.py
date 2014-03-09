self.greeting = "All your blacksmithing needs!"

self.text.setText(self.text.root, 'Want to buy some stuff?')
op2 = self.text.addOption(self.text.root, "No", "Oh, okay")
op1 = self.text.addOption(self.text.root, "Yes", "Oh wow!")
op3 = self.text.addOption(op1, "Are you sure?", "I don't have anything...")
#self.text.setAction(op1, "self.terminated = True")
#self.text.setAction(op2, "self.terminated = True")