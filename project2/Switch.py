# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015


from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):    
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        
        # Define a data structure to keep track of which links are part of / not part of the spanning tree.

        # Switch ID this switch currently sees as root. Initially it is the root.
        self.current_root = self.switchID
        self.distance_to_root = 0

        # The links to neighbors that should be drawn in the spanning tree
        self.active_links = set()

        # The neighbour this switch goes through to get to the root. Initially None.
        self.next_hop = None

    def send_initial_messages(self):
        # This function needs to create and send the initial messages from this switch.
        # Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        # Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)

        # Message's parameters from Message.py: claimedRoot, distanceToRoot, originID, destinationID, pathThrough
        # root (claimedRoot) = id of the switch thought to be the root by the origin switch
        # distance (distanceToRoot) = the distance from the origin to the root node
        # origin (originID) =  the ID of the origin switch
        # destination (destinationID) = the ID of the destination switch
        # pathThrough (pathThrough) = Boolean value indicating the path to the claimed root from the origin passes
        # through the destination

        for node in self.links:
            message = Message(
                claimedRoot=self.switchID,
                distanceToRoot=0,
                originID=self.switchID,
                destinationID=node,
                pathThrough=False
            )

            self.send_message(message=message)
        
    def process_message(self, message):
        # This function needs to accept an incoming message and process it accordingly.
        # This function is called every time the switch receives a new message.

        def send_messages_to_links():
            """ Send messages to all nodes to which a link exists """

            for node in self.links:
                # C.1.c.iii - pathThrough should only be TRUE if the destinationID
                # switch is the neighbor that the originID switch goes through to get to the
                # claimedRoot. Otherwise, pathThrough should be FALSE.
                path_through_to_root = (self.next_hop == node)

                msg = Message(
                    claimedRoot=self.current_root,
                    distanceToRoot=self.distance_to_root,
                    originID=self.switchID,
                    destinationID=node,
                    pathThrough=path_through_to_root
                )

                self.send_message(msg)

        def update_path_to_root():
            """ Change path to root by updating the next hop and the set of active links """

            # set.discard doesn't raise an exception if element is not in set. set.remove does.
            self.active_links.discard(self.next_hop)

            self.next_hop = message.origin

            # set.add is a no-op if element is already in the set.
            self.active_links.add(self.next_hop)

        update_and_send_messages = False

        # C.1.a.i & C.1.a.ii.a - Message has lower root ID - update root and distance to root. Update path to root and
        # send messages to links.
        if message.root < self.current_root:
            self.current_root = message.root
            self.distance_to_root = message.distance + 1

            update_and_send_messages = True

        # C.1.a.ii.b - Message has lesser distance to root, but same root - update distance to root. Update path to
        # root and send messages to links.
        if message.distance + 1 < self.distance_to_root and message.root == self.current_root:
            self.distance_to_root = message.distance + 1

            update_and_send_messages = True

        # C.1.b.i - Message has same root and distance, but message origin has smaller switchID than next hop - Update
        # path to root and send messages to links.
        if (message.root == self.current_root and message.distance + 1 == self.distance_to_root
                and message.origin < self.next_hop):
            update_and_send_messages = True

        # C.1.c.i - Send messages to links after updating path to root.
        if update_and_send_messages:
            update_path_to_root()
            send_messages_to_links()

        # C.1.b.ii in Project 2 description - add a link as the path to root for another node passes through
        # current node.
        if message.pathThrough:
            self.active_links.add(message.origin)

        # C.1.b.iii in Project 2 description - don't remove the current next hop as we don't know if current node
        # still needs it to reach root until other conditions are evaluated later.
        # E.g: We don't know which of other_node_1, other_node_2 and next_hop should be the next hop to reach root
        # until distances and switch IDs are evaluated.
        #
        #                      [other_node_1] ---------------|
        #                        |                           |
        #      [other_node_3] - [root] - [next_hop] - [current_node]
        #                                    |               |
        #                                [other_node_2] -----|
        #
        if not message.pathThrough and message.origin != self.next_hop:
            self.active_links.discard(message.origin)
        
    def generate_logstring(self):
        # This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.

        links = []

        for node in sorted(self.active_links):
            links.append("{0} - {1}".format(self.switchID, node))

        return ", ".join(links)
