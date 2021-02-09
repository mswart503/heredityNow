import pygame, random, pygame.font, math, pickle, pygame.gfxdraw

# Global variables
red = (249, 65, 68)
orangered = (243, 114, 44)
orange = (248, 150, 30)
orangelite = (255, 176, 79)
yellow = (249, 199, 79)
green = (70, 175, 145)
purple = (128, 74, 103)
white = (235, 235, 235)
fieldcolor = (100, 100, 100)
grey = (214, 214, 214)
black = (32, 34, 28)
sidecolor = grey
gap = 10
cardwidth = 100
cardheight = 150
singleplayer = True
cardcolor = (20, 20, 20)

# stole from stack overflow to outline text
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points
def render(text, font, gfcolor=None, ocolor=None, opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

# stole from stack overflow to round corners
def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


class Cardslot:
    def __init__(self, color, x, y, width, height, card, isEmpty, name='', strength='', priority='',
                 meleetext='', abilitytext='', tokentext='', background = '', image='', character='', side=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.card = card
        self.isEmpty = isEmpty
        self.name = str(name)
        self.strength = str(strength)
        self.priority = priority
        self.meleetext = meleetext
        self.abilitytext = abilitytext
        self.tokentext = tokentext
        self.detailwidth = self.width * 2
        self.detailheight = self.height * 2
        self.image = image
        self.character = character
        self.font = 'alagard.ttf'
        self.side = side


        # New Fav -> 'athelas'
        # Now doesn't work for some reason --> Strong font, probably my fav #'oriyamnttc'
        # looks more like fantasy text -> 'noteworthyttc'
        # Formal, but nice -> 'ptserifttc'
        # Looks like hyroglyphics a bit, could be good for story mode-> 'skia'

    def draw(self, window, outline=None, selected=None, decision=None, token=None, detail=None, mycard=None, oppcard=None, facedown=None, char=None, title=None, imagetextsize=None):

        # call method to draw the card on screen
        if outline:
            if char:
                outlinerect = pygame.Rect(self.x+3, self.y +3, self.width-2, self.height-6)
                draw_rounded_rect(window,outlinerect,self.color,10)
            else:
                outlinerect = pygame.Rect(self.x, self.y, self.width+4, self.height+4)
                draw_rounded_rect(window, outlinerect, black, 10)

        therect = pygame.Rect(self.x+2, self.y+2, self.width-1, self.height-1)
        draw_rounded_rect(window, therect, self.color, 7)
        #pygame.draw.rect(window, self.color, (self.x+4, self.y+4, self.width-8, self.height-8))
        if char:
            try:
                if self.priority == "Day":
                    if selected:
                        background = pygame.image.load("Day_Night_Images/sunselected.jpg")

                    elif decision:
                        background = pygame.image.load("Day_Night_Images/sundecision.jpg")

                    else:
                        background = pygame.image.load("Day_Night_Images/sun.jpg")

                else:
                    if selected:
                        background = pygame.image.load("Day_Night_Images/moonselected.jpg")
                    elif decision:
                        background = pygame.image.load("Day_Night_Images/moondecision.jpg")
                    else:
                        background = pygame.image.load("Day_Night_Images/moon.jpg")
                character = pygame.image.load(self.character)
                window.blit(background, (self.x+6,self.y+6))
                window.blit(character, (self.x+self.width/2-(character.get_width()/2)-1, self.y+(self.height/2-character.get_height()/2)))
            except:
                pass
        if self.name != '':

            namecolor = (199, 15, 2)
            if title:
                fontsize = 50
            else:
                fontsize = 30
            nfont = pygame.font.Font(self.font, fontsize)
            nametext = nfont.render(str(self.name), 1, namecolor)
            while nametext.get_width() >= self.width - 10:
                fontsize -= 1
                nfont = pygame.font.Font(self.font, fontsize)
                nametext = nfont.render(str(self.name), 1, namecolor)
            while nametext.get_height() >= self.height - 6:
                fontsize -= 1
                nfont = pygame.font.Font(self.font, fontsize)
                nametext = nfont.render(str(self.name), 1, namecolor)
            if char:
                window.blit(render(str(self.name), nfont, gfcolor=white, ocolor=black),
                            (self.x + (self.width / 2 - nametext.get_width() / 2),
                             self.y + (self.height / 2 - nametext.get_height() / 2)+50))

            else:
                window.blit(render(str(self.name), nfont, gfcolor=white, ocolor=black), (self.x + (self.width / 2 - nametext.get_width() / 2),
                                                                                         self.y + (self.height / 2 - nametext.get_height() / 2)))


        if self.strength != '':
            sfontsize = 25
            sfont = pygame.font.Font(self.font, sfontsize)
            strengthdisp = sfont.render(str(self.strength), 1, white)
            while strengthdisp.get_width() >= self.width-8:
                sfontsize -= 1
                sfont = pygame.font.Font(self.font, sfontsize)
                strengthdisp = sfont.render(self.strength, 1, yellow)
            window.blit(render(self.strength, sfont, gfcolor=white, ocolor=black), (self.x + 4, self.y + 4))

        if self.tokentext != '':
            pfontsize = 15
            pfont = pygame.font.Font(self.font, pfontsize)
            tokentext = pfont.render(self.tokentext, 1, yellow)
            while tokentext.get_width() >= self.width:
                pfontsize -= 1
                pfont = pygame.font.Font(self.font, pfontsize)
                tokentext = pfont.render(self.tokentext, 1, yellow)
            window.blit(tokentext, (self.x + (self.width - gap * 4), self.y+4))

        if facedown:
            therect = pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6)
            draw_rounded_rect(window, therect, self.color, 10)
            titletext = "elf"
            fontsize = 30
            nfont = pygame.font.Font(self.font, fontsize)
            titletext = nfont.render(titletext, 1, (255,255,255))
            window.blit(titletext, (self.x + (self.width / 2 - titletext.get_width() / 2),
                                   self.y + (self.height / 2 - titletext.get_height() / 2)))

    def settokentext(self,newtext):
        if self.tokentext != "":
            self.tokentext = self.tokentext+newtext
        else:
            self.tokentext = newtext

    def blankOut(self):
        self.color = (255, 255, 255)
        self.card = None
        self.isEmpty = True
        self.name = ""
        self.strength = ""
        self.priority = ""
        self.meleetext = ""
        self.abilitytext = ""

    def isOver(self, pos):
        # pos is the mouse position, or a tuple of x,y coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class PowerScoreboard:
    def __init__(self, x, y):
        self.daycoin = pygame.image.load("Day_Night_Images/SunCoinScoreboard.png")
        self.nightcoin = pygame.image.load("Day_Night_Images/MoonCoinScoreboard.png")
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.backgroundcolor = black
        #self.borderRect = pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+3)
        #self.interiorRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.opdaypowerText = 0
        self.opnightpowerText = 0
        self.mydaypowerText = 0
        self.mynightpowerText = 0
        self.font = 'alagard.ttf'


    def draw(self, window, daypoweradvantage, nightpoweradvantage):
        opdaypowerloc = (self.x+40, self.y+40)
        opnightpowerloc = (self.x+140, self.y+40)
        mydaypowerloc = (self.x+40, self.y+130)
        mynightpowerloc = (self.x+140, self.y+130)
        #draw_rounded_rect(window, self.borderRect, self.backgroundcolor, 7)
        #draw_rounded_rect(window, self.interiorRect, sidecolor, 7)
        tfont = pygame.font.Font(self.font, 20)
        nfont = pygame.font.Font(self.font, 40)
        nfontoutline = nfont.render(str(self.opdaypowerText), 1, black)
        window.blit(render("Opponent's Power", tfont, gfcolor=white, ocolor=black), (self.x+20, self.y))
        window.blit(render("Your Power", tfont, gfcolor=white, ocolor=black), (self.x+50, self.y+95))

        #draw coins:

        if daypoweradvantage == "my":
            window.blit(self.daycoin, (mydaypowerloc[0] - self.daycoin.get_width()/2+nfontoutline.get_width()/2, mydaypowerloc[1]-self.daycoin.get_height()/2+nfontoutline.get_height()/2))
        elif daypoweradvantage == "op":
            window.blit(self.daycoin, (opdaypowerloc[0] - self.daycoin.get_width()/2+nfontoutline.get_width()/2, opdaypowerloc[1]-self.daycoin.get_height()/2+nfontoutline.get_height()/2))
        if nightpoweradvantage == "my":
            window.blit(self.nightcoin, (mynightpowerloc[0]- self.nightcoin.get_width()/2+nfontoutline.get_width()/2,mynightpowerloc[1]-self.nightcoin.get_height()/2+nfontoutline.get_height()/2))
        elif nightpoweradvantage == "op":
            window.blit(self.nightcoin, (opnightpowerloc[0]- self.nightcoin.get_width()/2+nfontoutline.get_width()/2,opnightpowerloc[1]-self.nightcoin.get_height()/2+nfontoutline.get_height()/2))

        nfont = pygame.font.Font(self.font, 40)
        # opdaypower
        window.blit(render(str(self.opdaypowerText), nfont, gfcolor=white, ocolor=black),
                    opdaypowerloc)

        # opnightpower
        window.blit(render(str(self.opnightpowerText), nfont, gfcolor=white, ocolor=black),
                    opnightpowerloc)

        # mydaypower
        window.blit(render(str(self.mydaypowerText), nfont, gfcolor=white, ocolor=black),
                    mydaypowerloc)

        #opdaypower
        window.blit(render(str(self.mynightpowerText), nfont, gfcolor=white, ocolor=black),
                    mynightpowerloc)


    def updatevalues(self, opdaypower, opnightpower, mydaypower, mynightpower):
        self.opdaypowerText = opdaypower
        self.opnightpowerText = opnightpower
        self.mydaypowerText = mydaypower
        self.mynightpowerText = mynightpower


class ImageBox:
    def __init__(self,image, x, y, text, fontsize, outlinethickness):
        self.image = image
        self.x = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.outlinethickness = outlinethickness

    def draw(self, window, textYshift=0, color=(199, 15, 2), textoutlinecolor=black, textinsidecolor=yellow):
        if self.image != '':
            img = pygame.image.load(self.image)
            window.blit(img, (self.x, self.y))
            opxchoice = self.fontsize/15
            font = "alagard.ttf"

            nfont = pygame.font.Font(font, self.fontsize)
            nametext = nfont.render(self.text, 1, color)
            while nametext.get_width() >= img.get_width() - 8:
                self.fontsize -= 1
                nfont = pygame.font.Font(font, self.fontsize)
                nametext = nfont.render(self.text, 1, color)
            while nametext.get_height() >= img.get_height() - 6:
                self.fontsize -= 1
                nfont = pygame.font.Font(font, self.fontsize)
                nametext = nfont.render(self.text, 1, color)
            window.blit(render(self.text, nfont, gfcolor=textinsidecolor, ocolor=textoutlinecolor, opx=self.outlinethickness),
                        (self.x + (img.get_width() / 2 - nametext.get_width() / 2),
                         self.y + (img.get_height() / 2 - nametext.get_height() / 2)+textYshift))


class PriorityCoin:
    def __init__(self, centerx, centery, radius, priority, image=None):
        self.centerx = int(centerx)
        self.centery = int(centery)
        self.radius = int(radius)
        self.priority = int(priority)
        try:
            self.image = image
        except:
            pass


    def draw(self, window, highlight=''):
        if self.image is not None:
            coinimg = pygame.image.load(self.image)
            window.blit(coinimg, (self.centerx - (coinimg.get_width() / 2) + 1, self.centery - (coinimg.get_height() / 2) + 1))

        else:
            if highlight != '':
                pygame.draw.circle(window, (163, 140, 194), (self.centerx, self.centery), self.radius + 3)
                pygame.draw.circle(window, (255, 255, 255), (self.centerx, self.centery), self.radius)
            else:
                pygame.draw.circle(window, (0, 0, 0), (self.centerx, self.centery), self.radius + 3)
                pygame.draw.circle(window, (255, 255, 255), (self.centerx, self.centery), self.radius)
            if self.priority:
                fontsize = 30
                nfont = pygame.font.Font('alagard.ttf', fontsize)
                nametext = nfont.render("P", 1, (0, 0, 0))
                window.blit(nametext,
                            (self.centerx - (nametext.get_width() / 2) + 1, self.centery - (nametext.get_height() / 2) + 1))

    def isOver(self, pos):
        # pos is the mouse position, or a tuple of x,y coordinates
        if pos[0] > (self.centerx-self.radius) and pos[0] < (self.centerx+self.radius):
            if pos[1] > self.centery-self.radius and pos[1] < self.centery + self.radius:
                return True
        return False


class Textbox:
    def __init__(self, color, x, y, width, height, text, fontsize):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = 'alagard.ttf'
        self.fontsize = fontsize

        self.renderedfont = pygame.font.Font(self.font, fontsize)

    def draw(self, window, outline=None, selected=None, decision=None, blank=None, textonly=False):
        if not textonly:
            if outline:
                therect = pygame.Rect(self.x - 2, self.y - 2, self.width +4, self.height +4)
                draw_rounded_rect(window, therect, black, 7)

            if selected:
                pygame.draw.rect(window, (163, 140, 194), (self.x - 4, self.y - 4, self.width + 8, self.height + 8))
            if decision:
                pygame.draw.rect(window, (253, 109, 61), (self.x - 4, self.y - 4, self.width + 8, self.height + 8))

            if blank:
                pass
            else:
                therect = pygame.Rect(self.x, self.y, self.width, self.height)
                draw_rounded_rect(window, therect, self.color, 7)

        if self.text != '' or self.text != None:
            lines = self.text.split(" ")
            linearray = []
            while len(lines) > 0:
                line = ""
                while len(line) < self.width/11:
                    try:
                        if len(lines[0]) + len(line) > self.width/11:
                            break

                        else:
                            line = line + " " + lines.pop(0)
                    except:
                        break

                linearray.append(line)

            fontsize = 20

            originalfont = pygame.font.Font(self.font, fontsize)
            counter = 0
            for lineitem in linearray:
                oritext = originalfont.render(lineitem, 1, (0, 0, 0))
                # window.blit(render("Opponent's Power", tfont, gfcolor=white, ocolor=black), (self.x + 20, self.y))
                # window.blit(render("Your Power", tfont, gfcolor=white, ocolor=black), (self.x + 50, self.y + 95))
                text = originalfont.render(lineitem, 1, (0, 0, 0))
                window.blit(render(lineitem, self.renderedfont, gfcolor=white, ocolor=black), (self.x + (self.width / 2 - text.get_width() / 2),
                                   (self.y + gap / 2 + (oritext.get_height() * counter))))
                counter += 1


class Card:
    def __init__(self, name, strength, priority, abilityid, token, meleecheck, abilitytext, activeability, isEmpty, serial):
        self.name = name
        self.strength = strength
        self.priority = priority
        self.abilityid = abilityid
        self.token = token
        self.meleecheck = meleecheck
        self.abilitytext = abilitytext
        self.isEmpty = isEmpty
        self.serial = serial
        self.activeability = activeability

    def blank_out(self):
        self.name = ""
        self.strength = ""
        self.priority = ""
        self.abilityid = ""
        self.token = False
        self.abilitytext = ""
        self.isEmpty = True

    def get_name(self):
        return self.name

    def set_name(self, newname):
        self.name = newname

    def get_strength(self):
        return self.strength

    def set_strength(self, newstrength):
        self.strength = newstrength

    def get_priority(self):
        return self.priority

    def set_priority(self, newpriority):
        self.priority = newpriority

    def get_abilityid(self):
        return self.abilityid

    def set_abilityid(self, newabilityid):
        self.abilityid = newabilityid

    def get_token(self):
        return self.token

    def set_token(self, newtoken):
        self.token = newtoken


class Board:
    def __init__(self, cardsinplay, totalcardlist, decklist):
        self.cardsinplay = cardsinplay  # the number of cards delt to hands and created on field
        self.totalcardlist = totalcardlist
        self.decklist = decklist
        self.deck = Deck(totalcardlist, decklist)
        self.window = pygame.display.set_mode((1200, 700))
        self.myhand = Hand((2 * gap), self.window.get_height() - (1 * (cardheight + (2 * gap))), "my")
        self.ophand = Hand((2 * gap), (2 * gap), "op")
        self.myPassHandselected = False
        self.opPassHandselected = False
        self.myfield = Field(8, (2 * gap), (self.myhand.handy - (2 * gap) - cardheight)+1, "Backgrounds/myfieldarea.jpeg", "my")
        self.opfield = Field(8, (2 * gap)-1, (self.ophand.handy + (2 * gap) + cardheight), "Backgrounds/opfieldarea.jpeg", "op")
        self.myhandCardslots = []
        self.ophandCardslots = []
        self.myselectedCardslot = Cardslot(yellow, 0, 0, 0, 0, None, True)
        self.opselectedCardslot = Cardslot(yellow, 0, 0, 0, 0, None, True)
        self.checkmycardselected = False
        self.checkopcardselected = False
        self.ophandArea = Cardslot((100, 102, 105), self.ophand.handx - gap, self.ophand.handy - gap,
                                   8 * (cardwidth + gap) + gap, cardheight + (gap * 2), None, False)
        self.opfieldArea = Cardslot(fieldcolor, self.opfield.fieldx - gap, self.opfield.fieldy + gap / 2+5,
                                    8 * (cardwidth + gap) + gap, cardheight + (gap * 2), None, False)
        self.myfieldArea = Cardslot(fieldcolor, self.myfield.fieldx - gap, self.myfield.fieldy - gap * 1.5-1,
                                    8 * (cardwidth + gap) + gap, cardheight + (gap * 2), None, False)
        self.myhandArea = Cardslot((255, 255, 255), self.myhand.handx - gap, self.myhand.handy - gap,
                                   8 * (cardwidth + gap) + gap, cardheight + (gap *2 ) , None, False)
        self.myPassHand = Cardslot((200, 200, 200), self.myhandArea.width + self.myhandArea.x + gap, self.myhand.handy, 75,
                                   75, None, False, 'Play Card')
        self.opPassHand = Cardslot((200, 200, 200), self.ophandArea.width + self.ophandArea.x + gap,
                                   self.ophand.handy + cardheight - 75, 75, 75, None, False, 'Play Card')
        self.mypower = [0, 0]
        self.oppower = [0, 0]
        self.dayPowerAdvantage = ""
        self.nightPowerAdvantage = ""
        self.textdisplay = "Welcome to Spirit"
        self.textarea = Textbox(sidecolor,
                                self.myhandArea.width + self.myhandArea.x + (2 * gap) + self.myPassHand.width,
                                (self.window.get_height() / 2) - 100, 200, 200, self.textdisplay, 20)
        self.myabilityarea = Textbox(sidecolor,
                                     self.myhandArea.width + self.myhandArea.x + (2 * gap) + self.myPassHand.width,
                                     self.textarea.y + self.textarea.height + (3 * gap), self.textarea.width,
                                     self.textarea.height, "-", 20)
        self.powerarea = PowerScoreboard(self.textarea.x, 20)
        self.currentAbilityArray = []
        self.eventArray = []
        self.endofRoundArray = []
        self.cardchangesDict = dict()

    def redrawwindow(self, myselectedcard=None):
        bg = pygame.image.load("Backgrounds/dayForest.jpeg")
        self.window.blit(bg, (0, 0))
        self.opfield.build_field(self.window)
        self.myfield.build_field(self.window)
        self.powerarea.draw(self.window, self.dayPowerAdvantage, self.nightPowerAdvantage)
        self.myhand.build_hand(self.window)
        self.textarea.draw(self.window, blank=True)
        self.myabilityarea.draw(self.window, blank=True)
        try:
            self.opselectedCardslot.draw(self.window, outline=True, char=True)
        except:
            pass

        if myselectedcard is not None:
            myselectedcard.draw(self.window, outline=True, char=True, selected=True)

        pygame.display.flip()

    def dictionaryLoad(self):
        self.cardchangesDict["meleeremoval"] = []
        self.cardchangesDict["barbarian1kills"] = 0
        self.cardchangesDict["barbarian2kills"] = 0
        for card in self.myhandCardslots:
            self.cardchangesDict[card.card.serial] = 0
        for card in self.ophandCardslots:
            self.cardchangesDict[card.card.serial] = 0

    def setup(self):
        pygame.display.set_caption('spirit v0.5')
        bg = pygame.image.load("Backgrounds/dayForest.jpeg")
        self.window.blit(bg, (0, 0))
        dayornightstart = self.colorchoice(self.window)
        if dayornightstart == "day":
            self.dayPowerAdvantage = "my"
            self.nightPowerAdvantage = "op"
        else:
            self.nightPowerAdvantage = "my"
            self.dayPowerAdvantage = "op"
        self.myhand, self.ophand = self.deck.deal_hands(self.cardsinplay, self.myhand, self.ophand, 7)
        self.myhand.sort_hand()
        self.ophand.sort_hand()
        self.redrawwindow()
        self.dictionaryLoad()

        return self.window

    def colorchoice(self, window):
        choicebg = Textbox((170,170,130), 400, 250, 400, 200,"Do you want to start with Day priority or Night priority? Your opponent will get the other.", 20)
        choicebg.draw(window,outline=True)
        suncoin = PriorityCoin(choicebg.x+125,choicebg.y+120,50,True,image="Day_Night_Images/SunCoin.png")
        mooncoin = PriorityCoin(choicebg.x+275,choicebg.y+120,50,True,image="Day_Night_Images/MoonCoin.png")
        suncoin.draw(window)
        mooncoin.draw(window)
        pygame.display.flip()
        clicklisten=False
        while not clicklisten:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if clicklisten == True:
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if suncoin.isOver(pos):
                        sunchoice = PriorityCoin(choicebg.x+126,choicebg.y+122,50,True,image="Day_Night_Images/SunCoinSelected.png")
                        sunselector = Textbox((210, 210, 210), sunchoice.centerx - sunchoice.radius - 10,
                                               sunchoice.centery - sunchoice.radius - 60, sunchoice.radius * 2 + 20,
                                               sunchoice.radius * 2 + 80, "You start with Day Priority", 20)
                        sunselector.draw(self.window)
                        sunchoice.draw(self.window)
                        pygame.display.flip()
                        self.clicktocontinue(newX= 500, newY= 460)
                        clicklisten = True
                        return "day"
                    elif mooncoin.isOver(pos):
                        moonchoice = PriorityCoin(choicebg.x+276, choicebg.y + 120, 50, True,
                                                 image="Day_Night_Images/MoonCoinSelected.png")
                        moonselector = Textbox((210, 210, 210), moonchoice.centerx-moonchoice.radius-10, moonchoice.centery-moonchoice.radius-60,moonchoice.radius*2+20,moonchoice.radius*2+80,"You start with Night Priority", 20)
                        moonselector.draw(self.window)
                        moonchoice.draw(self.window)
                        pygame.display.flip()
                        self.clicktocontinue(newX= 500, newY= 460)
                        clicklisten= True
                        return "night"

    def aiCardSelect(self, opCardslots):
        cardselect = 0
        # Rule 1: Always try and play the strongest damaging card first:
        meleeprioritylist = ["bandit", "dragon", "barbarian", "nightwolf", "daywolf", "phoenix", "spearman"]
        for cardcheck in meleeprioritylist:
            for card in self.ophand.handArray:
                if card.card.abilityid == cardcheck:
                    return card
        if cardselect == 0:
        # Rule 2: Otherwise pick the highest strength card except a golem on an empty field
            pick = 0
            for card in self.ophand.handArray:
                if pick == 0:
                    pick = card
                else:
                    if int(pick.strength) < int(card.strength):
                        pick = card
            if pick != 0:
                return pick

    def clicktocontinue(self, newX=None, newY=None):
        signheight = 30
        x = self.textarea.x + 5
        y = self.textarea.y + self.textarea.height - signheight - 5
        if newX != None:
            x = newX
        if newY != None:
            y = newY
        clicksign = Cardslot(white, x, y, self.textarea.width - 10, signheight, None, False, name="Click Anywhere to Continue")
        clicksign.draw(self.window, outline=True)
        pygame.display.flip()
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clickevent.type == pygame.QUIT:
                    quit()
                if clicklisten == True:
                    break
                elif clickevent.type == pygame.MOUSEBUTTONDOWN:
                    clicklisten = True

        pygame.display.flip()

    def resetselectedvars(self):
        self.checkmycardselected = False
        self.checkopcardselected = False
        self.myPassHandselected = False
        self.opPassHandselected = False
        self.myhand.selectedArray = [False, False, False, False, False, False, False, False]

    def rotatehands(self,mylockedcard, oplockedcard):
        # one of the hands is ending up with and extra card and I don't know why yet.
        self.myhand.removeCard(mylockedcard) # Remove the locked card from my hand
        self.ophand.removeCard(oplockedcard) # remove the locked card from op hand
        holdop = self.ophand.copy()
        holdmy = self.myhand.copy()
        for card in holdop.handArray:
            self.ophand.removeCard(card)
        for card in holdmy.handArray:
            self.myhand.removeCard(card)
        for card in holdop.handArray:
            self.myhand.addCard(card.card)
        for card in holdmy.handArray:
            self.ophand.addCard(card.card)

        self.myhand.addCard(mylockedcard.card)
        self.ophand.addCard(oplockedcard.card)

    def updategametext(self, newtext):
        self.textarea.text = newtext
        self.redrawwindow()
        #self.textarea.draw(self.window, textonly=True)
        #pygame.display.flip()

    def updatemyabilitytext(self, newtext):
        self.myabilityarea.text = newtext
        self.redrawwindow()
        #self.myabilityarea.draw(self.window, textonly=True)
        #pygame.display.flip()


    def blankalltexts(self):
        self.updategametext("")
        self.updatemyabilitytext("")

    def deselectallcards(self):
        for myresetcard in self.myfield.fieldArray:
            myresetcard.draw(self.window, outline=True, char=True)
        for opresetcard in self.opfield.fieldArray:
            opresetcard.draw(self.window, outline=True, char=True)
        pygame.display.flip()

    def highlightcards(self, cardstoplay):
        for cards in cardstoplay:
            cards.draw(self.window, outline=True, selected=True, char=True)
        pygame.display.flip()

    def playmycard(self, cardtoplay):
        if cardtoplay not in self.myfield.fieldArray:
            self.myfield.fieldArray.append(cardtoplay)
            self.myfield.build_field(self.window)
            self.myhand.removeCard(cardtoplay)
            self.redrawwindow()
        self.abilityExecution(cardtoplay, "my")

    def playopcard(self, cardtoplay):
        if cardtoplay not in self.opfield.fieldArray:
            self.opfield.fieldArray.append(cardtoplay)
            self.opfield.build_field(self.window)
            self.ophand.removeCard(cardtoplay)
            self.redrawwindow()
        self.abilityExecution(cardtoplay, "op")

    def battlephase(self):
        # first executes Day turns

        # Check who has priority:
        self.advantagecheck()

        # Then pull day cards
        mycardstoplay = self.myfield.priorityArrays[0].copy()
        opcardstoplay = self.opfield.priorityArrays[0].copy()

        # Then get how many cards have to be played for each player
        mycurlength = len(mycardstoplay)
        opcurlength = len(opcardstoplay)

        # Then remove cards that don't have an active ability
        for card in mycardstoplay:
            if not card.card.activeability:
                mycardstoplay.remove(card)
        for card in opcardstoplay:
            if not card.card.activeability:
                opcardstoplay.remove(card)


        if self.dayPowerAdvantage == "my":
            if mycurlength == 1:
                cardtoplay = mycardstoplay.pop(0)
                self.playmycard(cardtoplay)

            elif mycurlength > 1:
                self.mychoicefunction(mycardstoplay)

            if opcurlength == 1:
                cardtoplay = opcardstoplay.pop(0)
                self.playopcard(cardtoplay)

            elif opcurlength > 1:
                self.opchoicefunction(opcardstoplay)

        elif self.dayPowerAdvantage == "op":
            if opcurlength == 1:
                cardtoplay = opcardstoplay.pop(0)
                self.playopcard(cardtoplay)

            elif opcurlength > 1:
                self.opchoicefunction(opcardstoplay)

            if mycurlength == 1:
                cardtoplay = mycardstoplay.pop(0)
                self.playmycard(cardtoplay)

            elif mycurlength > 1:
                self.mychoicefunction(mycardstoplay)


        # Now doing night priority

        # Check who has priority:
        self.advantagecheck()

        # Then pull night cards
        mycardstoplay = self.myfield.priorityArrays[1].copy()
        opcardstoplay = self.opfield.priorityArrays[1].copy()

        # Then get how many cards have to be played for each player
        mycurlength = len(mycardstoplay)
        opcurlength = len(opcardstoplay)

        # Then remove cards that don't have an active ability
        for card in mycardstoplay:
            if not card.card.activeability:
                mycardstoplay.remove(card)
        for card in opcardstoplay:
            if not card.card.activeability:
                opcardstoplay.remove(card)

        if self.nightPowerAdvantage == "my":
            if mycurlength == 1:
                cardtoplay = mycardstoplay.pop(0)
                self.playmycard(cardtoplay)

            elif mycurlength > 1:
                self.mychoicefunction(mycardstoplay)

            if opcurlength == 1:
                cardtoplay = opcardstoplay.pop(0)
                self.playopcard(cardtoplay)


            elif opcurlength > 1:
                self.opchoicefunction(opcardstoplay)

        elif self.nightPowerAdvantage == "op":
            if opcurlength == 1:
                cardtoplay = opcardstoplay.pop(0)
                self.playopcard(cardtoplay)


            elif opcurlength > 1:
                self.opchoicefunction(opcardstoplay)

            if mycurlength == 1:
                cardtoplay = mycardstoplay.pop(0)
                self.playmycard(cardtoplay)

            elif mycurlength > 1:
                self.mychoicefunction(mycardstoplay)

    def mychoicefunction(self, cardstoplay):

        while True:
            # if there is only 1 card left then play that card and break out of loop

            choicelength = len(cardstoplay)
            if choicelength == 1:
                currentcard = cardstoplay[0]
                self.playmycard(currentcard)
                break

            # while there are 2 or more cards to choose from, highlight all cards

            # Update game text to instruct user
            self.updategametext("A Priority Tie has occurred. Choose which card will go first")
            self.highlightcards(cardstoplay)


            # Listen for a click on any of the cards
            clicklisten = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:
                        for cardpick in cardstoplay:
                            if cardpick.isOver(pos):
                                if self.myfield.cardondeck == cardpick:
                                    self.playmycard(cardpick)
                                else:
                                    cardpick.draw(self.window, outline=True, char=True)
                                    pygame.display.flip()
                                    self.abilityExecution(cardpick, "my")

                                try:
                                    cardstoplay.remove(cardpick)
                                except:
                                    pass
                                clicklisten = True
                                self.blankalltexts()

    def opchoicefunction(self, cardstoplay):
        while True:
            # if there is only 1 card left then play that card and break out of loop
            choicelength = len(cardstoplay)
            if choicelength == 1:
                currentcard = cardstoplay[0]
                self.playopcard(currentcard)
                break
            else:
                count = -1
                for card in cardstoplay:
                    count += 1
                # randomly picks a card to go first
                try:
                    cardpick = random.randint(0, count)
                except:
                    cardpick = 0
                try:
                    choice = cardstoplay[cardpick]
                    if self.opfield.cardondeck == choice:
                        self.opfield.fieldArray.append(choice)
                        #self.ophandArea.draw(self.window, outline=True)
                        self.opfield.build_field(self.window)
                        self.ophand.handArray.remove(choice.card)
                        #self.ophand.build_hand(self.window)
                        pygame.display.flip()
                    else:
                        choice.draw(self.window, outline=True, char=True)
                        pygame.display.flip()
                    self.abilityExecution(choice, "op")
                    try:
                        cardstoplay.remove(choice)
                    except:
                        pass
                except:
                    break

    def aiDecision(self, abilityid, cardslot, defendingCard=None):

        if abilityid == "gorgon":
            # The AI will choose the highest strength card to reduce by half
            if not self.myfield.fieldArray:
                self.updategametext("Gorgon does not reduce")
                self.clicktocontinue()

            else:
                choice = 0
                for card in self.myfield.fieldArray:
                    if choice == 0:
                        choice = card
                    else:
                        if int(choice.strength) >= int(card.strength):
                            pass
                        else:
                            choice = card

                choice.draw(self.window, decision=True, char=True)
                pygame.display.flip()
                self.updategametext("Gorgon reduces " + choice.name + " by half")
                self.clicktocontinue()
                reducepercent = .5
                reduceamount = round(int(choice.strength) * reducepercent)
                if choice.card.serial not in self.cardchangesDict:
                    self.cardchangesDict[choice.card.serial] = 0
                self.cardchangesDict[choice.card.serial] = str(int(self.cardchangesDict[choice.card.serial]) - reduceamount)
                choice.strength = str(round(int(choice.strength) * reducepercent))
                if int(choice.strength) <= 0:
                    self.cardremoval(self.myfield, choice)

        elif abilityid == "forcedremove":
            # ai selects the lowest strength card to remove
            choice = 0
            for card in self.opfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) > int(card.strength):
                    choice = card

            if choice == 0:
                self.updategametext("There are no cards to remove, " + cardslot.name + " is discarded")
                self.clicktocontinue()
            else:
                self.updategametext("Opponent removes " + choice.name)
                choice.draw(self.window, selected=True, char=True)
                pygame.display.flip()
                self.clicktocontinue()
                self.cardremoval(self.opfield, choice)
                self.opfield.build_field(self.window)

        elif abilityid == "daywolf":
            # The ai checks if there are any cards it can defeat by melee left to right, if not it picks increase strength
            choice = 0
            for card in self.myfield.fieldArray:

                if int(card.strength) > 5:
                    pass
                else:
                    choice = card

            if choice == 0:
                self.updategametext("Opponent has chosen to increase Day Wolf's strength")
                self.clicktocontinue()
                cardslot.strength = str(8)
                cardslot.draw(self.window, outline=True, char=True)
                pygame.display.flip()
                self.cardchangesDict[cardslot.card.serial] = 0
                self.cardchangesDict[cardslot.card.serial] = self.cardchangesDict[cardslot.card.serial]+3
                self.cardchangesDict[cardslot.card.serial + "choice"] = "Passive"
                self.blankalltexts()
            else:
                self.updategametext("Opponent has chosen to give Day Wolf melee")
                self.clicktocontinue()
                self.cardchangesDict[cardslot.card.serial + "choice"] = "Melee"
                self.blankalltexts()

        elif abilityid == "nightwolf":
            # The ai checks if there are any cards it can defeat by melee left to right, if not it picks increase strength
            choice = 0
            for card in self.myfield.fieldArray:

                if int(card.strength) > 5:
                    pass
                else:
                    choice = card

            if choice == 0:
                self.updategametext("Opponent has chosen to increase Night Wolf's strength")
                self.clicktocontinue()
                cardslot.strength = str(8)
                cardslot.draw(self.window, outline=True, char=True)
                pygame.display.flip()
                self.cardchangesDict[cardslot.card.serial] = 0
                self.cardchangesDict[cardslot.card.serial] = self.cardchangesDict[cardslot.card.serial]+3
                self.cardchangesDict[cardslot.card.serial + "choice"] = "Passive"
                self.blankalltexts()
            else:
                self.updategametext("Opponent has chosen to give Night Wolf melee")
                self.clicktocontinue()
                self.cardchangesDict[cardslot.card.serial + "choice"] = "Melee"
                self.blankalltexts()

        elif abilityid == "beggarkingincrease":
            # the AI picks the lowest strength card and increases that one, left to right
            choice = 0
            for card in self.opfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) <= int(card.strength):
                    pass
                else:
                    choice = card
            try:
                self.cardchangesDict[choice.card.serial] = self.cardchangesDict[choice.card.serial]+5
            except:
                self.cardchangesDict[choice.card.serial] = 5
            choice.draw(self.window, decision=True, char=True)
            self.updategametext(cardslot.name + " increases " + choice.name)
            self.clicktocontinue()
            choice.strength = str(int(choice.strength) + 5)
            self.blankalltexts()

        elif abilityid == "beggarkingmelee":
            # the ai chooses the highest strength card and completes regular melee process
            choice = 0
            for card in self.opfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) < int(card.strength):
                    choice = card

            self.melee("op", choice)

        elif abilityid == "mybeggarking":
            # if the ai has any cards that can be defeated by a card meleeing, it chooses increase
            oploweststrength = 0
            for card in self.opfield.fieldArray:
                if oploweststrength == 0:
                    oploweststrength = card
                elif int(oploweststrength.strength) > int(card.strength):
                    oploweststrength = card
                else:
                    pass

            for card in self.myfield.fieldArray:
                if not self.opfield.fieldArray:
                    self.updategametext("The opponent chooses to have you melee immediately")
                    self.clicktocontinue()
                    return "melee"

                elif int(card.strength) > int(oploweststrength.strength):
                    self.updategametext("The opponent chooses to have you increase one of your cards by 5")
                    self.clicktocontinue()
                    return "increase"
                else:
                    pass
            self.updategametext("The opponent chooses to have you melee immediately")
            self.clicktocontinue()
            return "melee"

        elif abilityid == "golem":
            # the ai selects the lowest strength card to discard
            choice = 0
            for card in self.opfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) > int(card.strength):
                    choice = card
                else:
                    pass

            self.updategametext("Opponent discards " + choice.name + " to play Golem")
            self.clicktocontinue()

            self.cardremoval(self.opfield, choice)
            self.opfield.build_field(self.window)
            self.blankalltexts()

        elif abilityid == "barbarian":
            pass

        elif abilityid == "heretic":
            # Ai selects the highest strength card and increases it
            choice = 0
            for card in self.opfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) < int(card.strength):
                    choice = card
                else:
                    pass

            self.updategametext("Opponent increases " + choice.name + " by 5")
            choice.draw(self.window, selected=True, char=True)
            pygame.display.flip()
            self.clicktocontinue()
            self.cardchangesDict[choice.card.serial] = self.cardchangesDict[choice.card.serial]+5
            choice.strength = str(int(choice.strength) + 5)
            choice.draw(self.window, outline=True, char=True)
            self.opfield.build_field(self.window)
            self.myfield.build_field(self.window)

        elif abilityid == "myheretic":
            # if a card can be reduced and be destroyed pick that one, otherwise reduce the highest value
            choice = 0
            for card in self.myfield.fieldArray:

                if int(card.strength) <= 5:
                    choice = card
                    break
                elif choice == 0:
                    choice = card
                elif int(choice.strength) < int(card.strength):
                    choice = card
            self.updategametext("Because Heretic was defeated your Opponent reduces a card by 5. They choose "+ choice.name)
            choice.draw(self.window, selected=True, char=True)
            self.clicktocontinue()
            choice.strength = str(int(choice.strength) - 5)
            if int(choice.strength) <= 0:
                self.cardremoval(self.myfield, choice)
            pygame.display.flip()

        elif abilityid == "knight":
            # ai chooses lowest strength card on my field to assign
            choice = 0
            for card in self.myfield.fieldArray:
                if choice == 0:
                    choice = card
                elif int(choice.strength) > int(card.strength):
                    choice = card
            if choice != 0:
                self.updategametext("Opponent chooses " + choice.name + " to assign Knight to")
                self.clicktocontinue()
                choice.settokentext("K")
                self.cardchangesDict[cardslot.card.serial + "pick"] = [choice, "op"]
                self.myfield.build_field(self.window)
                pygame.display.flip()
                clicklisten = True

        elif abilityid == "dragon":
            # ai checks if using dragons ability will destroy it, it wont if it does
            # ai then checks if there are any cards it can destroy on the opponenets side, if so it does
            if int(cardslot.strength) == 1:
                self.updategametext("Dragon does not attack")
                self.clicktocontinue()
                pass
            else:
                choice = 0
                for card in self.myfield.fieldArray:
                    if card.card.abilityid == "ghostship":
                        if int(card.strength) <= 10:
                            choice = card
                            self.updategametext("Dragon attacks " + card.name)
                            card.draw(self.window, selected=True, char=True)
                            pygame.display.flip()
                            self.clicktocontinue()
                            self.cardremoval(self.myfield, choice)
                            if cardslot.card.serial not in self.cardchangesDict:
                                self.cardchangesDict[cardslot.card.serial] = -1
                            else:
                                self.cardchangesDict[cardslot.card.serial] = str(
                                    int(self.cardchangesDict[cardslot.card.serial]) - 1)
                            cardslot.strength = str(int(cardslot.strength) - 1)
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            return
                    elif int(card.strength) <= 5:
                        choice = card
                        self.updategametext("Dragon attacks " + card.name)
                        card.draw(self.window, selected=True, char=True)
                        pygame.display.flip()
                        self.clicktocontinue()
                        break
                    else:
                        pass
                if choice == 0:
                    self.updategametext("Dragon does not attack")
                    self.clicktocontinue()
                else:
                    self.cardremoval(self.myfield, choice)
                    if cardslot.card.serial not in self.cardchangesDict:
                        self.cardchangesDict[cardslot.card.serial] = -1
                    else:
                        self.cardchangesDict[cardslot.card.serial] = str(int(self.cardchangesDict[cardslot.card.serial]) - 1)
                    cardslot.strength = str(int(cardslot.strength) - 1)
                    self.myfield.build_field(self.window)
                    self.opfield.build_field(self.window)

        elif abilityid == "headsman":
            # the ai plays it on the opponents side
            self.updategametext("The Opponent plays Headsman on your side of the field")
            self.clicktocontinue()
            if self.myfield.fieldArray == []:
                self.myfield.addCardslotInTurn(cardslot)
                pygame.display.flip()
            else:
                self.forcedremovecard(cardslot, "my")
                self.cardremoval(self.opfield, cardslot)
                self.myfield.addCardslotInTurn(cardslot)
                self.opfield.build_field(self.window)
                self.myfield.build_field(self.window)
                self.blankalltexts()
                pygame.display.flip()

        elif abilityid == "madman":
            if cardslot.card.serial == "madman1":
                self.cardchangesDict["madman1side"] = "op"
            elif cardslot.card.serial == "madman2side":
                self.cardchangesDict["madman2side"] = "op"

        elif abilityid == "trolldefend":
            # If the attacker can defeat troll it does so, even if it dies as a result
            if cardslot.card.abilityid == "spearman":
                finaldmg = round(int(cardslot.strength) * .5)
            else:
                finaldmg = int(cardslot.strength)

            if finaldmg >= defendingCard.strength:
                return "attack"
            else:
                return "pass"

        elif abilityid == "meleeselect":
            # ai will only attack cards it can defeat starting with the strongest card it can kill, but it will
            # attack ghost ship, bandit and dragon (if it can get the kill) even if it means the attacker is destroyed
            cardtoreturn = None
            attackondeath = False
            attackerdmg = cardslot.strength
            defenderdmg = 0
            for card in self.myfield.fieldArray:
                defenderdmg = card.strength
                if card.card.abilityid == "bandit" or card.card.abilityid == "ghostship" or card.card.abilityid == "dragon":
                    attackondeath = True
                if card.card.abilityid == "ghostship":
                    attackerdmg = attackerdmg*2
                if card.card.abilityid == "spearman":
                    defenderdmg = math.ceil(card.strength/2)
                if card.strength > cardslot.strength:
                    pass
                elif cardslot.strength == defenderdmg and attackerdmg >= card.strength and attackondeath:
                    return card
                elif cardslot.strength > defenderdmg and attackerdmg >= card.strength:
                    return card

            return cardtoreturn

    def abilityExecution(self, cardslot, whoscard):

        if whoscard == "my":
            if cardslot == self.myfield.cardondeck:
                self.advantagecheck()

            if cardslot.card.abilityid == "barbarian":
                result = ""
                result = self.melee("my", cardslot)
                if result == "win":
                    try:
                        curbarbariankills = self.cardchangesDict[cardslot.card.serial]
                        curbarbariankills += 1
                        self.cardchangesDict[cardslot.card.serial] = curbarbariankills
                    except:
                        self.cardchangesDict[cardslot.card.serial] = 1
                    self.endofRoundArray.append(["barbarian", cardslot, whoscard])
                elif result == "lose" or result == "draw":
                    pass
            elif cardslot.card.abilityid == "frostgiant":
                self.endofRoundArray.append(["frostgiant", cardslot, whoscard])
            elif cardslot.card.abilityid == "gorgon":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    self.reducestrengthbypercent(cardslot, 50)
                    self.opfield.build_field(self.window)
                    self.myfield.build_field(self.window)
                else:
                    cardslot.draw(self.window, outline=True, char=True)
                    pygame.display.flip()
            elif cardslot.card.abilityid == "lightgolem":
                if len(self.myfield.fieldArray) >= 1:
                    self.updategametext("Select a card to sacrifice to give Light Golem melee, or click below to skip")
                    self.highlightcards(self.myfield.fieldArray)
                    skipbutton = Cardslot(white, self.textarea.x + 5,
                                          self.textarea.y + self.textarea.height - 30 - 5,
                                          self.textarea.width - 10, 30, None, False, name="Click to Skip")
                    skipbutton.draw(self.window, outline=True)

                    pygame.display.flip()
                    clicklisten = False
                    while clicklisten == False:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:

                                if skipbutton.isOver(pos):
                                    for resetcard in self.opfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    for resetcard in self.myfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    cardslot.draw(self.window, outline=True, char=True)
                                    pygame.display.flip()
                                    clicklisten = True

                                else:
                                    for card in self.myfield.fieldArray:
                                        if card == cardslot:
                                            pass
                                        elif card.isOver(pos):
                                            self.cardremoval(self.myfield, card)
                                            pygame.display.flip()
                                            self.melee("my", cardslot)
                                            clicklisten = True

            elif cardslot.card.abilityid == "darkgolem":
                if len(self.myfield.fieldArray) >= 1:
                    self.updategametext("Select a card to sacrifice to give Dark Golem melee, or click below to skip")
                    self.highlightcards(self.myfield.fieldArray)
                    skipbutton = Cardslot(yellow, self.textarea.x + 5,
                                          self.textarea.y + self.textarea.height - 30 - 5,
                                          self.textarea.width - 10, 30, None, False, name="Click to Skip")
                    skipbutton.draw(self.window, outline=True)

                    pygame.display.flip()
                    clicklisten = False
                    while clicklisten == False:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:

                                if skipbutton.isOver(pos):
                                    for resetcard in self.opfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    for resetcard in self.myfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    cardslot.draw(self.window, outline=True, char=True)
                                    pygame.display.flip()
                                    clicklisten = True

                                else:
                                    for card in self.myfield.fieldArray:
                                        if card == cardslot:
                                            pass
                                        elif card.isOver(pos):
                                            self.cardremoval(self.myfield, card)
                                            pygame.display.flip()
                                            self.melee("my", cardslot)
                                            clicklisten = True
            #elif cardslot.card.abilityid == "golem":
            #    if cardslot.card.serial == self.myselectedCardslot.card.serial:
            #        self.forcedremovecard(cardslot, "my")
            #    else:
            #        pass  # old Golem ability
            elif cardslot.card.abilityid == "dragon":
                result = ""
                result = self.reduceanystrengthbynumber(cardslot, 5, False)
                if result == "damage":
                    cardslot.strength = str(int(cardslot.strength) - 1)
                    self.myfield.build_field(self.window)
                    if int(cardslot.strength) <= 0:
                        self.cardremoval(self.myfield, cardslot)
                elif result == "skip":
                    cardslot.draw(self.window, outline=True, char=True)
                    pygame.display.flip()
            elif cardslot.card.abilityid == "seer":
                self.updategametext("Do you want to increase or decrease a card's strength by 1?")
                cardslot.draw(self.window, selected=True, char=True)
                select1 = Cardslot(yellow, self.myabilityarea.x + 10, self.myabilityarea.y + 10,
                                   self.myabilityarea.width - 20, 50, None, False, "Increase")
                select2 = Cardslot(yellow, self.myabilityarea.x + 10, self.myabilityarea.y + 10 + 60,
                                   self.myabilityarea.width - 20, 50, None, False, "Decrease")
                select3 = Cardslot(yellow, self.myabilityarea.x + 10, self.myabilityarea.y + 10 + 120,
                                   self.myabilityarea.width - 20, 50, None, False, "Skip")
                select1.draw(self.window, outline=True)
                select2.draw(self.window, outline=True)
                select3.draw(self.window, outline=True)
                pygame.display.flip()

                clicklisten = False
                while clicklisten == False:
                    for clickevent in pygame.event.get():
                        if clicklisten == True:
                            break
                        pos = pygame.mouse.get_pos()
                        if clickevent.type == pygame.MOUSEBUTTONDOWN:
                            if select1.isOver(pos):
                                result = ""
                                result = self.increaseanystrengthbynumber(cardslot, 1)
                                clicklisten = True
                            elif select2.isOver(pos):
                                result = ""
                                result = self.reduceanystrengthbynumber(cardslot, 1, True)
                                clicklisten = True

                            elif select3.isOver(pos):
                                clicklisten = True

                cardslot.draw(self.window, outline=True, char=True)
                pygame.display.flip()
            elif cardslot.card.abilityid == "headsman":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    self.updategametext("Do you want to play Headsman on your side or your opponents?")
                    select1 = Cardslot(yellow, self.myabilityarea.x + 10, self.myabilityarea.y + 10,
                                       self.myabilityarea.width - 20, 50, None, False, "My Field")
                    select2 = Cardslot(yellow, self.myabilityarea.x + 10, self.myabilityarea.y + 70,
                                       self.myabilityarea.width - 20, 50, None, False, "Opponent's Field")
                    self.updatemyabilitytext(" ")
                    select1.draw(self.window, outline=True)
                    select2.draw(self.window, outline=True)
                    pygame.display.flip()

                    clicklisten = False
                    while not clicklisten:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                if select1.isOver(pos):
                                    self.blankalltexts()
                                    self.forcedremovecard(cardslot, "my")
                                    cardslot.draw(self.window, outline=True, char=True)
                                    pygame.display.flip()
                                    clicklisten = True
                                elif select2.isOver(pos):
                                    self.blankalltexts()
                                    if self.opfield.fieldArray == []:
                                        self.opfield.addCardslotInTurn(cardslot)
                                        self.cardremoval(self.myfield, cardslot)
                                        self.opfield.build_field(self.window)
                                        self.myfield.build_field(self.window)
                                        pygame.display.flip()
                                        clicklisten = True
                                    else:
                                        self.aiDecision("forcedremove", cardslot)
                                        self.opfield.addCardslotInTurn(cardslot)
                                        self.cardremoval(self.myfield, cardslot)
                                        self.opfield.build_field(self.window)
                                        self.myfield.build_field(self.window)
                                        self.blankalltexts()
                                        pygame.display.flip()
                                        clicklisten = True
                            else:
                                pass
            elif cardslot.card.abilityid == "daywolf":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    self.updategametext("Do you want Day Wolf to have 8 strength or the melee ability?")
                    select1 = Cardslot(yellow, self.myabilityarea.x + gap, self.myabilityarea.y + gap, self.myabilityarea.width - (gap * 2), (self.myabilityarea.height / 2) - (gap * 2), None, False, "Strength to 8")
                    select2 = Cardslot(yellow, select1.x, select1.y + (gap * 2) + select1.height, self.myabilityarea.width - (gap * 2), (self.myabilityarea.height / 2) - (gap * 2), None, False, "Retain Melee ability")
                    self.updatemyabilitytext(" ")
                    select1.draw(self.window,outline=True)
                    select2.draw(self.window,outline=True)
                    pygame.display.flip()

                    clicklisten = False
                    while not clicklisten:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                if select1.isOver(pos):
                                    cardslot.strength = str(8)
                                    self.cardchangesDict[cardslot.card.serial+"choice"] = "Passive"
                                    clicklisten = True
                                    self.blankalltexts()
                                elif select2.isOver(pos):
                                    self.cardchangesDict[cardslot.card.serial+"choice"] = "Melee"
                                    clicklisten = True
                                    self.blankalltexts()


                if self.cardchangesDict[cardslot.card.serial+"choice"] == "Melee":
                    self.melee("my", cardslot)
                elif self.cardchangesDict[cardslot.card.serial+"choice"] == "Passive":
                    pass
            elif cardslot.card.abilityid == "nightwolf":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    self.updategametext("Do you want Night Wolf to have 8 strength or the melee ability?")
                    select1 = Cardslot(yellow, self.myabilityarea.x + gap, self.myabilityarea.y + gap, self.myabilityarea.width - (gap * 2), (self.myabilityarea.height / 2) - (gap * 2), None, False, "Strength to 8")
                    select2 = Cardslot(yellow, select1.x, select1.y + (gap * 2) + select1.height, self.myabilityarea.width - (gap * 2), (self.myabilityarea.height / 2) - (gap * 2), None, False, "Retain Melee ability")
                    self.updatemyabilitytext("")
                    select1.draw(self.window, outline=True)
                    select2.draw(self.window, outline=True)
                    pygame.display.flip()

                    clicklisten = False
                    while not clicklisten:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                if select1.isOver(pos):
                                    cardslot.strength = str(8)
                                    self.cardchangesDict[cardslot.card.serial+"choice"] = "Passive"
                                    clicklisten = True
                                    self.blankalltexts()
                                elif select2.isOver(pos):
                                    self.cardchangesDict[cardslot.card.serial+"choice"] = "Melee"
                                    clicklisten = True
                                    self.blankalltexts()


                if self.cardchangesDict[cardslot.card.serial+"choice"] == "Melee":
                    self.melee("my", cardslot)
                elif self.cardchangesDict[cardslot.card.serial+"choice"] == "Passive":
                    pass
            elif cardslot.card.abilityid == "beggarking":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    choice = self.aiDecision("mybeggarking", cardslot)

                    if choice == "increase":
                        self.updategametext("Now choose a card to increase")
                        for card in self.myfield.fieldArray:
                            card.draw(self.window, decision=True, char=True)
                        cardslot.draw(self.window, selected=True, char=True)
                        pygame.display.flip()

                        clicklisten = False
                        while clicklisten == False:
                            for clickevent in pygame.event.get():
                                if clicklisten == True:
                                    break
                                pos = pygame.mouse.get_pos()
                                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                    for cardpick in self.myfield.fieldArray:
                                        if clicklisten == True:
                                            break
                                        if cardpick.isOver(pos):
                                            for resetcard in self.myfield.fieldArray:
                                                resetcard.draw(self.window, outline=True, char=True)
                                            cardpick.draw(self.window, decision=True, char=True)
                                            self.updategametext(
                                                cardslot.name + " increases " + cardpick.name)
                                            cardpick.strength = str(int(cardpick.strength) + 5)
                                            clicklisten = True
                    elif choice == "melee":
                        self.updategametext("Now choose the card that will gain melee immediately")
                        for card in self.myfield.fieldArray:
                            card.draw(self.window, decision=True, char=True)
                        cardslot.draw(self.window, selected=True, char=True)
                        pygame.display.flip()

                        clicklisten = False
                        while clicklisten == False:
                            for clickevent in pygame.event.get():
                                if clicklisten == True:
                                    break
                                pos = pygame.mouse.get_pos()
                                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                    for cardpick in self.myfield.fieldArray:
                                        if clicklisten == True:
                                            break
                                        if cardpick.isOver(pos):
                                            for resetcard in self.myfield.fieldArray:
                                                resetcard.draw(self.window, outline=True, char=True)
                                            cardpick.draw(self.window, decision=True, char=True)
                                            self.melee("my", cardpick)
                                            clicklisten = True
                        self.blankalltexts()
            elif cardslot.card.abilityid == "undeadlegion":
                if cardslot.card.serial not in self.cardchangesDict:
                    self.cardchangesDict[cardslot.card.serial] = 0
            elif cardslot.card.abilityid == "madman":
                if cardslot.card.serial == "madman1":
                    self.cardchangesDict["madman1side"] = "my"
                elif cardslot.card.serial == "madman2":
                    self.cardchangesDict["madman2side"] = "my"
            elif cardslot.card.abilityid == "griffon":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    self.updategametext("Do you want Griffon to retain melee or restrict your opponent to only locking night cards and revealing their locks?")
                    select1 = Cardslot(yellow, self.myabilityarea.x + gap, self.myabilityarea.y + gap,
                                       self.myabilityarea.width - (gap * 2),
                                       (self.myabilityarea.height / 2) - (gap * 2), None, False, "Retain Melee ability")
                    select2 = Cardslot(yellow, select1.x, select1.y + (gap * 2) + select1.height,
                                       self.myabilityarea.width - (gap * 2),
                                       (self.myabilityarea.height / 2) - (gap * 2), None, False, "Restrict and reveal opponent locks")
                    self.updatemyabilitytext(" ")
                    select1.draw(self.window, outline=True)
                    select2.draw(self.window, outline=True)
                    pygame.display.flip()

                    clicklisten = False
                    while not clicklisten:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                if select1.isOver(pos):
                                    cardslot.strength = str(8)
                                    self.cardchangesDict[cardslot.card.serial + "choice"] = "Melee"
                                    clicklisten = True
                                    self.blankalltexts()
                                elif select2.isOver(pos):
                                    self.cardchangesDict[cardslot.card.serial + "choice"] = "Restict"
                                    clicklisten = True
                                    self.blankalltexts()

                if self.cardchangesDict[cardslot.card.serial + "choice"] == "Melee":
                    self.melee("my", cardslot)
                elif self.cardchangesDict[cardslot.card.serial + "choice"] == "Restrict":
                    pass
            elif cardslot.card.abilityid == "knight":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:

                    for card in self.opfield.fieldArray:
                        card.draw(self.window, decision=True, char=True)
                    for card in self.myfield.fieldArray:
                        card.draw(self.window, decision=True, char=True)
                    cardslot.draw(self.window, selected=True, char=True)
                    pygame.display.flip()

                    self.updategametext("Click the card you wish to assign, or click the button below to skip")
                    self.updatemyabilitytext(cardslot.card.abilitytext)
                    skipbutton = Cardslot(yellow, self.textarea.x + 5,
                                          self.textarea.y + self.textarea.height - 30 - 5,
                                          self.textarea.width - 10, 30, None, False, name="Click to Skip")
                    skipbutton.draw(self.window, outline = True)
                    pygame.display.flip()
                    clicklisten = False
                    while clicklisten == False:
                        for clickevent in pygame.event.get():
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                for cardpick in self.opfield.fieldArray:
                                    if clicklisten == True:
                                        break
                                    if cardpick.isOver(pos):
                                        cardpick.settokentext("K")
                                        for resetcard in self.opfield.fieldArray:
                                            resetcard.draw(self.window, outline=True, char=True)
                                        self.cardchangesDict[cardslot.card.serial+ "pick"] = [cardpick, "my"]
                                        pygame.display.flip()
                                        clicklisten = True
                                for cardpick in self.myfield.fieldArray:
                                    if clicklisten == True:
                                        break
                                    if cardpick.isOver(pos):
                                        cardpick.settokentext("K")
                                        for resetcard in self.opfield.fieldArray:
                                            resetcard.draw(self.window, outline=True, char=True)
                                        self.cardchangesDict[cardslot.card.serial+ "pick"] = [cardpick, "my"]
                                        pygame.display.flip()
                                        clicklisten = True
                                if skipbutton.isOver(pos):
                                    self.updategametext("You chose to skip assignment")
                                    self.clicktocontinue()
                                    clicklisten = True
            elif cardslot.card.abilityid == "heretic":
                if cardslot.card.serial == self.myselectedCardslot.card.serial:
                    cardpick = self.increasemystrengthbynumber(cardslot,5)
                    self.opfield.build_field(self.window)
                    self.myfield.build_field(self.window)
            elif cardslot.card.abilityid == "spearman":
                self.melee("my", cardslot)
            elif cardslot.card.abilityid == "phoenix":
                if cardslot.card.serial+"reborn" not in self.cardchangesDict:
                    self.melee("my", cardslot)
                elif cardslot.card.serial+"reborn" in self.cardchangesDict:
                    pass
            elif cardslot.card.abilityid == "bandit":
                self.advantagecheck()
                if self.nightPowerAdvantage == "my":
                    self.melee("my", cardslot)

        if whoscard == "op":
            if cardslot == self.opfield.cardondeck:
                self.advantagecheck()

            if cardslot.card.abilityid == "madman":
                if cardslot.card.serial == "madman1":
                    self.cardchangesDict["madman1side"] = "op"
                elif cardslot.card.serial == "madman2":
                    self.cardchangesDict["madman2side"] = "op"
            elif cardslot.card.abilityid == "undeadlegion":
                if cardslot.card.serial not in self.cardchangesDict:
                    self.cardchangesDict[cardslot.card.serial] = 0
            elif cardslot.card.abilityid == "frostgiant":
                self.endofRoundArray.append(["frostgiant", cardslot, whoscard])
            elif cardslot.card.abilityid == "gorgon":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("gorgon", cardslot)
            elif cardslot.card.abilityid == "daywolf":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("daywolf", cardslot)
                if self.cardchangesDict[cardslot.card.serial + "choice"] == "Melee":
                    self.melee("op",cardslot)
            elif cardslot.card.abilityid == "nightwolf":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("nightwolf", cardslot)
                if self.cardchangesDict[cardslot.card.serial + "choice"] == "Melee":
                    self.melee("op",cardslot)
            elif cardslot.card.abilityid == "beggarking":
                if cardslot.card.serial == self.opselectedCardslot.card.serial:
                    self.updategametext("Do you want your opponent to increase the strength of a card by 5 or have a card melee immediately?")
                    select1 = Cardslot(yellow, self.myabilityarea.x + gap, self.myabilityarea.y + gap,
                                       self.myabilityarea.width - (gap * 2),
                                       (self.myabilityarea.height / 2) - (gap * 2), None, False,
                                       "Increase Strength by 5")
                    select2 = Cardslot(yellow, select1.x, select1.y + (gap * 2) + select1.height,
                                       self.myabilityarea.width - (gap * 2),
                                       (self.myabilityarea.height / 2) - (gap * 2), None, False,
                                       "Gain Melee immediately")
                    self.updatemyabilitytext("")
                    select1.draw(self.window, outline=True)
                    select2.draw(self.window, outline=True)
                    pygame.display.flip()

                    clicklisten = False
                    while not clicklisten:
                        for clickevent in pygame.event.get():
                            if clickevent.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                if select1.isOver(pos):
                                    self.aiDecision("beggarkingincrease", cardslot)
                                    self.blankalltexts()
                                    clicklisten = True

                                elif select2.isOver(pos):
                                    self.aiDecision("beggarkingmelee", cardslot)
                                    self.blankalltexts()
                                    clicklisten = True
            elif cardslot.card.abilityid == "golem":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("golem", cardslot)
            elif cardslot.card.abilityid == "barbarian":
                result = self.melee("op", cardslot)
                if result == "win":
                    if cardslot.card.serial+"kills" not in self.cardchangesDict:
                        self.cardchangesDict[cardslot.card.serial+"kills"] = 1
                    else:
                        curbarbariankills = self.cardchangesDict[cardslot.card.serial+"kills"]
                        curbarbariankills += 1
                        self.cardchangesDict[cardslot.card.serial+"kills"] = curbarbariankills
                    self.endofRoundArray.append(["barbarian", cardslot, whoscard])
            elif cardslot.card.abilityid == "seer":
                # AI increases the highest card on it's side of the field. Including itself.
                choice = 0
                for card in self.opfield.fieldArray:
                    if choice == 0:
                        choice = card
                    elif int(card.strength) > int(choice.strength):
                        choice = card
                    else:
                        pass

                self.updategametext(cardslot.name + " increases " + choice.name)
                self.clicktocontinue()
                choice.strength = str(int(choice.strength) + 1)
                if choice.card.serial in self.cardchangesDict:
                    self.cardchangesDict[choice.card.serial] = int(self.cardchangesDict[choice.card.serial]) + 1
                else:
                    self.cardchangesDict[choice.card.serial] = 1
                self.opfield.build_field(self.window)
            elif cardslot.card.abilityid == "heretic":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("heretic", cardslot)
            elif cardslot.card.abilityid == "knight":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("knight", cardslot)
            elif cardslot.card.abilityid == "dragon":
                result = self.aiDecision("dragon", cardslot)
            elif cardslot.card.abilityid == "headsman":
                if cardslot == self.opfield.cardondeck:
                    self.aiDecision("headsman", cardslot)
            elif cardslot.card.abilityid == "kraken":
                pass
            elif cardslot.card.abilityid == "spearman":
                result = self.melee("op",cardslot)
            elif cardslot.card.abilityid == "phoenix":
                if cardslot.card.serial+"reborn" not in self.cardchangesDict:
                    self.melee("op", cardslot)
                elif cardslot.card.serial+"reborn" in self.cardchangesDict:
                    pass
            elif cardslot.card.abilityid == "bandit":
                self.advantagecheck()
                if self.nightPowerAdvantage == "op":
                    self.melee("op", cardslot)
        print(cardslot.name, "Ability executed")
        self.redrawwindow()

    def advantagecheck(self):
        self.opfield.calculatePower()
        self.myfield.calculatePower()
        if self.myfield.daypower > self.opfield.daypower:
            self.dayPowerAdvantage = "my"
        elif self.myfield.daypower == self.opfield.daypower:
            pass
        else:
            self.dayPowerAdvantage = "op"

        if self.myfield.nightpower > self.opfield.nightpower:
            self.nightPowerAdvantage = "my"
        elif self.myfield.nightpower == self.opfield.nightpower:
            pass
        else:
            self.nightPowerAdvantage = "op"

    def skipbutton(self):
        skipbutton = Cardslot(white, self.textarea.x + 5, self.textarea.y + self.textarea.height - 30 - 5,
                              self.textarea.width - 10, 30, None, False, name="Click to Skip")
        skipbutton.draw(self.window, outline=True)
        pygame.display.flip()
        return skipbutton

    def trollcheck(self, defendingside):
        if defendingside == "my":
            for card in self.myfield.fieldArray:
                if card.card.abilityid == "troll":
                    trollcheck = True
                    return trollcheck, card
        elif defendingside == "op":
            for card in self.opfield.fieldArray:
                if card.card.abilityid == "troll":
                    trollcheck = True
                    return trollcheck, card

        return False, None

    def meleeresolution(self, attacker, attackerside, defender, defenderside, attackingmodifiertype=None, attackingmodifier=0, defendingmodifiertype=None, defendingmodifier=0):
        if attackerside == "my":
            attackerfield = self.myfield
        elif attackerside == "op":
            attackerfield = self.opfield
        if defenderside == "my":
            defenderfield = self.myfield
        elif defenderside == "op":
            defenderfield = self.opfield
        attackerstr = int(attacker.strength)
        defenderstr = int(defender.strength)
        attackerdmg = attackerstr
        defenderdmg = defenderstr

        if attackingmodifiertype == None:
            pass
        elif attackingmodifiertype == "multiply":
            attackerdmg = math.ceil(attacker.strength * attackingmodifier)
        elif attackingmodifiertype == "add":
            attackerdmg = attacker.strength + attackingmodifier
        elif attackingmodifiertype == "subtract":
            attackerdmg = attacker.strength - attackingmodifier


        if defendingmodifiertype == None:
            pass
        elif defendingmodifiertype == "multiply":
            defenderdmg = math.ceil(defender.strength * defendingmodifier)
        elif defendingmodifiertype == "add":
            defenderdmg = defender.strength + defendingmodifier
        elif attackingmodifiertype == "subtract":
            defenderdmg = defender.strength - defendingmodifier

        defenderfinalstr = defenderstr - attackerdmg
        attackerfinalstr = attackerstr - defenderdmg

        if defenderfinalstr <= 0:
            defenderresolution = "remove"
        else:
            defenderresolution = "remain"

        if attackerfinalstr <= 0:
            attackerresolution = "remove"
        else:
            attackerresolution = "remain"

        if attackerresolution == "remain" and defenderresolution == "remove":
            self.updategametext(attacker.name + " attacks " + defender.name +" and " + defender.name + " is defeated" )
            self.cardremoval(defenderfield, defender)
            self.clicktocontinue()
            attacker.strength = attackerfinalstr

        elif attackerresolution == "remove" and defenderresolution == "remain":
            self.updategametext(attacker.name + " attacks " + defender.name + " and " + attacker.name + " is destroyed")
            self.cardremoval(attackerfield, attacker)
            self.clicktocontinue()
            defender.strength = defenderfinalstr


        elif attackerresolution == "remove" and defenderresolution == "remove":
            self.updategametext(attacker.name + " attacks " + defender.name + " and both fighters are destroyed")
            self.cardremoval(attackerfield, attacker)
            self.cardremoval(defenderfield, defender)
            self.clicktocontinue()

        elif attackerresolution == "remain" and defenderresolution == "remain":
            self.updategametext(attacker.name + " attacks " + defender.name + " and both fighters survive")
            self.clicktocontinue()
            defender.strength = defenderfinalstr
            attacker.strength = attackerfinalstr


        self.redrawwindow()

    def melee(self, attackingPlayer, attacker):
        # if card is in meleeremoval list the function ends immediately
        if attacker in self.cardchangesDict["meleeremoval"]:
            return

        if attackingPlayer == "my":
            # Troll ability check
            trollcheck, defender = self.trollcheck("op")
            if trollcheck:
                defender.draw(self.window, decision=True, char=True)
                attacker.draw(self.window, selected=True, char=True)
                skip = self.skipbutton()
                skip.draw(self.window, outline=True)
                self.updategametext("You can only melee Troll, if you don't want to melee click below to skip")
                clicklisten = False
            # If no troll detected, run normal melee
            else:
                self.updategametext("You can click any card to melee it, if you don't want to melee click below to skip")
                self.highlightcards(self.opfield.fieldArray+self.myfield.fieldArray)
                attacker.draw(self.window, selected=True, char=True)
                skip = self.skipbutton()
                skip.draw(self.window, outline=True)
                pygame.display.flip()

            # This next section forces the player to pick a defender for the melee, or skip
            clicklisten = False
            cardpicked = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    pick = None
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:
                        # Skips if detects skip, leaves cardpicked false which will end the melee function
                        if skip.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            attacker.draw(self.window, outline=True, char=True)
                            pygame.display.flip()
                            clicklisten = True

                        if trollcheck:
                            if defender.isOver(pos):
                                clicklisten = True

                        for card in self.opfield.fieldArray:
                            if card.isOver(pos):
                                for resetcard in self.opfield.fieldArray:
                                    resetcard.draw(self.window, outline=True, char=True)
                                for resetcard in self.myfield.fieldArray:
                                    resetcard.draw(self.window, outline=True, char=True)
                                attacker.draw(self.window, outline=True, selected=True, char=True)
                                defender = card
                                defender.draw(self.window, outline=True, selected=True, char=True)
                                pygame.display.flip()
                                cardpicked = True
                                clicklisten = True

            # this next section will be the attacker and defender resolving melee if cardpicked is True
            if cardpicked:
                attackingmodifier = 0
                attackingmodifiertype = ''
                defendingmodifier = 0
                defendingmodifiertype = ''

                if attacker.card.abilityid == "spearman":
                    attackingmodifiertype = "multiply"
                    attackingmodifier = .5

                if defender.card.abilityid == "ghostship":
                    defendingmodifiertype = "multiply"
                    defendingmodifier = 2



                self.meleeresolution(attacker, attacker.side, defender, defender.side, attackingmodifiertype=attackingmodifiertype,
                                     attackingmodifier=attackingmodifier, defendingmodifiertype=defendingmodifiertype,
                                     defendingmodifier=defendingmodifier)


        elif attackingPlayer == "op":
            attackingmodifiertype = None
            defendingmodifiertype = None
            attackingmodifier = 0
            defendingmodifier = 0

            trollcheck, card = self.trollcheck("my")
            if trollcheck:
                decision = self.aiDecision("trolldefend", attacker, defendingCard=card)
                if decision == "pass":
                    return
                else:
                    attacker.draw(self.window, selected=True, char=True)
                    card.draw(self.window, selected=True, char=True)
                    defender = card
            else:
                defender = self.aiDecision("meleeselect", attacker)
                if defender == None:
                    return

            if attacker.card.abilityid == "spearman":
                attackingmodifiertype = "multiply"
                attackingmodifier = .5

            if defender.card.abilityid == "ghostship":
                defendingmodifiertype = "multiply"
                defendingmodifier = 2


            self.meleeresolution(attacker, "op", defender, "my", attackingmodifiertype=attackingmodifiertype, attackingmodifier=attackingmodifier, defendingmodifiertype=defendingmodifiertype, defendingmodifier=defendingmodifier)

