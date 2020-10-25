class Mission():
	def __init__(self):
		self.foundClues = set()
		self.clueDict,self.ghostDict = Mission.makeDicts()
		
		self.clueSet = set(self.clueDict.keys())
		self.ghostSet = set(self.ghostDict.keys())
		
		self.ghostInfo = {
			"banshee":"Will exclusively hunt one player until they die.",
			"demon":"Attacks often. SUCCESSFUL questions on the Ouija board will not decrease sanity.",
			"jinn":"Interacts with electronics (lights/cars/phones/radios/tvs) often. Moves very fast in hunts if fuse box in on. Low activity if players avoid ghost room.",
			"mare":"Will attack more often in dark and less often in light. Likes to turn off lights and the fuse box.",
			"phantom":"Can copy the appearance of a team member on hunts/manifestations (will never appear holding an item). Drops sanity rapidly when seen. Likes manifesting to stand still or walk for a moment. Photos cause the phantom to disappear (not stop a hunt).",
			"poltergeist":"Interacts with objects often, especially doors, even very far from its room. Interactions not directly seen will cause decrease in sanity. Can interact with multiple objects at once (not focused on electronics like a jinn).",
			"revenant":"Moves very fast during a hunt when it spots a player, and will switch to closer targets freely. Smudge sticks will disorient the Revenant and buy time to hide.",
			"shade":"Low activity when players are grouped. Try to use the Crucifix and Smudge Sticks to provide a safe window for a lone player to provoke activity and get clues.",
			"spirit":"No unique powers, making it slightly harder to identify. Smudge Sticks prevent attacks for twice the duration of other ghosts.",
			"wraith":"Touching salt immediately ends a hunt. Can hover over the ground, only occasionally taking steps. Can see and pass through doors and walls. Can teleport on top of players in the ghost room. Hiding is futile",
			"yurei":"Passively drains sanity slightly faster than baseline. Smudge Sticks will cause a Yurei to stay in its room.",
			"oni":"Very active when people are nearby, and can throw objects at great speed"
		}
	
	def makeDicts():
		clueDict = {"emf":{"shade","phantom","jinn","banshee","revenant","oni"},
					"temp":{"phantom","yurei","mare","demon","banshee","wraith"},
					"box":{"jinn","mare","demon","oni","poltergeist","spirit","wraith"},
					"prints":{"banshee","revenant","poltergeist","spirit","wraith"},
					"orbs":{"phantom","shade","jinn","yurei","mare","poltergeist"},
					"book":{"shade","yurei","demon","revenant","oni","spirit"}
				}
			
		ghostDict = {}
		for clue,gList in clueDict.items():
			for ghost in gList:
				gSet = ghostDict.get(ghost,set())
				gSet.add(clue)
				ghostDict[ghost] = gSet
				
		return clueDict,ghostDict
		
	def validClue(self,clue):
		return clue in self.clueSet
		
	def hasClue(self,clue):
		return clue in self.foundClues
		
	def addClue(self,clue):
		self.foundClues.add(clue)
		
	def removeClue(self,clue):
		self.foundClues.remove(clue)
		
	def reset(self):
		self.foundClues = set()
		
	def getPossibleGhosts(self):
		if(len(self.foundClues) == 0):
			return self.ghostSet
		
		r = None
		for clue in self.foundClues:
			if(r is None):
				r = self.clueDict[clue]
			else:
				r = r.intersection(self.clueDict[clue])
		return set(r)
		
	def getGhostClues(self):
		possibleGhosts = self.getPossibleGhosts()
		r = {}
		for g in sorted(possibleGhosts):
			r[g] = self.ghostDict[g] - self.foundClues
		return r
		
	def getRemainingClues(self):
		r = set()
		for ghost,clues in self.getGhostClues().items():
			for c in clues:
				r.add(c)
		return r
	
	def showInfo(self):
		for ghost, clues in self.getGhostClues().items():
			print("%12s => %s" % (ghost, clues))
			
	def showClueInfo(self):
		possible = self.getRemainingClues()
		if(possible):
			print("Possible Remaining clues %s" % possible)
		impossible = self.clueSet - possible - self.foundClues
		
		if(impossible):
			print("Impossible clues %s" % (impossible))
		
		if(self.foundClues):
			print("Known clues %s" % self.foundClues)
			
	def showHelp(self):
		print("Commands: reset info clues ghosts help quirks questions about")
		print("\treset: remove all clues")
		print("\tinfo: show remaining <ghost,clue> pairs")
		print("\tghosts: show traits of remaining ghosts")
		print("\tclues: show remaining/entered/impossible clues")
		print("\tquestions: show valid questions to ask Ouija Board")
		print("\tabout: about this program")
		print("Type clues like this:",self.clueSet)
		print("Entering a clue a second time will remove it")
		
	def showQuirks(self):
		ghostClues = self.getGhostClues()
		for g in sorted(self.getPossibleGhosts()):
			print("%12s: %s" % (g,ghostClues[g]))
			
			self.widthAwarePrint(self.ghostInfo[g])
			print("-"*25)
	def showQuestions(self):
		self.widthAwarePrint(
"""How old are you?
Who did you kill?
How long have you been dead?
How many people are in this room?
Where is your room?
""")

	def showAbout(self):
		self.widthAwarePrint(		
"""Phasmophobia Deduction Console is designed to automate deduction of remaining clues and possible ghosts. Find what clues are still possible, and what ghost behaviors you should look for.
		
Based on v0.174 (10/25/2020)
	
Information sourced from phasmophobia.fandom.com""")
	
	def widthAwarePrint(self,s,width=65):
		lines = s.split("\n")
		for line in lines:
			words = line.split(" ")
			usedWidth = 4
			print("\t",end="")
			for w in words:
				wLen = len(w) + 1
				if usedWidth+wLen > width:
					print()
					usedWidth = 4
					print("\t",end="")
				
				print(w,end=" ")
				usedWidth += wLen
			print()
		
	def repl(self):
		self.showInfo()
		self.showClueInfo()
		while True:
			cmd = input(f"\n({len(self.foundClues)}/3)>").strip().lower()
			if(self.validClue(cmd)):
				if(self.hasClue(cmd)):
					self.removeClue(cmd)
					print(f"{cmd} removed from clues.")
					self.showInfo()
					print()
					self.showClueInfo()
				elif(cmd in self.getRemainingClues()):
					self.addClue(cmd)
					print(f"{cmd} added to clues.")
					self.showInfo()
					print()
					self.showClueInfo()
				else:
					print(f"{cmd} is an impossible clue.")
					
			elif(cmd == "reset"):
				self.reset()
			elif(cmd == "info"):
				self.showInfo()
			elif(cmd == "clues"):
				self.showClueInfo()
			elif(cmd == "ghosts"):
				self.showQuirks()
			elif(cmd == "questions"):
				self.showQuestions()
			elif(cmd == "help"):
				self.showHelp()
			elif(cmd == "about"):
				self.showAbout()
			else:
				print("Unknown command, type 'help'")
				
					
def main():
	m = Mission()
	m.repl()
	
if __name__ == "__main__":
	main()