
from mapUtilities import *
from utilities import *
from numpy import cos, sin
import numpy as np


class particle:

    def __init__(self, pose, weight):
        self.pose = pose
        self.weight = weight

    def motion_model(self, v, w, dt):
        #TODO: Implement the motion model for the particle
        """
        v: linear velocity
        w: angular velocity
        dt: time step
        """
        self.pose[0] += v * cos(self.pose[2]) * dt
        self.pose[1] += v * sin(self.pose[2]) * dt
        self.pose[2] += w * dt

    # TODO: You need to explain the following function to TA
    def calculateParticleWeight(self, scanOutput: LaserScan, mapManipulatorInstance: mapManipulator, laser_to_ego_transformation: np.array):
        
        # transformation from laser to map
        T = np.matmul(self.__poseToTranslationMatrix(), laser_to_ego_transformation)

        # convert scan to cartesian and transform to map frame
        _, scanCartesianHomo = convertScanToCartesian(scanOutput)
        scanInMap = np.dot(T, scanCartesianHomo.T).T

        #Get the likelihood field(2D array, size same as number of grids) and map indices(pixle positions)
        likelihoodField = mapManipulatorInstance.getLikelihoodField()
        cellPositions = mapManipulatorInstance.position_2_cell(
            scanInMap[:, 0:2])

        # filter out any transformed scan points that lie outside the known map dimensions
        lm_x, lm_y = likelihoodField.shape
        cellPositions = cellPositions[np.logical_and.reduce(
                (cellPositions[:, 0] > 0, -cellPositions[:, 1] > 0, cellPositions[:, 0] < lm_y,  -cellPositions[:, 1] < lm_x))]

        # Compute log-likelihood for all valid beams
        """
        For each valid beam endpoint, it looks up the likelihood value in the map (likelihoodField[y, x]).
        Takes the log of all those probabilities and sums them → this is the log-likelihood of the entire scan under that particle’s pose.
        Exponentiating gives a final unnormalized weight.
        Adding a small epsilon prevents numerical underflow.
        If a particle's predicted scan endpoints line up with high-probability regions (near walls/obstacles in the map), their individual likelihoods are high → the sum of logs is high → that particle's weight increases.
        If scan endpoints fall into free space far from any obstacle, the likelihoods are tiny → low weight.
        """
        log_weights = np.log(
            likelihoodField[-cellPositions[:, 1], cellPositions[:, 0]])
        log_weight = np.sum(log_weights)
        weight = np.exp(log_weight)
        weight += 1e-10

        self.setWeight(weight)

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setPose(self, pose):
        self.pose = pose

    def getPose(self):
        return self.pose[0], self.pose[1], self.pose[2]

    def __poseToTranslationMatrix(self):
        x, y, th = self.getPose()

        translation = np.array([[cos(th), -sin(th), x],
                                [sin(th), cos(th), y],
                                [0, 0, 1]])

        return translation