# Behemouth previous melee functions
    """def mymelee(self, cardslot):

        if cardslot in self.cardchangesDict["meleeremoval"]:
            return

        trollcheck = False
        cardpick = None
        for card in self.opfield.fieldArray:
            if card.card.abilityid == "troll":
                trollcheck = True
                cardpick = card
                break
        # if a troll is on your opponents field
        if trollcheck == True:
            cardpick.draw(self.window, decision=True, char=True)
            cardslot.draw(self.window, selected=True, char=True)
            self.updategametext("You can only melee Troll, if you don't want to melee click below to skip")
            skipbutton = Cardslot(white, self.textarea.x + 5, self.textarea.y + self.textarea.height - 30 - 5,
                                  self.textarea.width - 10, 30, None, False, name="Click to Skip")
            skipbutton.draw(self.window, outline=True)
            pygame.display.flip()
            clicklisten = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:

                        if skipbutton.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardslot.draw(self.window, outline=True, char=True)
                            pygame.display.flip()
                            clicklisten = True
                        else:
                            if cardpick.isOver(pos):
                                cardpick.draw(self.window, decision=True, char=True)
                                self.updategametext(cardslot.name + " Melee's " + cardpick.name)
                                self.clicktocontinue()
                                if cardslot.card.abilityid == "spearman":
                                    result = self.spearmanmelee(cardpick, cardslot)
                                    return result
                                elif int(cardpick.strength) < int(cardslot.strength):
                                    self.updategametext(cardpick.name + " is destroyed")
                                    self.clicktocontinue()
                                    cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
                                    self.cardremoval(self.opfield, cardpick)
                                    self.opfield.build_field(self.window)
                                    self.myfield.build_field(self.window)
                                    cardslot.draw(self.window, selected=True)
                                    pygame.display.flip()
                                    self.endofRoundArray.append(["melee", cardslot, "my"])
                                    return "win"
                                elif int(cardpick.strength) > int(cardslot.strength):
                                    self.updategametext(cardslot.name + " is destroyed")
                                    cardpick.strength = str(int(cardpick.strength) - int(cardslot.strength))
                                    self.cardremoval(self.myfield, cardslot)
                                    cardpick.draw(self.window, outline=True, char=True)
                                    pygame.display.flip()
                                    self.myfield.build_field(self.window)
                                    self.clicktocontinue()
                                    pygame.display.flip()
                                    self.endofRoundArray.append(["melee", cardpick, "op"])
                                    return "lose"
                                else:
                                    self.updategametext("Both fighters are destroyed")
                                    self.clicktocontinue()
                                    self.cardremoval(self.opfield, cardpick)
                                    self.opfield.build_field(self.window)
                                    self.cardremoval(self.myfield, cardslot)
                                    self.myfield.build_field(self.window)

                                    pygame.display.flip()
                                    return "draw"

        else:
            for card in self.opfield.fieldArray:
                card.draw(self.window, decision=True, char=True)
            for card in self.myfield.fieldArray:
                card.draw(self.window, decision=True, char=True)
            cardslot.draw(self.window, selected=True, char=True)

            self.updategametext("Click the card you wish to melee, or click the button below to skip Melee")
            skipbutton = Cardslot(white, self.textarea.x + 5, self.textarea.y + self.textarea.height - 30 - 5,
                                  self.textarea.width - 10, 30, None, False, name="Click to Skip")
            skipbutton.draw(self.window, outline=True)
            pygame.display.flip()
            clicklisten = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:

                        if skipbutton.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardslot.draw(self.window, outline=True, char=True)
                            pygame.display.flip()
                            clicklisten = True
                        else:
                            for cardpick in self.opfield.fieldArray:
                                if clicklisten == True:
                                    break
                                if cardpick.isOver(pos):
                                    for resetcard in self.opfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    for resetcard in self.myfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    cardpick.draw(self.window, decision=True, char=True)
                                    if cardpick.card.abilityid == "ghostship":
                                        result = self.ghostshipmelee(cardpick, cardslot)
                                        return result
                                    elif cardslot.card.abilityid == "spearman":
                                        result = self.spearmanmelee(cardpick, cardslot)
                                        return result

                                    elif int(cardpick.strength) < int(cardslot.strength):
                                        self.updategametext(cardslot.name + " Melee's " + cardpick.name + ". " + cardpick.name + " is destroyed")
                                        self.clicktocontinue()
                                        cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
                                        self.cardremoval(self.opfield, cardpick)
                                        self.redrawwindow()
                                        if cardpick.card.abilityid == "seer":
                                            self.updategametext(cardslot.name + " loses their ability to Melee")
                                            self.cardchangesDict["meleeremoval"].append(cardslot)
                                            self.clicktocontinue()
                                        self.opfield.build_field(self.window)
                                        self.myfield.build_field(self.window)

                                        cardslot.draw(self.window, selected=True)
                                        pygame.display.flip()
                                        self.endofRoundArray.append(["melee", cardslot, "my"])
                                        return "win"
                                    elif int(cardpick.strength) > int(cardslot.strength):
                                        self.updategametext(cardslot.name + " Melee's " + cardpick.name + ". " + cardslot.name + " is destroyed")
                                        cardpick.strength = str(int(cardpick.strength) - int(cardslot.strength))
                                        self.cardremoval(self.myfield,cardslot)
                                        cardpick.draw(self.window, outline=True, char=True)
                                        pygame.display.flip()
                                        self.myfield.build_field(self.window)
                                        #self.clicktocontinue()
                                        pygame.display.flip()
                                        self.endofRoundArray.append(["melee", cardpick, "op"])
                                        return "lose"
                                    else:
                                        self.updategametext("Both fighters are destroyed")
                                        self.clicktocontinue()
                                        self.cardremoval(self.opfield, cardpick)
                                        self.opfield.build_field(self.window)
                                        self.cardremoval(self.myfield, cardslot)
                                        self.myfield.build_field(self.window)

                                        pygame.display.flip()
                                        return "draw"
                            for cardpick in self.myfield.fieldArray:
                                if clicklisten == True:
                                    break
                                if cardpick == cardslot:
                                    pass
                                elif cardpick.isOver(pos):
                                    for resetcard in self.opfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    for resetcard in self.myfield.fieldArray:
                                        resetcard.draw(self.window, outline=True, char=True)
                                    cardpick.draw(self.window, decision=True, char=True)
                                    if cardpick.card.abilityid == "ghostship":
                                        result = self.ghostshipmelee(cardpick, cardslot)
                                        return result
                                    elif int(cardpick.strength) < int(cardslot.strength):
                                        self.updategametext(cardslot.name + " Melee's " + cardpick.name + ". " + cardpick.name + " is destroyed")
                                        self.clicktocontinue()
                                        cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
                                        self.cardremoval(self.myfield, cardpick)
                                        self.opfield.build_field(self.window)
                                        self.myfield.build_field(self.window)
                                        cardslot.draw(self.window, selected=True)
                                        pygame.display.flip()
                                        self.endofRoundArray.append(["melee", cardslot, "my"])
                                        return "win"
                                    elif int(cardpick.strength) > int(cardslot.strength):
                                        self.updategametext(cardslot.name + " Melee's " + cardpick.name + ". " + cardslot.name + " is destroyed")

                                        cardpick.strength = str(int(cardpick.strength) - int(cardslot.strength))
                                        self.cardremoval(self.myfield,cardslot)
                                        self.myfield.build_field(self.window)
                                        self.clicktocontinue()
                                        pygame.display.flip()
                                        self.endofRoundArray.append(["melee", cardpick, "op"])
                                        return "lose"
                                    else:
                                        self.updategametext("Both fighters are destroyed")
                                        self.clicktocontinue()
                                        self.cardremoval(self.myfield, cardpick)
                                        self.opfield.build_field(self.window)
                                        self.cardremoval(self.myfield, cardslot)
                                        self.myfield.build_field(self.window)


                                        pygame.display.flip()
                                        return "draw"

    def opmelee(self, cardslot):
        # ai will only attack cards it can defeat, but it will
        # attack ghost ship and dragon (if it can get the kill) even if it means the attacker is destroyed
        if cardslot in self.cardchangesDict["meleeremoval"]:
            return

        trollcheck = False
        cardpick = None
        for card in self.myfield.fieldArray:
            if card.card.abilityid == "troll":
                trollcheck = True
                cardpick = card
                break

        if trollcheck == True:
            if cardslot.card.abilityid == "spearman":
                reducedstrength = math.ceil(int(cardslot.strength) / 2)
                if int(cardpick.strength) <= reducedstrength and int(cardpick.strength) < int(cardslot.strength):
                    self.updategametext(cardslot.name + " melee's " + cardpick.name)
                    self.clicktocontinue()

                    cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))

                    self.cardremoval(self.myfield, card)

                    self.myfield.build_field(self.window)
                    self.opfield.build_field(self.window)
                    pygame.display.flip()
                    if cardslot.card.abilityid == "barbarian":
                        pass
                    else:
                        self.endofRoundArray.append(["melee", cardslot, "op"])
                    return "win"

            elif int(cardslot.strength) > int(cardpick.strength):
                self.updategametext(cardslot.name + " melee's " + cardpick.name)
                self.clicktocontinue()
                cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
                self.cardremoval(self.myfield, card)

                self.myfield.build_field(self.window)
                self.opfield.build_field(self.window)
                pygame.display.flip()
                if cardslot.card.abilityid == "barbarian":
                    pass
                else:
                    self.endofRoundArray.append(["melee", cardslot, "op"])
                return "win"



        else:
            for card in self.myfield.fieldArray:
                if card.card.abilityid == "ghostship":
                    if int(card.strength)/2 <= int(cardslot.strength):
                        self.updategametext(cardslot.name + " melee's " + card.name)
                        self.clicktocontinue()

                        cardslot.strength = str(int(cardslot.strength) - int(card.strength))
                        if int(cardslot.strength) <= 0:
                            self.cardremoval(self.opfield, cardslot)
                            self.cardremoval(self.myfield, card)
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            pygame.display.flip()
                            return "lose"
                        else:
                            self.cardremoval(self.myfield, card)
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            pygame.display.flip()
                            if cardslot.card.abilityid == "barbarian":
                                pass
                            else:
                                self.endofRoundArray.append(["melee", cardslot, "op"])
                            return "win"
                elif cardslot.card.abilityid == "spearman":
                    reducedstrength = math.ceil(int(cardslot.strength) / 2)
                    if int(card.strength) <= reducedstrength and int(card.strength) < int(cardslot.strength):
                        self.updategametext(cardslot.name + " melee's " + card.name)
                        self.clicktocontinue()

                        cardslot.strength = str(int(cardslot.strength) - int(card.strength))

                        self.cardremoval(self.myfield, card)

                        self.myfield.build_field(self.window)
                        self.opfield.build_field(self.window)
                        pygame.display.flip()
                        if cardslot.card.abilityid == "barbarian":
                            pass
                        else:
                            self.endofRoundArray.append(["melee", cardslot, "op"])
                        return "win"

                elif card.name == "dragon":
                    if int(card.strength) <= int(cardslot.strength):
                        self.updategametext(cardslot.name + " melee's " + card.name + ".")
                        self.clicktocontinue()

                        cardslot.strength = str(int(cardslot.strength) - int(card.strength))
                        if int(cardslot.strength) <= 0:
                            self.cardremoval(self.opfield, cardslot)
                            self.cardremoval(self.myfield, card)
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            pygame.display.flip()
                            return "lose"
                        else:
                            self.cardremoval(self.myfield, card)
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            pygame.display.flip()
                            if cardslot.card.abilityid == "barbarian":
                                pass
                            else:
                                self.endofRoundArray.append(["melee", cardslot, "op"])
                            return "win"
                elif int(card.strength) < int(cardslot.strength):
                    self.updategametext(cardslot.name + " melee's " + card.name)
                    self.clicktocontinue()
                    if card.card.abilityid == "seer":
                        self.updategametext(cardslot.name + " loses their ability to Melee")
                        self.cardchangesDict["meleeremoval"].append(cardslot)
                        self.clicktocontinue()
                    cardslot.strength = str(int(cardslot.strength) - int(card.strength))

                    self.cardremoval(self.myfield, card)

                    self.redrawwindow()
                    if cardslot.card.abilityid == "barbarian":
                        pass
                    else:
                        self.endofRoundArray.append(["melee", cardslot, "op"])
                    return "win"
"""

    def cardremoval(self, field, cardslot):
        field.removeCardslotInTurn(cardslot)

        # below are where abilities that resolve when a card is removed occur
        if cardslot.card.abilityid == "madman":
            fieldside = self.cardchangesDict[cardslot.card.serial+"side"]
            self.madmanswitch(cardslot, fieldside)
        elif cardslot.card.abilityid == "heretic":
            if field == self.myfield:
                self.aiDecision("myheretic", cardslot)
            elif field == self.opfield:
                if self.opfield.fieldArray == []:
                    self.updategametext("There are no cards for you to reduce")
                    self.clicktocontinue()
                    self.blankalltexts()
                else:
                    for card in self.opfield.fieldArray:
                        card.draw(self.window, decision=True, char=True)
                    self.updategametext("Choose card to reduce by 5")
                    clicklisten = False
                    while clicklisten == False:
                        for clickevent in pygame.event.get():
                            if clickevent.type == pygame.QUIT:
                                quit()
                            if clicklisten == True:
                                break
                            pos = pygame.mouse.get_pos()
                            if clickevent.type == pygame.MOUSEBUTTONDOWN:
                                for cardpick in self.opfield.fieldArray:
                                    if clicklisten == True:
                                        break
                                    if cardpick.isOver(pos):
                                        cardpick.strength = str(int(cardpick.strength) - 5)
                                        if int(cardpick.strength) <= 0:
                                            self.cardremoval(self.opfield, cardpick)
                                        pygame.display.flip()
                                        clicklisten = True
                                for cardpick in self.myfield.fieldArray:
                                    if clicklisten == True:
                                        break
                                    if cardpick.isOver(pos):
                                        cardpick.strength = str(int(cardpick.strength) - 5)
                                        if int(cardpick.strength) <= 0:
                                            self.cardremoval(self.myfield, cardpick)
                                        pygame.display.flip()
                                        clicklisten = True
        elif cardslot.card.abilityid == "phoenix":
            if cardslot.card.serial+"reborn" not in self.cardchangesDict:
                self.updategametext("The Phoenix is reborn with 8 strength, but lost the ability to Melee")
                self.clicktocontinue()
                cardslot.strength = str(8)
                cardslot.card.activeability = False
                field.addCardslotInTurn(cardslot)
                self.cardchangesDict[cardslot.card.serial+"reborn"] = True
                cardslot.draw(self.window, outline=True, char=True)
                pygame.display.flip()
        if "undeadlegion1" in self.cardchangesDict:
            change = 2
            self.cardchangesDict["undeadlegion1"] = self.cardchangesDict["undeadlegion1"] + change
            for card in self.myfield.fieldArray:
                if card.card.serial == "undeadlegion1":
                    card.strength = str(int(card.strength) + change)
                    pygame.display.flip()
                    break
            for card in self.opfield.fieldArray:
                if card.card.serial == "undeadlegion1":
                    card.strength = str(int(card.strength) + change)
                    pygame.display.flip()
                    break
        if "knight1pick" in self.cardchangesDict:
            if self.cardchangesDict["knight1pick"][0] == cardslot:
                if self.cardchangesDict["knight1pick"][1] == "my":
                    for card in self.myfield.fieldArray:
                        if card.card.serial == "knight1":
                            card.strength = str(int(card.strength) + 5)
                elif self.cardchangesDict["knight1pick"][1] =="op":
                    for card in self.opfield.fieldArray:
                        if card.card.serial == "knight1":
                            card.strength = str(int(card.strength) + 5)

        return field

    def madmanswitch(self, cardslot, fieldside):
        if fieldside == "my":
            cardslot.strength = str(cardslot.card.strength)
            cardslot.tokentext = ''
            self.opfield.addCardslotInTurn(cardslot)
            self.opfield.build_field(self.window)
            self.cardchangesDict[cardslot.card.serial+"side"] = "op"
        elif fieldside == "op":
            cardslot.strength = str(cardslot.card.strength)
            cardslot.tokentext = ''
            self.myfield.addCardslotInTurn(cardslot)
            self.myfield.build_field(self.window)
            self.cardchangesDict[cardslot.card.serial+"side"] = "my"
        pass

    def ghostshipmelee(self, cardpick, cardslot):
        inccardslotstr = int(cardslot.strength) * 2
        if int(cardpick.strength) < inccardslotstr and int(cardpick.strength) < int(cardslot.strength):
            self.updategametext(cardpick.name + " is destroyed")
            cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
            self.cardremoval(self.opfield, cardpick)
            if cardpick.card.abilityid == "seer":
                self.updategametext(cardslot.name + " loses their ability to Melee")
                self.cardchangesDict["meleeremoval"].append(cardslot)
                self.clicktocontinue()
            self.opfield.build_field(self.window)
            pygame.display.flip()
            self.endofRoundArray.append(["melee", cardslot, "my"])
            return "win"

        elif int(cardpick.strength) > inccardslotstr:
            self.updategametext(cardslot.name + " is destroyed")
            cardpick.strength = str(int(cardpick.strength) - inccardslotstr)
            self.cardremoval(self.myfield, cardslot)
            self.myfield.build_field(self.window)
            pygame.display.flip()
            self.endofRoundArray.append(["melee", cardpick, "op"])
            return "lose"

        else:
            self.updategametext("Both fighters are destroyed")
            self.cardremoval(self.opfield, cardpick)
            self.opfield.build_field(self.window)
            self.cardremoval(self.myfield, cardslot)
            self.myfield.build_field(self.window)
            pygame.display.flip()
            return "draw"

    def spearmanmelee(self, cardpick, cardslot):
        inccardslotstr = math.ceil(int(cardslot.strength) / 2)
        if int(cardpick.strength) <= inccardslotstr:
            self.updategametext(cardslot.name + " melee's " + cardpick.name + ". " + cardpick.name + " is destroyed")
            cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
            self.cardremoval(self.opfield, cardpick)
            if cardpick.card.abilityid == "seer":
                self.updategametext(cardslot.name + " loses their ability to Melee")
                self.cardchangesDict["meleeremoval"].append(cardslot)
                self.clicktocontinue()
            self.opfield.build_field(self.window)
            pygame.display.flip()
            self.endofRoundArray.append(["melee", cardslot, "my"])
            return "win"

        elif int(cardpick.strength) >= int(cardslot.strength):
            self.updategametext(cardslot.name + " is destroyed")
            self.clicktocontinue()
            cardpick.strength = str(int(cardpick.strength) - inccardslotstr)
            self.cardremoval(self.myfield, cardslot)
            self.myfield.build_field(self.window)
            pygame.display.flip()
            self.endofRoundArray.append(["melee", cardpick, "op"])
            return "lose"

        elif int(cardpick.strength) > inccardslotstr and int(cardpick.strength) < int(cardslot.strength):
            self.updategametext("Both fighters live to fight another day")
            self.clicktocontinue()
            cardslot.strength = str(int(cardslot.strength) - int(cardpick.strength))
            cardpick.strength = str(int(cardpick.strength) - inccardslotstr)
            self.myfield.build_field(self.window)
            self.opfield.build_field(self.window)
            pygame.display.flip()
            self.endofRoundArray.append(["melee", cardpick, 'op'])
            self.endofRoundArray.append(["melee", cardslot, 'my'])

        else:
            self.updategametext("Both fighters are destroyed")
            self.clicktocontinue()
            self.cardremoval(self.opfield, cardpick)
            self.opfield.build_field(self.window)
            self.cardremoval(self.myfield, cardslot)
            self.myfield.build_field(self.window)
            pygame.display.flip()
            return "draw"

    def reducestrengthbypercent(self, cardslot, percent):
        reducepercent = percent / 100
        for card in self.opfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        cardslot.draw(self.window, selected=True, char=True)
        pygame.display.flip()

        self.updategametext("Click the card you wish to reduce, or click on " + cardslot.name + " to skip")
        self.updatemyabilitytext(cardslot.card.abilitytext)
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clicklisten == True:
                    break
                pos = pygame.mouse.get_pos()
                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                    for cardpick in self.opfield.fieldArray:
                        print(cardpick)
                        print(clicklisten)
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " reduces " + cardpick.name)
                            self.cardchangesDict[cardpick.card.serial] = int(cardpick.strength) - round(int(cardpick.strength) * reducepercent)
                            cardpick.strength = str(round(int(cardpick.strength) * reducepercent))

                            if int(cardpick.strength) <= 0:
                                self.cardremoval(self.opfield, cardpick)
                            clicklisten = True

                    if cardslot.isOver(pos):
                        for resetcard in self.opfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)
                        self.updategametext(cardslot.name + " does not reduce")
                        clicklisten = True
        pass

    def reduceopstrengthbynumber(self, cardslot, number, permanence):
        for card in self.opfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        cardslot.draw(self.window, selected=True, char=True)
        pygame.display.flip()
        self.updategametext("Choose card to deal damage to, or click " + cardslot.name + " to skip")
        self.updatemyabilitytext(cardslot.card.abilitytext)
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clicklisten == True:
                    break
                pos = pygame.mouse.get_pos()
                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                    for cardpick in self.opfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " reduces " + cardpick.name)
                            if cardpick.card.abilityid == "ghostship":
                                number = number * 2
                            elif number >= int(cardpick.strength):
                                self.cardremoval(self.opfield, cardpick)
                                self.opfield.build_field(self.window)
                                pygame.display.flip()
                                clicklisten = True
                                return "damage"

                            if permanence:
                                cardpick.strength = str(int(cardpick.strength) - number)
                            else:
                                cardpick.strength = str(int(cardpick.strength) - number)
                                if int(cardpick.strength) <= 0:
                                    self.cardremoval(self.opfield, cardpick)
                                    self.myfield.build_field(self.window)
                                    self.opfield.build_field(self.window)
                                else:
                                    self.myfield.build_field(self.window)
                                    self.opfield.build_field(self.window)
                                    self.endofRoundArray.append(["restore", cardpick, "op", number])

                            return "damage"
                        clicklisten = True

                    if cardslot.isOver(pos):
                        for resetcard in self.opfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)
                        self.updategametext(cardslot.name + " does not reduce")
                        clicklisten = True
                        return "skip"
        pass

    def reduceanystrengthbynumber(self, cardslot, number, permanence):
        for card in self.opfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        for card in self.myfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        cardslot.draw(self.window, selected=True, char=True)
        skipbutton = Cardslot(yellow, self.textarea.x + 5, self.textarea.y + self.textarea.height - 30 - 5, self.textarea.width - 10, 30, None, False, name="Click to Skip")

        self.updategametext("Choose card to deal damage to, or click the button below to skip")
        self.updatemyabilitytext(cardslot.card.abilitytext)
        skipbutton.draw(self.window, outline=True)
        pygame.display.flip()
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clicklisten == True:
                    break
                pos = pygame.mouse.get_pos()
                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                    for cardpick in self.opfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " reduces " + cardpick.name)
                            if cardpick.card.abilityid == "ghostship":
                                number = number * 2
                            if number >= int(cardpick.strength):
                                self.cardremoval(self.opfield, cardpick)
                                self.opfield.build_field(self.window)
                                pygame.display.flip()
                                clicklisten = True
                                return "damage"

                            if permanence:
                                cardpick.strength = str(int(cardpick.strength) - number)
                            else:
                                cardpick.strength = str(int(cardpick.strength) - number)
                                self.myfield.build_field(self.window)
                                self.opfield.build_field(self.window)
                                self.endofRoundArray.append(["restore", cardpick, "op", number])

                            return "damage"
                            clicklisten = True

                    for cardpick in self.myfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " reduces " + cardpick.name)
                            if cardpick.card.abilityid == "ghostship":
                                number = number * 2
                            elif number >= int(cardpick.strength):
                                self.cardremoval(self.myfield, cardpick)
                                self.myfield.build_field(self.window)
                                pygame.display.flip()
                                clicklisten = True
                                return "damage"

                            if permanence:
                                cardpick.strength = str(int(cardpick.strength) - number)
                            else:
                                cardpick.strength = str(int(cardpick.strength) - number)
                                self.myfield.build_field(self.window)
                                self.opfield.build_field(self.window)
                                self.endofRoundArray.append(["restore", cardpick, "op", number])

                            return "damage"
                            clicklisten = True

                    if skipbutton.isOver(pos):
                        for resetcard in self.opfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)
                        for resetcard in self.myfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)

                        self.updategametext(cardslot.name + " does not reduce")
                        clicklisten = True
                        return "skip"

    def increasemystrengthbynumber(self, cardslot, number):
        for card in self.myfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        pygame.display.flip()
        self.updategametext("Choose card to increase the strength of")
        self.updatemyabilitytext(cardslot.card.abilitytext)
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clicklisten == True:
                    break
                pos = pygame.mouse.get_pos()
                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                    for cardpick in self.myfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " increases " + cardpick.name)
                            self.clicktocontinue()
                            cardpick.strength = str(int(cardpick.strength) + number)
                            if cardpick.card.serial in self.cardchangesDict:
                                self.cardchangesDict[cardpick.card.serial] = int(self.cardchangesDict[cardpick.card.serial])+number
                            else:
                                self.cardchangesDict[cardpick.card.serial] = number
                            clicklisten = True
                            self.myfield.build_field(self.window)
                            return cardpick

                    if cardslot.isOver(pos):
                        for resetcard in self.opfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)
                        self.updategametext(cardslot.name + " does not reduce")
                        clicklisten = True

    def increaseanystrengthbynumber(self, cardslot, number):
        for card in self.myfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        for card in self.opfield.fieldArray:
            card.draw(self.window, decision=True, char=True)
        pygame.display.flip()
        self.updategametext("Choose card to increase the strength of")
        self.updatemyabilitytext(cardslot.card.abilitytext)
        clicklisten = False
        while clicklisten == False:
            for clickevent in pygame.event.get():
                if clicklisten == True:
                    break
                pos = pygame.mouse.get_pos()
                if clickevent.type == pygame.MOUSEBUTTONDOWN:
                    for cardpick in self.opfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " increases " + cardpick.name)
                            self.clicktocontinue()
                            cardpick.strength = str(int(cardpick.strength) + number)
                            if cardpick.card.serial in self.cardchangesDict:
                                self.cardchangesDict[cardpick.card.serial] = int(self.cardchangesDict[cardpick.card.serial])+number
                            else:
                                self.cardchangesDict[cardpick.card.serial] = number
                            clicklisten = True
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            return cardpick

                    for cardpick in self.myfield.fieldArray:
                        if clicklisten == True:
                            break
                        if cardpick.isOver(pos):
                            for resetcard in self.myfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            for resetcard in self.opfield.fieldArray:
                                resetcard.draw(self.window, outline=True, char=True)
                            cardpick.draw(self.window, decision=True, char=True)
                            self.updategametext(cardslot.name + " increases " + cardpick.name)
                            self.clicktocontinue()
                            cardpick.strength = str(int(cardpick.strength) + number)
                            if cardpick.card.serial in self.cardchangesDict:
                                self.cardchangesDict[cardpick.card.serial] = int(self.cardchangesDict[cardpick.card.serial])+number
                            else:
                                self.cardchangesDict[cardpick.card.serial] = number
                            clicklisten = True
                            self.myfield.build_field(self.window)
                            self.opfield.build_field(self.window)
                            return cardpick

                    if cardslot.isOver(pos):
                        for resetcard in self.opfield.fieldArray:
                            resetcard.draw(self.window, outline=True, char=True)
                        self.updategametext(cardslot.name + " does not reduce")
                        clicklisten = True

    def forcedremovecard(self, cardslot, sidetoremove):
        if sidetoremove == "my":
            for card in self.myfield.fieldArray:
                card.draw(self.window, decision=True, char=True)
            cardslot.draw(self.window, selected=True, char=True)
            pygame.display.flip()

            self.updatemyabilitytext(cardslot.card.abilitytext)
            self.updategametext("Click the card you wish to remove")
            clicklisten = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:
                        for cardpick in self.myfield.fieldArray:
                            if clicklisten == True:
                                break
                            elif cardpick.isOver(pos):
                                self.cardremoval(self.myfield, cardpick)
                                for array in self.myfield.priorityArrays:
                                    if cardpick in array:
                                        array.remove(cardpick)
                                self.myfield.build_field(self.window)
                                pygame.display.flip()
                                clicklisten = True

        if sidetoremove == "op":
            for card in self.opfield.fieldArray:
                card.draw(self.window, decision=True, char=True)
            cardslot.draw(self.window, selected=True, char=True)
            pygame.display.flip()

            self.updatemyabilitytext(cardslot.card.abilitytext)
            self.updategametext("Click the card you wish to remove")
            clicklisten = False
            while clicklisten == False:
                for clickevent in pygame.event.get():
                    if clicklisten == True:
                        break
                    pos = pygame.mouse.get_pos()
                    if clickevent.type == pygame.MOUSEBUTTONDOWN:
                        for cardpick in self.opfield.fieldArray:
                            if clicklisten == True:
                                break
                            elif cardpick.isOver(pos):
                                self.cardremoval(self.opfield, cardpick)
                                for array in self.opfield.priorityArrays:
                                    if cardpick in array:
                                        array.remove(cardpick)
                                self.opfield.build_field(self.window)
                                pygame.display.flip()
                                clicklisten = True
        pass

    def draw_power(self):
        self.myfield.calculatePower()
        self.opfield.calculatePower()
        self.mypower = (self.myfield.nightpower + self.myfield.daypower)
        self.oppower = (self.opfield.nightpower + self.opfield.daypower)
        self.powerarea.updatevalues(self.opfield.daypower, self.opfield.nightpower, self.myfield.daypower, self.myfield.nightpower)
        self.powerarea.draw(self.window, self.dayPowerAdvantage, self.nightPowerAdvantage)

    def endofround(self):
        if self.endofRoundArray is not []:
            for action in self.endofRoundArray:
                actName = action.pop(0)
                card: Cardslot = action.pop(0)
                whoscard = action.pop(0)

                try:
                    number = action.pop(0)
                except:
                    pass
                if card not in self.opfield.fieldArray and card not in self.myfield.fieldArray:
                    pass
                else:
                    if actName == "melee":
                        if card.card.serial not in self.cardchangesDict:
                            self.cardchangesDict[card.card.serial] = 0
                        card.strength = str(int(card.card.strength) + self.cardchangesDict[card.card.serial])
                        card.draw(self.window, outline=True, char=True)

                    elif actName == "barbarian":
                        if whoscard == "my":
                            self.updatemyabilitytext(card.card.abilitytext)
                            self.clicktocontinue()
                        elif whoscard == "op":
                            pass
                        if card.card.serial not in self.cardchangesDict:
                            self.cardchangesDict[card.card.serial] = 0
                        card.strength = str(int(card.card.strength) + self.cardchangesDict[card.card.serial + "kills"] + int(self.cardchangesDict[card.card.serial]))
                        self.blankalltexts()

                    elif actName == "frostgiant":
                        if whoscard == "my":
                            self.updatemyabilitytext(card.card.abilitytext)
                            self.clicktocontinue()
                            pygame.display.flip()
                            if card.card.serial in self.cardchangesDict:
                                hold = self.cardchangesDict[card.card.serial]
                                hold = hold - 1
                                self.cardchangesDict[card.card.serial] = hold
                            else:
                                self.cardchangesDict[card.card.serial] = -1

                        elif whoscard == "op":
                            pass
                        card.strength = str(int(card.strength) - 1)
                        card.draw(self.window, outline=True, char=True)
                        pygame.display.flip()
                        self.updatemyabilitytext("")
                        pygame.display.flip()

                    elif actName == "restore":
                        card.strength = str(int(card.strength) + number)
                        pygame.display.flip()


        self.endofRoundArray = []

    def lockphase(self):
        if self.myhand.handArray:
            self.myhand.build_hand(self.window)
            oplockedcard = self.aiCardSelect(self.ophand.handArray)

            for card in self.myfield.fieldArray:
                if card.card.abilityid=="succubus":
                    self.updategametext("Because you have Succubus you get to select your opponent's lock")
                    for card in self.ophand.handArray:
                        card.draw(self.window, decision=True, char=True)
                    pygame.display.flip()
                    clicklisten = False
                    while clicklisten==False:
                        for event in pygame.event.get():
                            pos = pygame.mouse.get_pos()
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                for card in self.ophand.handArray:
                                    if card.isOver(pos):
                                        oplockedcard = card
                                        self.redrawwindow()
                                        clicklisten = True
                                        break


            for card in self.opfield.fieldArray:
                if card.card.abilityid == "succubus":
                    self.updategametext("Your opponent has Succubus so they get to select your lock")
                    self.clicktocontinue()
                    pick = 0

                    # AI strategy: Selects lowest strength card
                    for card in self.myhandCardslots:
                        if pick == 0:
                            pick = card
                        elif int(pick.strength) >= int(card.strength):
                            pick = card
                        else:
                            pass
                    return pick, oplockedcard

            self.updategametext("Now select one card to keep before you pass your hand")

            self.myselectedCardslot = self.myhand.pick_hand_card(self.window, self.myabilityarea, self)
            return self.myselectedCardslot, oplockedcard


