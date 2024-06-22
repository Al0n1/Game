__author__ = "Al0n1"
__version__ = "0.0.4"


import pygame as pg
import random

from config import Utils
from spritesheet import SpriteSheet


"""# Components
class PositionComponent:
    def __init__(self, pos, rect):
        self.pos = pos
        self.rect = rect


class HealthComponent:
    def __init__(self, health):
        self.health = health


class SpriteComponent:
    def __init__(self, sprite, frame_index=0):
        self.sprite = sprite
        self.frame_index = frame_index


class StateComponent:
    def __init__(self, state="idle"):
        self.state = state


class CooldownComponent:
    def __init__(self, cooldown, last_tick):
        self.cooldown = cooldown
        self.last_tick = last_tick


# Systems
class RenderSystem:
    def __init__(self, screen):
        self.screen = screen

    def display(self, entity):
        position = entity.get_component(PositionComponent)
        sprite = entity.get_component(SpriteComponent)
        state = entity.get_component(StateComponent)

        if position and sprite and state:
            self.screen.blit(
                sprite.sprite.parse_sprite(scale=Utils.SCALE_OF_MONSTERS_IN_CLICKER, sprite_index=sprite.frame_index, state=state.state),
                (position.pos[0], position.pos[1])
            )


class HealthSystem:
    def update(self, entity):
        health = entity.get_component(HealthComponent)
        state = entity.get_component(StateComponent)

        if health and state:
            if health.health <= 0:
                state.state = 'dead'


class InputSystem:
    def __init__(self, menu):
        self.menu = menu

    def handle_click(self, entity):
        state = entity.get_component(StateComponent)
        health = entity.get_component(HealthComponent)
        if state and health and state.state != 'dead':
            state.state = 'hurt'
            health.health -= self.menu.get_player().get_clicker_damage()

            if health.health < 1:
                health.health = 0
                state.state = 'dead'
                self.menu.get_player().change_money(Utils.REWARD_FOR_KILL)


class AnimationSystem:
    def update(self, entity):
        sprite = entity.get_component(SpriteComponent)
        state = entity.get_component(StateComponent)
        cooldown = entity.get_component(CooldownComponent)

        if sprite and state and cooldown:
            now = pg.time.get_ticks()
            if now - cooldown.last_tick >= cooldown.cooldown:
                cooldown.last_tick = now
                sprite.frame_index = (sprite.frame_index + 1) % sprite.sprite.get_number_of_frames(state.state)


# Initialization
def create_monster(screen):
    monster = Entity()
    monster.add_component(PositionComponent((50, 75), pg.Rect(50, 75, 96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER, 96 * Utils.SCALE_OF_MONSTERS_IN_CLICKER)))
    monster.add_component(HealthComponent(Utils.MONSTER_HP_IN_CLICKER))
    sprite = SpriteSheet(random.choice(Utils.MONSTERS_IN_CLICKER) + "_sheet_idle.png")
    monster.add_component(SpriteComponent(sprite))
    monster.add_component(StateComponent())
    monster.add_component(CooldownComponent(200, pg.time.get_ticks()))

    return monster"""


