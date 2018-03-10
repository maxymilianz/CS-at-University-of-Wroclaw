import pygame
from enum import Enum, unique
from random import choice


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


@unique
class Controls(Enum):
    exit = 0
    pause = 1


@unique
class States(Enum):
    menu = 0
    waiting = 1
    animations = 2


@unique
class Directions(Enum):
    left = 0
    right = 1


@unique
class Collectibles(Enum):
    fire = 0
    water = 1
    mud = 2
    no_oxygen = 3
    electricity = 4
    bomb = 5
    weight = 6
    poison = 7

    recover = 100
    health = 101
    shield = 102

    independence = 200


@unique
class Sprites(Enum):
    bg0 = 0

    character0die_r = 10
    character0hit_r = 11
    character0idle_r = 12
    character0run_r = 13

    character0die_l = 14
    character0hit_l = 15
    character0idle_l = 16
    character0run_l = 17

    corridor0 = 100
    corridor1 = 101
    corridor2 = 102
    corridor3 = 103

    fire = 200
    water = 201
    mud = 202
    no_oxygen = 203
    electricity = 204
    bomb = 205
    weight = 206
    poison = 207

    recover = 300
    health = 301
    shield = 302

    independence = 400


def image(path, flip_y = False, scale = 1):
    img = pygame.image.load(path)

    if flip_y:
        img = pygame.transform.flip(img, False, True)

    if scale != 1:
        img = pygame.transform.scale(img, (round(img.get_width() * scale), round(img.get_height() * scale)))

    return img