class Deck:
    def __init__(self, totalcardlist, deckspecs):
        self.deckspecs = deckspecs
        self.totalcardlist = totalcardlist
        self.decklist = []
        self.deckdict = dict()
        self.create_Deck()


    def create_Deck(self):

        # First chunk importing total card list into a dictionary with the name as the key
        cardlist = dict()
        totalcardlistfile = open(self.totalcardlist, 'r')
        deckspecificsfile = open(self.deckspecs, 'r')
        cardstack = []
        for line in totalcardlistfile:  # Convert file of all possible cards to dictionary to pull cards from by name
            line = line.rstrip()
            templist = line.split(",")
            name = templist[0]
            countemup = 1
            curstack = [name]
            while countemup < 6:
                rcard = Card(templist[0], templist[1], templist[2], templist[3], templist[4], templist[5], templist[6], templist[7],
                             False, templist[3] + str(countemup))
                curstack.append(rcard)
                countemup += 1
            cardstack.append(curstack)
        tempDeckList = []
        for line2 in deckspecificsfile:  # Add amount of cards in deckspecs to deck
            line2 = line2.rstrip()
            templist2 = line2.split(",")
            name2 = templist2[0]
            amount = int(templist2[1])
            cardlist[name2] = amount

        for item in cardstack:
            cardnum = 0
            curcardname = item.pop(0)
            curamount = cardlist[curcardname]
            while cardnum < curamount:
                curitem = item.pop(0)
                tempDeckList.append(curitem)
                cardnum += 1
                self.deckdict[curitem.serial] = curitem

        self.decklist = tempDeckList

    def shuffle(self, numberoftimestoshuffle):
        counter = 0
        while counter <= numberoftimestoshuffle:
            random.shuffle(self.decklist)
            counter += 1

    def deal_hands(self, handsize, hand1, hand2, shuffletimes):
        self.shuffle(shuffletimes)
        handcounter = 0
        while handcounter < (handsize * 2):
            hand1.addCard(self.decklist[handcounter])
            handcounter += 1
            hand2.addCard(self.decklist[handcounter])
            handcounter += 1
        return hand1, hand2


