# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here

    # Comment and uncommentduing the lab to perfrorm different trajectories
    def trajectory_planner(self):
        import math

        pts = []
        ############ parabola ############
        # x0, x1 = 0.0, 1.5 #x goes from 0 to 1.5
        # num_points = 25 #extract 25 points in total
        # for i in range(num_points):
        #     # linspace
        #     x = x0 + (x1 - x0) * i / (num_points - 1)
        #     y = x * x
        #     pts.append([x, y])
        # print("pts ", pts)


        ############ sigmoid ############
        x0, x1 = 0.0, 2.5 #x goes from 0 to 2.5
        num_points = 25 #extract 25 points in total

        for i in range(num_points):
            # linspace
            x = x0 + (x1 - x0) * i / (num_points - 1)
            y = 2.0 / (1.0 + math.exp(-2.0 * x)) - 1.0
            pts.append([x, y])
        print("pts ", pts)

        # the return should be a list of trajectory points: [ [x1,y1], ..., [xn,yn]]
        return pts