class Sprite:
    # NOT SURE IF THIS SHOULD STAY
    collectible_to_sprite = {Collectibles.fire: Sprites.fire, Collectibles.water: Sprites.water, Collectibles.mud: Sprites.mud, Collectibles.no_oxygen: Sprites.no_oxygen,
                             Collectibles.electricity: Sprites.electricity, Collectibles.bomb: Sprites.bomb, Collectibles.weight: Sprites.weight,
                             Collectibles.poison: Sprites.poison, Collectibles.recover: Sprites.recover, Collectibles.health: Sprites.health,
                             Collectibles.shield: Sprites.shield, Collectibles.independence: Sprites.independence}

    collectible_to_effect_sprite = collectible_to_sprite

    @staticmethod
    def get_sprite(enum):
        return Sprite.sprites[enum]

    @staticmethod
    def init():
        bg0_img = Image('res/bgs/space0.jpg')

        character0die_r_paths = ['res/characters/0d0.png', 'res/characters/0d1.png', 'res/characters/0d2.png', 'res/characters/0d3.png', 'res/characters/0d4.png',
                                 'res/characters/0d5.png']
        character0hit_r_paths = ['res/characters/0h0.png', 'res/characters/0h1.png', 'res/characters/0h2.png']
        character0idle_r_paths = ['res/characters/0i0.png', 'res/characters/0i1.png', 'res/characters/0i2.png', 'res/characters/0i3.png', 'res/characters/0i4.png',
                                  'res/characters/0i5.png']
        character0run_r_paths = ['res/characters/0r0.png', 'res/characters/0r1.png', 'res/characters/0r2.png', 'res/characters/0r3.png', 'res/characters/0r4.png',
                                 'res/characters/0r5.png', 'res/characters/0r6.png']

        character0die_r_anim = Animation(character0die_r_paths)
        character0hit_r_anim = Animation(character0hit_r_paths)
        character0idle_r_anim = Animation(character0idle_r_paths)
        character0run_r_anim = Animation(character0run_r_paths)

        character0die_l_anim = Animation(character0die_r_paths, True)
        character0hit_l_anim = Animation(character0hit_r_paths, True)
        character0idle_l_anim = Animation(character0idle_r_paths, True)
        character0run_l_anim = Animation(character0run_r_paths, True)

        corridor0img = Image('res/corridors/0cr.png')
        corridor1img = Image('res/corridors/1cr.png')
        corridor2img = Image('res/corridors/2cr.png')
        corridor3img = Image('res/corridors/3c.png')

        fire_paths = ['res/fx/fire0.gif', 'res/fx/fire1.gif', 'res/fx/fire2.gif', 'res/fx/fire3.gif', 'res/fx/fire4.gif', 'res/fx/fire5.gif', 'res/fx/fire6.gif',
                      'res/fx/fire7.gif', 'res/fx/fire8.gif', 'res/fx/fire9.gif', 'res/fx/fire10.gif', 'res/fx/fire11.gif', 'res/fx/fire12.gif', 'res/fx/fire13.gif',
                      'res/fx/fire14.gif', 'res/fx/fire15.gif']
        fire_anim = Animation(fire_paths, scale = 112/256)

        electricity_paths = ['res/fx/electricity0.gif', 'res/fx/electricity1.gif', 'res/fx/electricity2.gif', 'res/fx/electricity3.gif', 'res/fx/electricity4.gif',
                             'res/fx/electricity5.gif', 'res/fx/electricity6.gif', 'res/fx/electricity7.gif']
        electricity_anim = Animation(electricity_paths, scale = 112/600)

        bomb_paths = ['res/fx/bomb0.gif', 'res/fx/bomb1.gif']
        bomb_anim = Animation(bomb_paths, scale = .1)

        poison_paths = ['res/fx/poison0.gif', 'res/fx/poison1.gif', 'res/fx/poison2.gif', 'res/fx/poison3.gif', 'res/fx/poison4.gif']
        poison_anim = Animation(poison_paths, scale = 100/1280)

        health_paths = ['res/fx/health14.gif', 'res/fx/health13.gif', 'res/fx/health12.gif', 'res/fx/health11.gif', 'res/fx/health10.gif', 'res/fx/health9.gif',
                        'res/fx/health8.gif', 'res/fx/health7.gif', 'res/fx/health6.gif', 'res/fx/health5.gif', 'res/fx/health4.gif', 'res/fx/health3.gif',
                        'res/fx/health2.gif', 'res/fx/health1.gif', 'res/fx/health0.gif']
        health_anim = Animation(health_paths, scale = 112/200)

        water_img = Image('res/fx/water.png', scale = 112/2400)

        mud_img = Image('res/fx/mud.png', scale = 112/173)

        no_oxygen_img = Image('res/fx/no_oxygen.png', scale = 112/512)

        weight_img = Image('res/fx/weight.png', scale = 112/512)

        recover_img = Image('res/fx/recover.png', scale = 112/300)

        shield_img = Image('res/fx/shield.png', scale = 112/512)

        independence_img = Image('res/fx/independence.png', scale = 112/200)

        Sprite.sprites = {Sprites.bg0: bg0_img, Sprites.character0die_r: character0die_r_anim, Sprites.character0hit_r: character0hit_r_anim,
                          Sprites.character0idle_r: character0idle_r_anim, Sprites.character0run_r: character0run_r_anim, Sprites.character0die_l: character0die_l_anim,
                          Sprites.character0hit_l: character0hit_l_anim, Sprites.character0idle_l: character0idle_l_anim, Sprites.character0run_l: character0run_l_anim,
                          Sprites.corridor0: corridor0img, Sprites.corridor1: corridor1img, Sprites.corridor2: corridor2img, Sprites.corridor3: corridor3img,
                          Sprites.fire: fire_anim, Sprites.bomb: bomb_anim, Sprites.electricity: electricity_anim, Sprites.poison: poison_anim,
                          Sprites.health: health_anim, Sprites.water: water_img, Sprites.mud: mud_img, Sprites.no_oxygen: no_oxygen_img, Sprites.weight: weight_img,
                          Sprites.recover: recover_img, Sprites.shield: shield_img, Sprites.independence: independence_img}

    def get_image(self):
        pass