class Hand:
    def __init__(self, handx, handy, side):
        self.handx = handx
        self.handy = handy
        self.handSize = 0
        self.handArray = []
        self.handDict = dict()
        self.side = side
        self.selectedArray = [False, False, False, False, False, False, False, False]


    def addCard(self, card):
        cardslottoadd = Cardslot(cardcolor, self.handx, self.handy, cardwidth, cardheight, card, False, card.name, card.strength, card.priority, character="Card_images/"+card.abilityid+".png")
        if cardslottoadd.priority == "Day":
            self.handArray.insert(0, cardslottoadd)
        elif cardslottoadd.priority == "Night":
            self.handArray.append(cardslottoadd)
        self.handDict[cardslottoadd.card.serial] = cardslottoadd
        self.handSize += 1

    def removeCard(self, card):
        for slot in self.handArray:
            if slot.card.serial == card.card.serial:
                self.handArray.remove(slot)
                self.handDict.pop(slot.card.serial)
        self.handSize -= 1

    def sort_hand(self):
        reorderedhand = []
        for card in self.handArray:
            if card.priority == "Day":
                reorderedhand.insert(0, card)
            elif card.priority == "Night":
                reorderedhand.append(card)
        self.handArray = reorderedhand

    def build_hand(self, window):
        #display hands
        counter = 0

        if self.side == "op":
            for card in self.handArray:
                card.x = self.handx + ((gap * counter) + (cardwidth * counter))
                card.draw(window, outline=True, char=True, facedown=True)
                counter += 1
        else:
            spacing = gap - (1.5*(len(self.handArray)))
            for card in self.handArray:
                card.x = self.handx + ((spacing * counter) + (cardwidth * counter))
                card.draw(window, outline=True, char=True)
                counter += 1

    def pick_hand_card(self, window, abilitytext, board):
        myselectedCardslot = Cardslot(black, 1, 1, 1, 1, None, False)
        checkmycardselected = False
        passHandselected = False
        while passHandselected == False:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    counter = 0

                    for card in self.handArray:
                        if myselectedCardslot.isOver(pos) and checkmycardselected:
                            passHandselected = True
                            break

                        elif card.isOver(pos):
                            for resetcard in self.handArray:
                                resetcard.draw(window, char=True)
                            checkmycardselected = True
                            myselectedCardslot = card
                            abilitytext.text = myselectedCardslot.card.abilitytext
                            abilitytext.draw(window, blank=True)
                            board.redrawwindow(myselectedcard=card)
                            break


        return myselectedCardslot

    def copy(self):
        newhand = Hand(self.handx, self.handy, self.side)
        newhand.handArray = self.handArray.copy()
        newhand.handDict = self.handDict.copy()
        newhand.handSize = self.handSize
        return newhand


