'''
Function:
    Python小游戏合集
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import warnings
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    from modules import *
else:
    from .modules import *
warnings.filterwarnings('ignore')


'''Python实用工具集'''
class CPGames():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_games = self.initialize()
    '''执行对应的小程序'''
    def execute(self, game_type=None, config={}):
        assert game_type in self.supported_games, 'unsupport game_type %s...' % game_type
        qt_games = ['tetris', 'gobang']
        if game_type in qt_games:
            app = QApplication(sys.argv)
            client = self.supported_games[game_type](**config)
            client.show()
            sys.exit(app.exec_())
        else:
            client = self.supported_games[game_type](**config)
            client.run()
    '''初始化'''
    def initialize(self):
        supported_games = {
            #'ski': SkiGame,            #pygame滑雪，已可以自动玩
            #'maze': MazeGame,          #pygame迷宫，已可以自动玩
            #'gobang': GobangGame,      #Qt五子棋，可局域网联网
            #'tetris': TetrisGame,      #Qt俄罗斯方块
            #'pacman': PacmanGame,      #pygame小精灵吃米
            #'gemgem': GemGemGame,      #pygame消消乐
            #'tankwar': TankWarGame,    #pygame坦克大战，可以自己玩
            #'sokoban': SokobanGame,        #pygame推箱子
            #'pingpong': PingpongGame,      #pygame打乒乓
            #'trexrush': TRexRushGame,       #pygame小恐龙
            #'bomberman': BomberManGame,     #pygame炸弹人
            #'whacamole': WhacAMoleGame,     #打地鼠
            #'catchcoins': CatchCoinsGame,   #pygame接金币
            #'flappybird': FlappyBirdGame,   #pygame飞扬的小鸟
            #'angrybirds': AngryBirdsGame,  #pygame愤怒小鸟
            #'magictower': MagicTowerGame,  
            #'aircraftwar': AircraftWarGame,    #飞机打陨石，可以自动玩
            'bunnybadger': BunnyBadgerGame,     #pygame兔子和獾射击游戏，可以研究如何自动玩
            #'minesweeper': MineSweeperGame,
            #'greedysnake': GreedySnakeGame,
            #'puzzlepieces': PuzzlePiecesGame,
            #'towerdefense': TowerDefenseGame,
            #'alieninvasion': AlienInvasionGame,
            #'breakoutclone': BreakoutcloneGame,
            #'twentyfourpoint': TwentyfourPointGame,
            #'flipcardbymemory': FlipCardByMemoryGame,
            #'twozerofoureight': TwoZeroFourEightGame,
            #'voicecontrolpikachu': VoiceControlPikachuGame,
        }
        return supported_games
    '''获得所有支持的游戏信息'''
    def getallsupported(self):
        all_supports = {}
        for key, value in self.supported_games.items():
            all_supports[value.game_type] = key
        return all_supports
    '''repr'''
    def __repr__(self):
        return 'Python小游戏合集; 作者: Charles; 微信公众号: Charles的皮卡丘'


'''run'''
if __name__ == '__main__':
    import random
    games_client = CPGames()
    all_supports = games_client.getallsupported()
    games_client.execute(random.choice(list(all_supports.values())))