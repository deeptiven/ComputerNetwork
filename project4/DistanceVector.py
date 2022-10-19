# Project 4 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *


class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        # Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        self.NEGATIVE_INFINITY = -99        # per project description
        self.INFINITE_EDGE_WEIGHT = float('inf')

        # Distance to self is 0
        self.distance_vector = {self.name: 0}


    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for node in self.incoming_links:
            self.send_msg(msg=(self.name, self.distance_vector), dest=node.name)


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:

        # Process queued messages
        send_message = False

        for msg in self.messages:
            neighbour, neighbour_dv = msg

            for node in neighbour_dv:
                # Do not process self
                if node == self.name:
                    continue

                # Add node to self's distance vector - initialize to high value
                if node not in self.distance_vector:
                    self.distance_vector[node] = self.INFINITE_EDGE_WEIGHT

                # c(x,v)
                distance_to_neighbour = max(int(self.get_outgoing_neighbor_weight(neighbour)), self.NEGATIVE_INFINITY)
                # Dv(y)
                distance_from_neighbour_to_node = max(neighbour_dv[node], self.NEGATIVE_INFINITY)

                # Calculate distance from self to node
                if (distance_to_neighbour == self.NEGATIVE_INFINITY or
                        distance_from_neighbour_to_node == self.NEGATIVE_INFINITY):
                    # Negative infinite cycle: If distance to neighbour is -99 or
                    # distance from neighbour to node is -99, distance from self to node is -99
                    total_distance = self.NEGATIVE_INFINITY
                else:
                    # {c(x,v) + Dv(y)}, ensuring minimum weight is always -99
                    total_distance = max(distance_to_neighbour + distance_from_neighbour_to_node,
                                         self.NEGATIVE_INFINITY)

                # Bellman - Ford equation: min{c(x,v) + Dv(y), Dx(y)}
                if total_distance < self.distance_vector[node]:
                    self.distance_vector[node] = total_distance
                    send_message = True

        # Empty queue
        self.messages = []

        # Send neighbors updated distances
        if send_message:
            for node in self.incoming_links:
                self.send_msg(msg=(self.name, self.distance_vector), dest=node.name)


    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.
        add_entry(self.name, ",".join(["{0}{1}".format(node, self.distance_vector[node])
                                       for node in self.distance_vector]))