class Image(Sprite):
    def __init__(self, path, inverse = False, scale = 1):
        super().__init__()
        self.image = image(path, inverse, scale)

    def get_image(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    @staticmethod
    def init():
        raise AttributeError('This function is not implemented for Image class.')

    @staticmethod
    def get_sprite(enum):
        raise AttributeError('This function is not implemented for Image class.')


class Animation(Sprite):
    def __init__(self, paths, inverse = False, scale = 1):
        super().__init__()
        self.images = list(map(lambda path: image(path, inverse, scale), paths))

        self.n = 0
        self.image = self.images[self.n]

    def get_image(self):
        self.n += 1

        if self.n == len(self.images):
            self.n = 0

        return self.images[self.n]

    def get_size(self):
        return self.images[self.n].get_size()

    def get_width(self):
        return self.images[self.n].get_width()

    def get_height(self):
        return self.images[self.n].get_height()

    @staticmethod
    def init():
        raise AttributeError('This function is not implemented for Animation class.')

    @staticmethod
    def get_sprite(enum):
        raise AttributeError('This function is not implemented for Animation class.')


class Text(Sprite):
    def __init__(self, text, font, color):
        super().__init__()
        self.image = font.render(text, True, color)

    def get_image(self):
        return self.image

    def get_size(self):
        return self.image.get_size()

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    @staticmethod
    def init():
        raise AttributeError('This function is not implemented for Text class.')

    @staticmethod
    def get_sprite(enum):
        raise AttributeError('This function is not implemented for Text class.')


class Input:
    @staticmethod
    def update():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Controls.exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Controls.pause
                elif event.key in {pygame.K_a, pygame.K_LEFT}:
                    return Directions.left
                elif event.key in {pygame.K_d, pygame.K_RIGHT}:
                    return Directions.right

        return None


class Point:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    # no accessors due to the size of the class and convenience of using it


class Displayable:
    def __init__(self, sprite, point):
        self.sprite = sprite
        self.point = point

    # no accessors due to the size of the class and convenience of using it


class Screen:
    def __init__(self, res, flags, game):
        self.res = Point(res)
        self.game = game
        self.maps = game.get_maps()
        self.screen = pygame.display.set_mode(res, flags)

        self.left_capsule_center_x, self.right_capsule_center_x = 79, 372

        self.font = pygame.font.SysFont('Arial', 64, True)        # this should be changed to a font that matches the games aesthetics

        self.init_bg()
        self.init_corridors()
        self.init_characters()
        self.init_collectibles()
        self.init_effects()
        self.init_gui()

    def init_bg(self):      # position (2nd element of tuple) grows to right and upside (0, 0 is lower left)
        self.bg = Displayable(Sprite.get_sprite(Sprites.bg0), Point((0, self.res.y)))

    def init_corridors(self):
        assert self.bg

        map_count = len(self.maps)
        corridor_size = Point(Sprite.get_sprite(Sprites.corridor0).get_size())
        empty_y = (self.res.y - map_count*corridor_size.y) / (map_count + 1)
        next_y = empty_y

        corridor_enums = [choice([Sprites.corridor0, Sprites.corridor1, Sprites.corridor2, Sprites.corridor3]) for i in range(map_count)]
        self.corridors = []

        for enum in corridor_enums:
            self.corridors += [Displayable(Sprite.get_sprite(enum), Point(((self.res.x - corridor_size.x) / 2, self.res.y - next_y)))]
            next_y += corridor_size.y + empty_y

    def init_characters(self):      # in this method the height of character over corridor level is defined implicitly
        assert self.corridors

        map_count = len(self.maps)

        corridor_size = Point(self.corridors[0].sprite.get_size())
        character_size = Point(Sprite.get_sprite(Sprites.character0idle_r).get_size())

        character_enums = [choice([Sprites.character0idle_r]) for i in range(map_count)]
        self.characters = []

        for enum, corridor in zip(character_enums, self.corridors):
            pos = corridor.point
            self.characters += [Displayable(Sprite.get_sprite(enum),
                                            Point((pos.x + (corridor_size.x - character_size.x) / 2, pos.y - corridor_size.y + character_size.y - 2)))]

    def init_collectibles(self):
        assert self.corridors

        corridor_pos = self.corridors[0].point

        collectible_enum_lists = self.game.get_collectibles()
        self.collectibles = []

        for (left, right), corridor in zip(collectible_enum_lists, self.corridors):     # font and positions should be different
            corridor_y = corridor.point.y

            left_img = Sprite.get_sprite(Sprite.collectible_to_sprite[left[0]])
            left_img_x = left_img.get_width()
            self.collectibles += [Displayable(left_img, Point((corridor_pos.x + self.left_capsule_center_x - left_img_x / 2, corridor_y)))]

            right_img = Sprite.get_sprite(Sprite.collectible_to_sprite[right[0]])
            right_img_x = right_img.get_width()
            self.collectibles += [Displayable(right_img, Point((corridor_pos.x + self.right_capsule_center_x - right_img_x / 2, corridor_y)))]

    def init_effects(self):
        self.effects = self.collectibles

    def init_gui(self):
        assert self.maps

        self.health_texts = []
        self.burning_texts = []     # this should be replaced with fire sprite at characters position
        self.armor_texts = []

        for c, m in zip(self.game.get_characters(), self.corridors):
            map_coords = m.point

            self.health_texts += [Displayable(Text(str(c.get_health()), self.font, (255, 0, 0)), Point((0, map_coords.y)))]
            if c.is_burning():
                self.burning_texts += [Displayable(Text('Fire', self.font, (255, 0, 0)), Point((100, map_coords.y)))]
            self.armor_texts += [Displayable(Text(str(c.get_armor()), self.font, (0, 0, 255)), Point((300, map_coords.y)))]

    def update(self):
        self.draw_bg()
        self.draw_corridors()
        self.draw_characters()

        if self.game.get_state == States.waiting:       # TODO create, handle and display menu
            self.draw_collectibles()
        else:
            self.draw_effects()

        self.init_gui()
        self.draw_gui()

        pygame.display.flip()

    def draw_inv_y(self, displayable):
        sprite, pos = displayable.sprite, displayable.point
        self.screen.blit(sprite.get_image(), (pos.x, self.res.y - pos.y))

    def draw_bg(self):
        self.draw_inv_y(self.bg)

    def draw_corridors(self):
        for corridor in self.corridors:
            self.draw_inv_y(corridor)

    def draw_characters(self):
        for character, x in zip(self.characters, self.game.get_characters_x()):
            pos = self.corridors[0].point
            corridor_size = Point(self.corridors[0].sprite.get_size())
            character_size = Point(character.sprite.get_size())
            character.point.x = pos.x + (corridor_size.x - character_size.x) / 2 + x * (self.right_capsule_center_x - self.left_capsule_center_x) / 2
            self.draw_inv_y(character)

    def draw_collectibles(self):
        for collectible in self.collectibles:
            self.draw_inv_y(collectible)

    def draw_effects(self):
        for effect in self.effects:
            self.draw_inv_y(effect)

    def draw_gui(self):
        for text in self.health_texts + self.burning_texts + self.armor_texts:
            self.draw_inv_y(text)


class Game:
    # how long effect works on character
    work_times = {Collectibles.fire: 1, Collectibles.water: 0, Collectibles.mud: 0, Collectibles.no_oxygen: 0, Collectibles.electricity: 0, Collectibles.bomb: 0,
                  Collectibles.weight: 0, Collectibles.poison: 1, Collectibles.recover: 0, Collectibles.health: 0, Collectibles.shield: 0, Collectibles.independence: 0}

    # how long effect stays on map
    map_times = {Collectibles.fire: 1, Collectibles.water: 1, Collectibles.mud: 1, Collectibles.no_oxygen: 1, Collectibles.electricity: 1, Collectibles.bomb: 1,
                 Collectibles.weight: 1, Collectibles.poison: 1, Collectibles.recover: 1, Collectibles.health: 1, Collectibles.shield: 1, Collectibles.independence: 1}

    collecting_time = 20     # frames, how long is a collectible being collected by a character

    def __init__(self):
        pygame.init()

        Sprite.init()

        self.quited = False

        self.round = 0

        self.character_count = 2

        self.maps = []
        self.init_maps()

        self.characters = []
        self.init_characters()

        self.decision_times = {0: self.characters}       # keys are consecutive naturals
        self.current_decision_time = 0
        self.max_decision_time = max(self.decision_times)

        self.comebacks = 0

        self.change_dependence = False

        self.screen = Screen((1280, 720), pygame.DOUBLEBUF, self)     # TODO check if DOUBLEBUF does anything
        self.input = Input()

        self.state = States.waiting      # TODO change

        self.go_center_times = {c: 0 for c in self.characters}

        self.run()

    def init_maps(self):
        assert self.maps == []

        for i in range(self.character_count):
            self.maps += [Map()]

    def init_characters(self):
        assert self.maps != [] and self.characters == []

        for map in self.maps:
            self.characters += [Character(map)]

    def run(self):
        while True:
            self.handle_input()
            self.update()
            if self.quited:
                break
            self.screen.update()

    def update(self):
        for c in self.characters:
            if c.has_collected():
                self.go_center_times[c] += 1
            if self.go_center_times[c] == Game.collecting_time:
                self.comebacks += 1
                c.go_center()
                self.go_center_times[c] = 0
            c.update()

        if self.turn_end():
            if [c for c in self.characters if c.dead()]:
                pygame.quit()
                self.quited = True
                print('You have lost :( but You have survived', str(self.round), 'rounds :)')

            if self.change_dependence:
                Character.independent_characters = False
                self.change_dependence = False

            if Character.independent_characters:
                self.change_dependence = True

            for c in self.characters:
                c.reset_effects()
                c.apply_effects()

            self.comebacks = 0
            for m in self.maps:
                m.update()
            self.screen.init_collectibles()
            self.screen.init_effects()

            self.round += 1

        if Character.independent_characters and len(self.decision_times) == 1:
            self.make_characters_independent()
        elif not Character.independent_characters and len(self.decision_times) != 1:
            self.make_characters_dependent()

    def make_characters_independent(self):
        for i in range(len(self.characters)):
            self.decision_times[i] = [self.characters[i]]
        self.max_decision_time = max(self.decision_times)

    def make_characters_dependent(self):
        self.decision_times = dict()
        self.decision_times[0] = self.characters
        self.max_decision_time = max(self.decision_times)

    def turn_end(self):
        return self.comebacks == self.character_count

    def handle_input(self):
        flag = Input.update()

        if flag == Controls.exit:
            self.exit()
        elif flag == Controls.pause:
            self.pause()
        elif flag in {Directions.left, Directions.right} and self.state == States.waiting:
            self.move(flag)
            self.update_decision_time()

    def exit(self):
        pygame.quit()

    def pause(self):
        pass # TODO

    def update_decision_time(self):
        if self.current_decision_time == self.max_decision_time:
            self.current_decision_time = 0
        else:
            self.current_decision_time += 1

    def move(self, direction):
        for character in self.decision_times[self.current_decision_time]:
            character.change_position(direction)

    def get_maps(self):
        return self.maps

    def get_characters(self):
        return self.characters

    def get_collectibles(self):
        return [map.get_collectibles() for map in self.maps]

    def get_state(self):
        return self.state

    def get_characters_x(self):
        return [c.get_x() for c in self.characters]

    @staticmethod
    def get_map_times():
        return Game.map_times


class Map:
    def __init__(self):
        self.left, self.right = ((None, 0),) * 2
        self.update()

    @staticmethod
    def random_collectible():
        return choice([Collectibles.fire, Collectibles.bomb, Collectibles.electricity, Collectibles.poison, Collectibles.health, Collectibles.water, Collectibles.mud,
                       Collectibles.fire, Collectibles.bomb, Collectibles.electricity, Collectibles.poison, Collectibles.water, Collectibles.mud,
                       Collectibles.no_oxygen, Collectibles.weight, Collectibles.no_oxygen, Collectibles.weight, Collectibles.recover, Collectibles.shield,
                       Collectibles.independence])

    def update(self):
        if self.left[1] == 0:
            c = Map.random_collectible()
            self.left = c, Game.get_map_times()[c] - 1
        if self.right[1] == 0:
            c = Map.random_collectible()
            self.right = c, Game.get_map_times()[c] - 1

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_collectibles(self):
        return self.left, self.right


class Character:
    @unique
    class State(Enum):
        left = 0
        moving_left = 1
        center = 2
        moving_right = 3
        right = 4
        moving_center = 5

    independent_characters = False

    def __init__(self, map):
        self.health_max = 10
        self.health = self.health_max
        self.burning = False
        self.armor_max = 10
        self.armor = 0

        self.map = map

        self.speed = .05
        self.x = 0      # -1 - on left, 1 - on right
        self.state = Character.State.center

        self.collects = {}      # Collectible -> how many turns will the effect remain
        self.collected = False

    def change_position(self, direction):
        if self.state == Character.State.center:
            if direction == Directions.left:
                self.state = Character.State.moving_left
            else:
                self.state = Character.State.moving_right

    def update(self):
        self.move()

        if self.state in {Character.State.left, Character.State.right} and not self.collected:
            self.collect()

    def reset_effects(self):
        self.burning = False

    def go_center(self):
        self.collected = False
        self.state = Character.State.moving_center

    def apply_effects(self):
        for c in [c for c in self.collects if self.collects[c] > 0]:
            Effect.collectible_to_effect[c[0]](self)
            self.collects[c] -= 1

    def move(self):
        if self.state == Character.State.moving_left:
            self.x -= self.speed
            if self.x <= -1:
                self.state = Character.State.left
                self.x = -1
        elif self.state == Character.State.moving_right:
            self.x += self.speed
            if self.x >= 1:
                self.state = Character.State.right
                self.x = 1
        elif self.state == Character.State.moving_center:
            sign_x = sign(self.x)
            self.x += -self.speed * sign_x
            if sign(self.x) != sign_x:
                self.state = Character.State.center
                self.x = 0

    def collect(self):
        assert self.state in {Character.State.left, Character.State.right}

        if self.state == Character.State.left:
            collectible = self.map.get_left()
        else:
            collectible = self.map.get_right()

        self.collects[collectible] = Game.work_times[collectible[0]]
        Effect.collectible_to_effect[collectible[0]](self)

        self.collected = True

    def take_damage(self, damage):
        absorbed = min(damage, self.armor)
        self.armor -= absorbed
        self.health -= damage - absorbed
        if self.health < 0:
            self.health = 0

    def dead(self):
        return self.health == 0

    def get_x(self):
        return self.x

    def get_health(self):
        return self.health

    def is_burning(self):
        return self.burning

    def get_armor(self):
        return self.armor

    def has_collected(self):
        return self.collected


class Effect:       # the following methods cannot be static, because they would not be callable then
    def fire(character):
        character.take_damage(1)
        character.burning = True

    def water(character):
        character.take_damage(1)
        character.burning = False

    def mud(character):
        character.take_damage(1)
        character.burning = False

    def no_oxygen(character):
        character.take_damage(1)
        character.burning = False

    def electricity(character):
        character.take_damage(1)

    def bomb(character):
        character.take_damage(2)
        character.burning = True

    def weight(character):
        character.take_damage(1)
        character.burning = False

    def poison(character):
        character.take_damage(1)

    def recover(character):
        character.health = character.health_max
        character.burning = False

    def health(character):
        character.health = min(character.health + 1, character.health_max)
        character.burning = False

    def shield(character):
        character.armor = character.armor_max
        character.burning = False

    def independence(character):        # arg is not used, but enables this method to be called like other ones in effects dict
        Character.independent_characters = True

    # Collectible -> function to apply on character
    collectible_to_effect = {Collectibles.fire: fire, Collectibles.water: water, Collectibles.mud: mud, Collectibles.no_oxygen: no_oxygen,
                             Collectibles.electricity: electricity, Collectibles.bomb: bomb, Collectibles.weight: weight, Collectibles.poison: poison,
                             Collectibles.recover: recover, Collectibles.health: health, Collectibles.shield: shield, Collectibles.independence: independence}