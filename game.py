from basic import *
import config
import os
from itertools import chain


__metaclass__ = type

class GameEvent(Transferable):
    pass

class EObjMove(GameEvent):
    def __init__(self, obj, action, args):
        self.obj = obj
        self.action = action
        self.args = args

class EObjVanish(GameEvent):
    def __init__(self, obj):
        self.obj = obj

class ETankShoot(GameEvent):
    def __init__(self, tank):
        self.tank = tank

class ETankHurt(GameEvent):
    def __init__(self, tank, damage):
        self.tank = tank
        self.bullet = damage

class Game(Transferable):
    def __init__(self):
        self.tanks = []
        self.bullets = []
        self.players = []
        self.obstacles = []
        self.round = 0
        self.events = []
        self.fps = 0

    def add_player(self, player):
        self.players.append(player)
        if player.tank:
            self.tanks.append(player.tank)

    def bu_hit_bu(self, b1, b2):
        # bullet hit bullet
        print 'bu hit bu'
        b1.boom()
        b2.boom()
        # self.events.append(EObjVanish(b1))
        # self.events.append(EObjVanish(b2))

    def bu_hit_tank(self, b, t):
        # bullet hits tank
        print 'bu hit tank', self.round
        b.boom()
        t.v += b.v.normalized() * b.I / t.m
        t.health -= b.damage
        # lost energy, can be proportional to damage
        # self.events.append(EObjVanish(b))
        # self.events.append(ETankHurt(t, b.damage))

    def bu_hit_ob(self, bu, ob):
        bu.boom()

    def tk_hit_ob(self, t, ob):
        s = (ob.pos - t.pos).normalized()
        t.v = t.v - (2 *(t.v * s) + 20) * s
        lt, rt = 0, 1.0/self.fps
        ct = lt
        while rt - lt > 0.001:
            mt = (lt + rt) / 2
            print lt, mt, rt
            t.move(mt - ct)
            if t.hittest(ob):
                rt = mt
            else:
                lt = mt
            ct = mt

    def tank_hit_tank(self, t1, t2):
        print 'tk hit tk', self.round
        I = (t2.pos - t1.pos).normalized() * config.hitI
        t1.v -= I/t1.m
        t2.v += I/t2.m
        t1.move(0.0001)
        t2.move(0.0001)

    def exist_hit(self):
        for o1 in chain(self.bullets, self.tanks):
            for o2 in chain(self.bullets, self.tanks, self.obstacles):
                if o1.hittest(o2):
                    return o1, o2
        return None

    def hittest(self):
        for b1 in self.bullets:
            if b1.active:
                for b2 in self.bullets:
                    if b2.active and b1.hittest(b2):
                        self.bu_hit_bu(b1, b2)
                        break
            if b1.active:
                for t2 in self.tanks:
                    if t2.active and b1.hittest(t2):
                        self.bu_hit_tank(b1, t2)
                        break
            if b1.active:
                for ob in self.obstacles:
                    if b1.hittest(ob):
                        self.bu_hit_ob(b1, ob)
                        break
        for t1 in self.tanks:
            if t1.active:
                for t2 in self.tanks:
                    if t1 != t2 and t2.active and t1.hittest(t2):
                        self.tank_hit_tank(t1, t2)
            if t1.active:
                for ob in self.obstacles:
                    if t1.hittest(ob):
                        self.tk_hit_ob(t1, ob)
                        break

    def apply(self):
        for b in chain(self.bullets, self.obstacles, self.tanks):
            if b.active:
                b.apply()

        self.bullets = [b for b in self.bullets if b.active]
        self.tanks = [b for b in self.tanks if b.active]

    def move(self, dt):
        for obj in chain(self.bullets, self.tanks, self.obstacles):
            obj.move(dt)

    def start(self):
        self.round = 0
        self.events = []

    def obj_hittest(self, obj):
        for obj1 in chain(self.tanks, self.obstacles):
            if obj.hittest(obj1):
                return obj1
        return None

    def handle_react(self):
        dAngle = config.dAngle
        dAngle1 = config.dAngle1
        for plr in self.players:
            if not plr.tank.active: continue
            s = plr.react(self)
            t = plr.tank
            angle1 = 0
            if 'L' in s:
                angle1 -= dAngle
            if 'R' in s:
                angle1 += dAngle

            if 'U' in s:
                t.engineSide = 1
            elif 'D' in s:
                t.engineSide = -1
            else:
                t.engineSide = 0

            if 'J' in s:
                t.rotate2(-dAngle1)
            if 'K' in s:
                t.rotate2(dAngle1)

            if angle1:
                t.rotate1(angle1)
                if self.obj_hittest(t):
                    t.rotate1(-angle1)
            if 'S' in s and t.shootReady:
                bullet = t.shoot()
                self.bullets.append(bullet)

    def debug_print(self):
        print self.bullets
        print self.tanks
        print self.obstacles
        print '-' * 80

    def loop(self, dt):
        # import pdb; pdb.set_trace()
        self.round += 1
        # self.debug_print()
        # ask for react
        self.handle_react()
        # logic
        dt0 = dt / config.logicCnt
        while dt > 0:
            dt1 = min(dt0, dt)
            lt, rt = 0.0, dt1
            self.move(rt)
            if self.exist_hit():
                ct = rt
                # binary search
                while rt - lt > 0.01:
                    mt = (rt + lt) / 2
                    self.move(mt - ct)
                    if self.exist_hit():
                        rt = mt
                    else:
                        lt = mt
                    ct = mt
                self.move(rt - ct)
                self.hittest()
            # apply
            dt -= rt
            # apply movements
            self.apply()