class Field:
    def __init__(self, fieldSize, fieldx, fieldy, fieldimg, side):
        self.fieldSize = fieldSize
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.fieldArray = []
        self.cardondeck = Cardslot(yellow, 0, 0, 0, 0, None, True, )
        self.priorityArrays = [[], []]
        self.fieldArea = Cardslot((50, 50, 50), self.fieldx, self.fieldy, (cardwidth + gap) * 8, cardheight, None, isEmpty=True)
        self.fieldimage = fieldimg
        self.daypower = 0
        self.nightpower = 0
        self.side  = side

    def build_field(self, window):
        #Adds an image to the field
        #mf = pygame.image.load(self.fieldimage)
        #window.blit(mf, (self.fieldx, self.fieldy))
        counter = 0
        self.fieldCardslots = []
        for cardslot in self.fieldArray:
            cardslot.x = self.fieldx + ((gap * counter) + (cardwidth * counter))
            cardslot.y = self.fieldy
            cardslot.draw(window, outline=True, char=True)
            counter += 1
        return window

    def calculatePower(self):
        self.daypower = 0
        self.nightpower = 0
        for card in self.fieldArray:
            if card.card.abilityid == "gargoyle":
                self.nightpower = self.nightpower + int(card.strength)
            elif card.card.priority == "Day":
                self.daypower = self.daypower+int(card.strength)
            else:
                self.nightpower = self.nightpower+int(card.strength)


    def prioritysort(self, cardslot):
        if cardslot.priority == "Day":
            self.priorityArrays[0].append(cardslot)
        elif cardslot.priority == "Night":
            self.priorityArrays[1].append(cardslot)


    def addCardslot(self, cardslot): #sets a card up to be played, but keeps it off the field until it's played
        cardslot.side = self.side
        self.cardondeck = cardslot
        self.prioritysort(cardslot)

    def addCardslotInTurn(self, cardslot):
        cardslot.side = self.side
        self.fieldArray.append(cardslot)
        if cardslot.card.priority == "Day":
            self.priorityArrays[0].append(cardslot)

        elif cardslot.card.priority == "Night":
            self.priorityArrays[1].append(cardslot)

    def removeCardslot(self, cardslot):
        self.fieldArray.remove(cardslot)
        for array in self.priorityArrays:
            try:
                array.remove(cardslot)
            except:
                pass

    def removeCardslotInTurn(self, cardslot):
        self.fieldArray.remove(cardslot)
        if cardslot.card.priority == "Day":
            self.priorityArrays[0].remove(cardslot)

        elif cardslot.card.priority == "Night":
            self.priorityArrays[1].remove(cardslot)




