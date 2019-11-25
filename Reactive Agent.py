
from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random


class TerranAgent(base_agent.BaseAgent):

    def __init__(self):
        super(TerranAgent, self).__init__()
        self.attack_coordinates = None
        # self.pos1 = False
        # self.camera = False
        # self.sselect = False
        self.attackcount = 0
        self.sepx = 7
        self.sepy = 7
        self.supply_depots = [[50,57], [10,10]]
        self.sup = [(self.supply_depots[0]),                                                                 #1 50,60
                    (self.supply_depots[0][0],self.sepy+self.supply_depots[0][1]),                            #2 50,65
                    (self.supply_depots[0][0]+self.sepx,self.supply_depots[0][1]),                            #3 55,60
                    (self.supply_depots[0][0]+self.sepx,self.supply_depots[0][1] + self.sepy)]

        self.sdown = [(self.supply_depots[1]),                                                               #01 10,10
                   (self.supply_depots[1][0], self.sepy + self.supply_depots[1][1]),                         #02 10,15
                   (self.supply_depots[1][0] + self.sepx, self.supply_depots[1][1]),                         #03 15,10
                   (self.supply_depots[1][0] + self.sepx, self.supply_depots[1][1] + self.sepy)]

        self.barracksup = [[70,60], [75,45]]
        self.barracksdown =[[20,40],[35,15]]
        self.i = 0

        # This verifies if the operation you want to do is available
    def can_do(self, obs, action):
        return action in obs.observation.available_actions

    # def my_move_camera(self, obs):
    #     if  self.camera == True:
    #         self.camera = False
    #         return actions.FUNCTIONS.move_camera(self.base)

    # This verifies if a unit or several units are selected
    def unit_type_is_selected(self, obs, unit_type):  # Check selection
        if (len(obs.observation.single_select) > 0 and
                obs.observation.single_select[0].unit_type == unit_type):
            return True
        if (len(obs.observation.multi_select) > 0 and
                obs.observation.multi_select[0].unit_type == unit_type):
            return True

        return False

    # This generates the array of units of any unit_type generated
    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units
                if unit.unit_type == unit_type]

    def supply_depot(self, obs):
        supply_depot = self.get_units_by_type(obs, units.Terran.SupplyDepot)
        food_cap = obs.observation.player.food_cap

        if len(supply_depot) < 4 or food_cap < 30:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
                    if self.pos1:
                        self.i += 1
                        if self.i == 5:
                            self.i = 1
                        print(self.i)
                        print(self.sup[self.i-1])
                        return actions.FUNCTIONS.Build_SupplyDepot_screen("now", ((self.sup[self.i-1][0]),(self.sup[self.i-1][1])))
                    else:
                        self.i += 1
                        if self.i == 5:
                            self.i = 1
                        print(self.i)
                        print(self.sdown[self.i-1])
                        return actions.FUNCTIONS.Build_SupplyDepot_screen("now", ((self.sdown[self.i-1][0]),(self.sdown[self.i-1][1])))
            else:
                SCV = self.get_units_by_type(obs, units.Terran.SCV)
                if len(SCV) > 0:
                    SCV = random.choice(SCV)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(SCV.x), abs(SCV.y)))

    def refinery(self, obs):
        refinery = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(refinery) == 0:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Refinery_screen.id):
                    geysers = self.get_units_by_type(obs, units.Neutral.VespeneGeyser)
                    if len(geysers) > 0:
                        geyser = random.choice(geysers)
                        return actions.FUNCTIONS.Build_Refinery_screen("now", (abs(geyser.x), abs(geyser.y)))

            else:
                SCV = self.get_units_by_type(obs, units.Terran.SCV)
                if len(SCV) > 0:
                    SCV = random.choice(SCV)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(SCV.x), abs(SCV.y)))

    def barracks(self, obs):
        barracks = self.get_units_by_type(obs, units.Terran.Barracks)
        if len(barracks) < 2:
            if self.unit_type_is_selected(obs, units.Terran.SCV):
                if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
                    if self.pos1:
                        self.i += 1
                        if self.i > 2:
                            self.i = 0
                        print(self.i)
                        return actions.FUNCTIONS.Build_Barracks_screen("now", (self.barracksup[self.i]))
                    else:
                        self.i += 1
                        if self.i > 2:
                            self.i = 0
                        print(self.i)
                        return actions.FUNCTIONS.Build_Barracks_screen("now", (self.barracksdown[self.i]))
            else:
                SCV = self.get_units_by_type(obs, units.Terran.SCV)
                if len(SCV) > 0:
                    SCV = random.choice(SCV)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(SCV.x), abs(SCV.y)))

    def reactor(self, obs):
        reactor = self.get_units_by_type(obs, units.Terran.BarracksReactor)
        if len(reactor) < 2:
            if self.unit_type_is_selected(obs, units.Terran.Barracks):
                if self.can_do(obs, actions.FUNCTIONS.Build_Reactor_quick.id):
                    print("Reactor Step if")
                    return actions.FUNCTIONS.Build_Reactor_quick("now")
            else:
                barracks = self.get_units_by_type(obs, units.Terran.Barracks)
                if len(barracks) > 0:
                    print("Reactor Step else")
                    barracks = random.choice(barracks)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(barracks.x), abs(barracks.y)))

    def gas(self, obs):
        gaseslist = self.get_units_by_type(obs, units.Terran.Refinery)
        if len(gaseslist) == 1:
            gases = random.choice(gaseslist)
            if gases['assigned_harvesters'] < 1:
                SCV = self.get_units_by_type(obs, units.Terran.SCV)
                if len(SCV) > 0:
                    SCV = random.choice(SCV)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(SCV.x), abs(SCV.y)))
                if self.unit_type_is_selected(obs, units.Terran.SCV):
                    if self.can_do(obs, actions.FUNCTIONS.Harvest_Gather_screen.id):
                      return actions.FUNCTIONS.Harvest_Gather_screen("now", (abs(gases.x), abs(gases.y)))

    def workers(self, obs):
        refinery = self.get_units_by_type(obs, units.Terran.Refinery)
        if self.unit_type_is_selected(obs, units.Terran.SCV) and (len(obs.observation.single_select) < 2 and len(obs.observation.multi_select) <2) and self.sselect == False:
            if len(refinery) > 0:
                refinery = random.choice(refinery)
                if refinery['assigned_harvesters'] < 1:
                    if self.can_do(obs, actions.FUNCTIONS.Harvest_Gather_screen.id):
                        self.sselect = True
                        return actions.FUNCTIONS.Harvest_Gather_screen("now", (abs(refinery.x), abs(refinery.y)))
        else:
            self.sselect = False
            self.camera = True
            return actions.FUNCTIONS.select_idle_worker("select")

    def train(self, obs):
            if self.unit_type_is_selected(obs, units.Terran.Barracks):
                if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
                    return actions.FUNCTIONS.Train_Marine_quick("now")
            else:
                barracks = self.get_units_by_type(obs, units.Terran.Barracks)
                if len(barracks) > 0:
                    barracks = random.choice(barracks)
                    return actions.FUNCTIONS.select_point("select_all_type", (abs(barracks.x), abs(barracks.y)))

    def attack(self, obs):
        marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(marines) > 27:
            if self.unit_type_is_selected(obs, units.Terran.Marine):
                if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
                    self.attackcount+=1
                    if self.attackcount == 3:
                        self.attackcount = 1
                    return actions.FUNCTIONS.Attack_minimap("now", self.attack_coordinates[self.attackcount-1])
            else:
                if self.can_do(obs, actions.FUNCTIONS.select_army.id):
                    return actions.FUNCTIONS.select_army("select")

    # Here are defined all the actions that our agent will do
    def step(self, obs):
        super(TerranAgent, self).step(obs)  # Call 'super' to gain access to inherited methods which is either from a parent or sibling class.

        if obs.first():  # Check if first step
            player_y, player_x = (obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
            xmean = player_x.mean()
            ymean = player_y.mean()
            if xmean <= 31 and ymean <= 31:  # Select coordinates to atttack
                self.pos1 = True
                self.attack_coordinates = [[40, 45],[20,45]]
                self.base = (20, 25)
            else:
                self.pos1 = False
                self.attack_coordinates = [[20, 25], [40,26]]
                self.base = (40, 45)

        supply_depot = self.supply_depot(obs)
        if supply_depot:
            return supply_depot


        refinery = self.refinery(obs)
        if refinery:
            print("Refinery step")
            return refinery

        my_gas = self.gas(obs)
        if my_gas:
            print("Gas Step")
            return my_gas

        barracks = self.barracks(obs)
        if barracks:
            return barracks

        reactor = self.reactor(obs)
        if reactor:
            return reactor

        attack = self.attack(obs)
        if attack:
            print("Attack Step")
            return attack

        marines = self.get_units_by_type(obs, units.Terran.Marine)
        if len(marines) < 50:
            print(len(marines))
            make_units = self.train(obs)
            if make_units:
                return make_units

        if actions.FUNCTIONS.select_idle_worker.id in obs.observation["available_actions"]:
            workerss = self.workers(obs)
            if workerss:
                return workerss

        return actions.FUNCTIONS.no_op()  # do not do anything if there were no matches


def main(unused_argv):
    agent = TerranAgent()  # Start agent
    try:
        while True:  # Run function indefinitely
            with sc2_env.SC2Env(  # Setup environment

                    map_name="Simple64",

                    players=[sc2_env.Agent(sc2_env.Race.terran),  # Player 1 is agent, player 2 is a very easy bot
                             sc2_env.Bot(sc2_env.Race.random,
                                         # It's possible to change 'Bot' to 'Agent' for another agent
                                         sc2_env.Difficulty.hard)],

                    agent_interface_format=features.AgentInterfaceFormat(
                        feature_dimensions=features.Dimensions(screen=84, minimap=64),  # Screen and minimap resolutions
                        use_feature_units=True),  # Feature units list

                    step_mul=8,
                    game_steps_per_episode=0,
                    visualize=True) as env:

                agent.setup(env.observation_spec(), env.action_spec())  # what is spec?

                timesteps = env.reset()
                agent.reset()

                while True:
                    step_actions = [agent.step(timesteps[0])]  # how does this work?
                    if timesteps[0].last():
                        break
                    timesteps = env.step(step_actions)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    app.run(main)