class Monster:
    def __init__(self, screen, state: bool = True, saved_data: dict = None):
        self.__screen: pg.Surface = screen
        self.__rect: pg.Rect = Utils.MONSTER_RECT

        self.__filename_of_sprite: str = ""
        self.__sprite: SpriteSheet = None
        self.__frame_index: int = 0
        self.__status_of_monster: str = "idle"
        self.__state = state
        self.__last_frame_tick: int = pg.time.get_ticks()
        self.__cooldown: int = 200
        self.__monster_sprite_data: dict = {}
        self.__already_dead: bool = False  # метка того, что анимация смерти уже проигрывается, если true, то клики
        # перестают обрабатываться

        self.__health: float = Utils.MONSTER_MAX_HP_IN_CLICKER
        self.__monster_name: str = None
        self.__monster_counter: int = 0
        self.__reward: int = 1

        self.__menu = None

        self.__monster_window: pg.Surface = pg.Surface(
            (Utils.MONSTER_BASE_WIDTH * Utils.SCALE_OF_MONSTERS_IN_CLICKER,
             Utils.MONSTER_BASE_HEIGHT * Utils.SCALE_OF_MONSTERS_IN_CLICKER)
        )

        self.change_monster(self.__monster_name)

    def display(self):
        if (self._get_frame_index() >= self._get_number_of_frames() - 1) and (self._get_status_of_monster() != "idle"):
            if self.__status_of_monster == 'dead':
                self.set_cooldown(500)
                if self._can_change_sprite():
                    self.__frame_index = 0
                    self.__status_of_monster = "idle"
                    self.change_monster()
                    self.__health = Utils.MONSTER_MAX_HP_IN_CLICKER
                    self.__already_dead = False
                    self.set_cooldown(200)
            else:
                self.__frame_index = 0
                self.__status_of_monster = "idle"
                self.change_monster(self.__monster_name)
        elif self._can_change_sprite():
            self.set_cooldown(200)
            self.change_frame_index()

        self.__screen.blit(
            self.__sprite.parse_sprite(scale=Utils.SCALE_OF_MONSTERS_IN_CLICKER, sprite_index=self.__frame_index,
                                       state=self.__status_of_monster), (100, 0))

    def click_action(self, mode: str):
        if not self.__already_dead:
            self.__status_of_monster = 'hurt'
            self.__frame_index = 0
            self.change_monster(self.__monster_name)  # Переключает спрайт стоящего зомби на зомби получающего удар
            self.change_hp_to_monster(-self.__menu.get_player().get_clicker_damage() if mode == "manual" else -self.__menu.get_game().get_auto_clicker().get_damage())

            # Обработка смерти монстра
            if self.__health < 1:
                if self.__health < 0:
                    self.__health = 0
                self.__status_of_monster = 'dead'
                self.increment_monster_counter()
                self.change_monster(self.__monster_name)
                self.__already_dead = True
                self.__menu.get_player().change_money(self.get_reward())
                if self.get_monster_counter() >= 10:
                    self.set_monster_counter(0)
                    Utils.MONSTER_MAX_HP_IN_CLICKER += 5
                    self.__menu.get_player().increment_stage()
                    self.increment_reward()

    def change_monster(self, monster_name: str = None):
        self.__monster_name = random.choice(Utils.MONSTERS_IN_CLICKER) if monster_name is None else monster_name
        self.__filename_of_sprite = self.__monster_name + f"_sheet_{self.__status_of_monster}.png"
        self.__sprite = SpriteSheet(self.__filename_of_sprite)
        self.__monster_sprite_data = self.__sprite.get_data()

    def set_name(self, name: str):
        self.__monster_name = name

    def change_monster_state(self, state):
        self.__state = state

    def change_monster_status(self, status):
        self.__status_of_monster = status

    def set_hp_to_monster(self, value: float):
        self.__health = value

    def change_hp_to_monster(self, value: float):
        self.__health += value

    def get_hp(self):
        return self.__health

    def get_rect(self) -> pg.Rect:
        return self.__rect

    def change_frame_index(self):
        self.__frame_index = (self.__frame_index + 1) % (self._get_number_of_frames())

    def set_cooldown(self, value: int):
        self.__cooldown = value

    def _can_change_sprite(self) -> bool:
        now = pg.time.get_ticks()
        if now - self.__last_frame_tick >= self.__cooldown:
            self.__last_frame_tick = now
            return True
        else:
            return False

    def get_state(self) -> bool:
        return self.__state

    def _get_status_of_monster(self) -> str:
        return self.__status_of_monster

    def _get_number_of_frames(self) -> int:
        return self.__monster_sprite_data[self._get_status_of_monster()]["info"]["numbers_of_frames"]

    def _get_frame_index(self) -> int:
        return self.__frame_index

    def set_menu(self, menu):
        self.__menu = menu

    def get_menu(self):
        return self.__menu

    def increment_monster_counter(self):
        self.__monster_counter += 1

    def set_monster_counter(self, value: int):
        self.__monster_counter = value

    def get_monster_counter(self) -> int:
        return self.__monster_counter

    def get_name(self) -> str:
        return self.__monster_name

    def set_reward(self, reward: int):
        self.__reward = reward

    def get_reward(self) -> int:
        return self.__reward

    def increment_reward(self):
        self.__reward += 1