# League Classes below:
class Player:
    def __init__(self, playername):
        self.name = playername
        self.baseSynergyVision = 0
        self.baseThinkingAhead = 0
        self.baseMetaKnowledge = 0
        self.age = 0
        self.jobHours = (0, 0)
        self.gamesplayed = 0
        self.wins = 0
        self.score = 0
        self.rank = 0

    def applymatchtorank(self, win, changenumber):

        if win:
            self.wins += 1
            self.score = self.score + round(changenumber / 5)

        if not win:
            if self.score + round(changenumber / 2) <= 0:
                self.score = 0
            else:
                self.score = self.score + round(changenumber / 10)


        # To determine rank, I take the amount the person won by and divide it by 5 and round it. That number is their rank change.
        # Losses are reduced by half as much as winners are increased by. Hopefully this makes points more evenly spread.
        # In future I want to have the amount you rank fluctuates dependant on how high a rank the person you beat is.
        self.gamesplayed += 1


class League:
    def __init__(self):
        self.playerdict = {}
        self.rankingArray = []
        self.playerlist = []
        self.rankedDict = {}


    def createplayers(self, numberofplayers, gamestoprep):
        playernames = ["Amos", "Catalina", "Earl", "Clifford the Stump", "Lil Perry", "Ava", "Lucky Lucy",
                       "Buster", "Mabel", "Beatrix", "Liam", "Old Man Keith", "Fletcher", "Crabby Addy",
                       "Francis", "Reverend Gus", "Jasper", "Sweets", "Viviana", "Milton", "Norm",
                       "Big Otis", "Sly", "Roy", "Sterling", "Famous Otis", "Martha"]

        counter = 0
        # This section creates blank slate characters
        while counter < numberofplayers:
            random.shuffle(playernames)
            randomname = playernames.pop()
            curplayer = Player(randomname)
            self.playerdict[randomname] = curplayer
            self.playerlist.append(randomname)
            counter += 1
        self.playerdict["You"] = Player("You")
        self.playerlist.append("You")

        # This section makes them play against each other and change rankings
        # Matchups are completely random, want to make it so peoplw who show up at different times play each other.
        counter = 0
        while counter < gamestoprep:
            p1num = random.randint(0,numberofplayers-1)
            p2num = random.randint(0,numberofplayers-1)
            while p1num == p2num:
                p2num = random.randint(0, numberofplayers-1)
            winner, loser, winamount = self.aiMatch(self.playerdict[self.playerlist[p1num]],self.playerdict[self.playerlist[p2num]])
            winner.applymatchtorank(True, winamount)
            loser.applymatchtorank(False, -1*winamount)
            counter += 1
        self.rankleague()
        self.createsavefile()

    def rankleague(self):
        tempArray = []
        for player in self.playerlist:
            curplayer = self.playerdict[player]
            tempArray.append([curplayer.name, curplayer.score])

        rankedArray = []
        while tempArray != []:
            curplayer = tempArray.pop(0)
            if rankedArray == []:
                rankedArray.append(curplayer)
            else:
                counter = 0
                while True:
                    try:
                        checkplayer = rankedArray[counter]
                        if curplayer[1] >= checkplayer[1]:
                            rankedArray.insert(counter, curplayer)
                            break
                        else:
                            counter += 1
                    except:
                        rankedArray.append(curplayer)
                        break
        rank = 1
        for player in rankedArray:
            player.insert(0, rank)
            self.rankedDict[player[1]] = rank
            rank += 1

        return rankedArray

    def createsavefile(self):
        playerdict = self.playerdict.copy()
        playerlist = self.playerlist.copy()

        savefile = {"playerdict": playerdict,
                    "playerlist": playerlist,
                    }
        pickle.dump(savefile, open('savefiles/tavernleague.pkl', "wb"))

    def loadsavefile(self):
        savefile = pickle.load(open("savefiles/tavernleague.pkl", "rb"))
        self.playerdict = savefile["playerdict"]
        self.playerlist = savefile["playerlist"]

    def aiMatch(self, player1, player2):
        # Right now this is completely randomized, in future versions I want to have them play real games
        whowon = None
        wholost = None
        byhowmuch = 0
        winner = random.randint(0,100)
        if winner > 50:
            whowon = player2
            wholost = player1
            byhowmuch = winner-50
        else:
            whowon = player1
            wholost = player2
            byhowmuch = winner
        whowon.gamesplayed += 1
        whowon.wins += 1
        wholost.gamesplayed += 1

        return whowon, wholost, byhowmuch


