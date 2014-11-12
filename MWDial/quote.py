import re


class Quote:

    def __init__(self):
        self.topic = None
        self.speaker = None
        self.dial = None
        self.result = None
        self.race = None
        self.class_ = None
        self.gender = None
        self.cell = None
        self.faction = None
        self.rank = None
        self.pcfaction = None
        self.pcrank = None
        self.mindisp = None
        self.var1 = None
        self.var2 = None
        self.var3 = None
        self.var4 = None
        self.var5 = None
        self.var6 = None
        self.sharedby = None
        self.choicenum = None
        self.callschoices = []
        self.choicestext = []
        self.questrel = None
        self.queststages = []
        self.skillcheck = None
        self.firsttime = False
        self.itemreq = None
        self.goodbye = False
        self.dispmod = None
        self.itemadd = []
        self.itemrmv = []

    def tablerow(self, layout):
        if layout == "faction":
            return('|-\n| ' + self.rank + ' || ' + self.cell + ' || ' + self.class_ + ' || ' + str(self.mindisp)
                   + ' || "' + self.dial + '" || ' + self.var1)

        elif layout == "person":
            return('*\'\'\'' + self.topic + ':\'\'\'\n' + self.tablerow("personcont"))

        elif layout == "personcont":
            return ":" + self.addvariables()

        elif layout == "response":
            return self.addvariables()

        elif layout == "class":
            return('|-\n| ' + self.topic + ' || ' + self.faction + ' || ' + str(self.mindisp)[:-2]
                   + ' || "' + self.dial + '" || ' + self.var1)

    def processvars(self):
        for var in [self.var1, self.var2, self.var3, self.var4, self.var5, self.var6]:
            if var.startswith("Function Choice"):
                self.choicenum = int(var[var.find("=") + 2])
            elif var.startswith("Journal"):
                self.questrel = var[8:var.index(" ", 8)]
                self.queststages.append(str(var[var.index(" ", 8) + 1:]))
            elif var.startswith("Function PC"):
                self.skillcheck = var[12:]
            elif var.startswith("Function Talked To PC"):
                if var[len(var)-1:] == "0":
                    self.firsttime = True
            elif var.startswith("Item"):
                self.itemreq = var[5:var.index(' ', 6)]

        for result in self.result.splitlines():
            if result.startswith("Choice"):
                choicetext = []
                self.callschoices = [int(num) for num in re.findall(r"\b[1-9]\b", result)]
                for num in self.callschoices:
                    choicetext.append(result[result.index('"') + 1:result.index(str(num)) - 2])
                    result = result[result.index(str(num)) + 2:]
                self.choicestext = choicetext
            elif result.startswith("Goodbye"):
                self.goodbye = True
            elif result.lower().startswith("moddisposition"):
                self.dispmod = result[15:]
            elif result.lower().startswith("player->add"):
                self.itemadd.append(result[16:])
            elif result.lower().startswith("player->rem"):
                self.itemrmv.append(result[19:])

    def addvariables(self):
        assembled = ""
        if self.firsttime:
            assembled += '(First time speaking to you) '

        if self.skillcheck:
            assembled += '(With ' + self.skillcheck + ') '

        if self.mindisp > 0:
            assembled += '(Disposition at least ' + str(self.mindisp)[:-2] + ') '

        assembled += '\'\'"' + self.dial + '"\'\''

        if self.goodbye:
            assembled += " \'\'\'{{hover|You are forced to end dialogue.|Goodbye.}}\'\'\'"

        if self.dispmod:
            if "-" in self.dispmod:
                assembled += " (Disposition down by " + str(self.dispmod).strip(" -") + ")"
            else:
                assembled += " (Disposition up by " + str(self.dispmod).strip() + ")"

        if self.itemadd:
            addtext = " (You receive"
            for item in self.itemadd:
                addtext += " " + item
            assembled += addtext + ")"

        if self.itemrmv:
            rmvtext = " (You lose"
            for item in self.itemrmv:
                rmvtext += " " + item
            assembled += rmvtext + ")"

        return assembled

    def lineconditions(self):
        if self.questrel:
            print "Following line requires Journal " + self.questrel + " status " + str(self.queststages)
        if self.pcfaction:
            if self.pcrank:
                print "If you are of " + self.pcrank + " rank in the " + self.pcfaction + " faction:"
            else:
                print "If you're a member of " + self.pcfaction
        if self.itemreq:
            print "If you have item " + self.itemreq


class Topic:
    topics = []

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.starttable()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        endtable()

    def starttable(self, layout, header=None):
        if layout == "faction":
            return(':{| class="wikitable collapsible collapsed" align="center"\n! width="200px" | '
                   + self.name + '\n|-\n! scope="col" width="10%" | Rank\n! scope="col" width="15%" | '
                   + 'Location\n! scope="col" width="6%" align="center" | Class\n! scope="col" '
                   + 'width="3%" align="center" | Disp\n! scope="col"| Quote\n! scope="col" width="15%"| '
                   + 'Other Conditions\n|-')
        elif layout == "person":  # Topic, Disposition, Dialogue, Result, Other
            return(':{| class="wikitable collapsible collapsed" align="center"\n! width="200px" | '
                   + header + '\n|-\n! scope="col" width="10%" | Topic\n! scope="col" width="3%" align="center" | '
                   + 'Disposition\n! scope="col" | Dialogue\n! scope="col" '
                   + 'width="15%" align="center" | Result\n! scope="col" width="15%"| Other Conditions\n|-')
        elif layout == "class":  # Topic, Faction, Disposition, Dialogue, Other
            return(':{| class="wikitable collapsible collapsed" align="center"\n! width="200px" | '
                   + header + '\n|-\n! scope="col" width="10%" | Topic\n! scope="col" width="15%" | '
                   + 'Faction\n! scope="col" width="3%" align="center" | Disp\n! '
                   + 'scope="col"| Quote\n! scope="col" width="15%"| Other Conditions\n|-')
        else:
            return None


def endtable():
    print('|}\n')