class RankingBoard:
    def __init__(self, league, x, y, width, height, myplayername):
        self.league = league
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rankArray = []
        self.myplayername = myplayername
        self.rankDict = {}


    def topten(self):
        tempArray = []
        for player in self.league.playerlist:
            curplayer = self.league.playerdict[player]
            tempArray.append([curplayer.name, curplayer.score])

        rankedArray = []
        while tempArray != []:
            curplayer = tempArray.pop(0)
            if rankedArray == []:
                rankedArray.append(curplayer)
            else:
                counter = 0
                while True:
                    try:
                        checkplayer = rankedArray[counter]
                        if curplayer[1] >= checkplayer[1]:
                            rankedArray.insert(counter, curplayer)
                            break
                        else:
                            counter += 1
                    except:
                        rankedArray.append(curplayer)
                        break
        rank = 1
        for player in rankedArray:
            player.insert(0, rank)
            self.rankDict[player[1]] = rank
            rank += 1

        return rankedArray


    def draw(self, window):
        background = pygame.image.load("scroll.png")
        window.blit(background, (self.x, self.y))
        nfont = pygame.font.Font('alagard.ttf', 40)
        toptencolor = (140, 185, 209)
        nametext = nfont.render("Top Ten", 1, yellow)
        rank1 = Cardslot(toptencolor, self.x+45, self.y+90, self.width-100, 40, None, False, str(self.rankArray[0][0])+" - "+str(self.rankArray[0][1])+" - "+str(self.rankArray[0][2]))
        window.blit(render("Top Ten", nfont, gfcolor=yellow, ocolor=black), (self.x + self.width / 2 - nametext.get_width() / 2, self.y + 20))
        rank2 = Cardslot(toptencolor, rank1.x, rank1.y+rank1.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[1][0])+" - "+self.rankArray[1][1]+" - "+str(self.rankArray[1][2]))
        rank3 = Cardslot(toptencolor, rank1.x, rank2.y+rank2.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[2][0])+" - "+self.rankArray[2][1]+" - "+str(self.rankArray[2][2]))
        rank4 = Cardslot(toptencolor, rank1.x, rank3.y+rank3.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[3][0])+" - "+self.rankArray[3][1]+" - "+str(self.rankArray[3][2]))
        rank5 = Cardslot(toptencolor, rank1.x, rank4.y+rank4.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[4][0])+" - "+self.rankArray[4][1]+" - "+str(self.rankArray[4][2]))
        rank6 = Cardslot(toptencolor, rank1.x, rank5.y+rank5.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[5][0])+" - "+self.rankArray[5][1]+" - "+str(self.rankArray[5][2]))
        rank7 = Cardslot(toptencolor, rank1.x, rank6.y+rank6.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[6][0])+" - "+self.rankArray[6][1]+" - "+str(self.rankArray[6][2]))
        rank8 = Cardslot(toptencolor, rank1.x, rank7.y+rank7.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[7][0])+" - "+self.rankArray[7][1]+" - "+str(self.rankArray[7][2]))
        rank9 = Cardslot(toptencolor, rank1.x, rank8.y+rank8.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[8][0])+" - "+self.rankArray[8][1]+" - "+str(self.rankArray[8][2]))
        rank10 = Cardslot(toptencolor, rank1.x, rank9.y+rank9.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[9][0])+" - "+self.rankArray[9][1]+" - "+str(self.rankArray[9][2]))
        rankings = [rank1,rank2,rank3,rank4,rank5,rank6,rank7,rank8,rank9,rank10]
        for player in rankings:
            if player.name == str(self.rankDict[self.myplayername])+ " - "+self.myplayername+ " - "+str(self.rankArray[int(self.rankDict[self.myplayername]) - 1][2]):
                player.color = (120, 36, 199)
                break
        for rank in rankings:
            rank.draw(window, outline=True)

        pygame.display.flip()


class Gametables:
    def __init__(self,x, y, width, height):
        self.seatcolor = (92, 224, 187)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sitDict = {"table1":["Open","Open"],
                        "table2": ["Open", "Open"],
                        "table3": ["Open", "Open"],
                        "table4": ["Open", "Open"]}
        self.seat1 = Cardslot(self.seatcolor, self.x + 224, self.y + 55, 150, 40, None, False, name=str(self.sitDict["table1"][0]))
        self.seat2 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 125, 150, 40, None, False, name=str(self.sitDict["table1"][1]))
        self.seat3 = Cardslot(self.seatcolor, self.seat1.x + 210, self.seat1.y, 150, 40, None, False, name=str(self.sitDict["table2"][0]))
        self.seat4 = Cardslot(self.seatcolor, self.seat3.x, self.seat3.y + 125, 150, 40, None, False, name=str(self.sitDict["table2"][1]))
        self.seat5 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 180, 150, 40, None, False, name=str(self.sitDict["table3"][0]))
        self.seat6 = Cardslot(self.seatcolor, self.seat1.x, self.seat5.y + 125, 150, 40, None, False, name=str(self.sitDict["table3"][1]))
        self.seat7 = Cardslot(self.seatcolor, self.seat5.x + 210, self.seat5.y, 150, 40, None, False, name=str(self.sitDict["table4"][0]))
        self.seat8 = Cardslot(self.seatcolor, self.seat7.x, self.seat7.y + 125, 150, 40, None, False, name=str(self.sitDict["table4"][1]))



    def draw(self, window):
        bg = pygame.image.load("map.png")
        table = pygame.image.load("taverntable.png")
        window.blit(bg,(self.x, self.y))
        window.blit(table, (self.x+250,self.y+100))
        window.blit(table, (self.x+460,self.y+100))
        window.blit(table, (self.x+250,self.y+280))
        window.blit(table, (self.x+460,self.y+280))
        self.seat1 = Cardslot(self.seatcolor, self.x + 224, self.y + 55, 150, 40, None, False, name=str(self.sitDict["table1"][0]))
        self.seat1.draw(window, outline=True)
        self.seat2 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 125, 150, 40, None, False, name=str(self.sitDict["table1"][1]))
        self.seat2.draw(window, outline=True)
        self.seat3 = Cardslot(self.seatcolor, self.seat1.x + 210, self.seat1.y, 150, 40, None, False, name=str(self.sitDict["table2"][0]))
        self.seat3.draw(window, outline=True)
        self.seat4 = Cardslot(self.seatcolor, self.seat3.x, self.seat3.y + 125, 150, 40, None, False, name=str(self.sitDict["table2"][1]))
        self.seat4.draw(window, outline=True)
        self.seat5 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 180, 150, 40, None, False, name=str(self.sitDict["table3"][0]))
        self.seat5.draw(window, outline=True)
        self.seat6 = Cardslot(self.seatcolor, self.seat1.x, self.seat5.y + 125, 150, 40, None, False, name=str(self.sitDict["table3"][1]))
        self.seat6.draw(window, outline=True)
        self.seat7 = Cardslot(self.seatcolor, self.seat5.x + 210, self.seat5.y, 150, 40, None, False, name=str(self.sitDict["table4"][0]))
        self.seat7.draw(window, outline=True)
        self.seat8 = Cardslot(self.seatcolor, self.seat7.x, self.seat7.y + 125, 150, 40, None, False, name=str(self.sitDict["table4"][1]))
        self.seat8.draw(window, outline=True)
        pygame.display.flip()

    def aitablepick(self):
        tablepick = random.randint(0,3)
        seatpick = random.randint(0,1)
        if tablepick == 0:
            table = "table1"
            if seatpick == 0:
                locnum = 0
            else:
                locnum = 1
        elif tablepick == 1:
            table = "table2"
            if seatpick == 0:
                locnum = 2
            else:
                locnum = 3
        elif tablepick == 2:
            table = "table3"
            if seatpick == 0:
                locnum = 4
            else:
                locnum = 5
        elif tablepick == 3:
            table = "table4"
            if seatpick == 0:
                locnum = 6
            else:
                locnum = 7


        return table, seatpick, locnum


    def playerupdate(self, window):
        pass


class PlayerStats:
    def __init__(self,x, y, width, height, name, wins, rank, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.wins = wins
        self.rank = rank
        self.score = score
        self.playercolor = (120, 36, 199)

    def draw(self, window):
        bg = pygame.image.load("myscroll.png")
        window.blit(bg,(self.x, self.y))

        nameslot = Cardslot(self.playercolor, self.x+100,self.y+self.height/2-40,150,50,None,False,self.name)
        nameslot.draw(window, outline=True)
        rankslot = Cardslot(self.playercolor, nameslot.x + nameslot.width + 40, self.y + self.height / 2 - 45, 75, 60, None, False, strength="Rank", priority=str(self.rank))
        rankslot.draw(window, outline=True)
        scoreslot = Cardslot(self.playercolor, rankslot.x + rankslot.width + 40, self.y + self.height / 2 - 45, 75, 60, None, False, strength="Score", priority=str(self.score))
        scoreslot.draw(window, outline=True)
        winslot = Cardslot(self.playercolor, scoreslot.x + scoreslot.width + 40, self.y + self.height / 2 - 45, 70, 60, None, False, strength="Wins", priority=str(self.wins))
        winslot.draw(window, outline=True)
        pygame.display.flip()

    def applyMatchToStats(self, win, byhowmuch):
        scorechange = round(byhowmuch/5)
        if win:
            self.wins += 1
            self.score += scorechange

        else:
            if self.score-scorechange<= 0:
                self.score = 0
            else:
                self.score = self.score-scorechange

