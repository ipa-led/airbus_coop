#!/usr/bin/env python
#
# Copyright 2015 Airbus
# Copyright 2017 Fraunhofer Institute for Manufacturing Engineering and Automation (IPA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from airbus_docgen.digraph.digraph import *
from airbus_docgen.digraph.model.topic import *
from airbus_docgen.digraph.model.package import *

class IO_TYPE:
    Input  = 'Input'
    Output = 'Output'

def getActionTRModel(io_type, topic_name, data_class, bgcolor=RgbColor.White, align = ALIGN.Left):
    
    model = TR()
    
    model.addTD(getStandardTDModel(io_type, bgcolor, align))
    model.addTD(getStandardTDModel(topic_name, bgcolor, align))
    model.addTD(getStandardTDModel(data_class, bgcolor, align))
    
    return model


class ActionClientModel(NODE):
    
    def __init__(self, server_name, action_msg):
        
        NODE.__init__(self, server_name)
        
        table = TABLE()
        table.setAttrib(TABLE.BORDER, 0)
        table.setAttrib(TABLE.CELLBORDER, 1)
        table.setAttrib(TABLE.CELLSPACING, 0)
        table.setAttrib(TABLE.BGCOLOR, RgbColor.White)
        
        title = TD()
        title.setAttrib(TD.ALIGN, ALIGN.Center)
        title.setAttrib(TD.BGCOLOR, RgbColor.LightGreen)
        title.setAttrib(TD.COLSPAN, 3)
        title.setText('Action client "%s"'%server_name)
        table.addTR(TR(title))
        
        header = getActionTRModel("I/O", "Topic name", "Message type", bgcolor=RgbColor.LightGray, align=ALIGN.Center)
        table.addTR(header)
        
        goal = getActionTRModel(IO_TYPE.Output, "%s/goal"%server_name, "%sGoal"%action_msg)
        table.addTR(goal)
        
        cancel = getActionTRModel(IO_TYPE.Output, "%s/cancel"%server_name, "actionlib_msgs::GoalID")
        table.addTR(cancel)
        
        status = getActionTRModel(IO_TYPE.Input, "%s/status"%server_name, "actionlib_msgs::GoalStatus")
        table.addTR(status)
        
        feedback = getActionTRModel(IO_TYPE.Input, "%s/feedback"%server_name, "%sFeedback"%action_msg)
        table.addTR(feedback)
        
        result = getActionTRModel(IO_TYPE.Input, "%s/result"%server_name, "%sResult"%action_msg)
        table.addTR(result)
        
        self.setHtml(table)
    
class ActionServerModel(NODE):
    
    def __init__(self, server_name, action_msg):
        
        NODE.__init__(self, server_name)
        
        table = TABLE()
        table.setAttrib(TABLE.BORDER, 0)
        table.setAttrib(TABLE.CELLBORDER, 1)
        table.setAttrib(TABLE.CELLSPACING, 0)
        table.setAttrib(TABLE.BGCOLOR, RgbColor.White)
        
        title = TD()
        title.setAttrib(TD.ALIGN, ALIGN.Center)
        title.setAttrib(TD.BGCOLOR, RgbColor.LightGreen)
        title.setAttrib(TD.COLSPAN, 3)
        title.setText('Action server "%s"'%server_name)
        table.addTR(TR(title))
        
        header = getActionTRModel("I/O", "Topic name", "Message type", bgcolor=RgbColor.LightGray, align=ALIGN.Center)
        table.addTR(header)
        
        goal = getActionTRModel(IO_TYPE.Input, "%s/goal"%server_name, "%sGoal"%action_msg)
        table.addTR(goal)
        
        cancel = getActionTRModel(IO_TYPE.Input, "%s/cancel"%server_name, "actionlib_msgs::GoalID")
        table.addTR(cancel)
        
        status = getActionTRModel(IO_TYPE.Output, "%s/status"%server_name, "actionlib_msgs::GoalStatus")
        table.addTR(status)
        
        feedback = getActionTRModel(IO_TYPE.Output, "%s/feedback"%server_name, "%sFeedback"%action_msg)
        table.addTR(feedback)
        
        result = getActionTRModel(IO_TYPE.Output, "%s/result"%server_name, "%sResult"%action_msg)
        table.addTR(result)
        
        self.setHtml(table)
        
def digraph_test():
    
    digraph = Digraph("digraph_test")
    digraph.setAttrib(Digraph.NODESEP, 0.8)
    
    nconf = NODE("node")
    nconf.setAttrib(NODE.SHAPE, SHAPE.Plaintext)
    digraph.addNode(nconf)
    
    pkg = NODE("joint_trajectory_executor_node")
    pkg.setAttrib(NODE.SHAPE, SHAPE.Ellipse)
    pkg.setAttrib(NODE.STYLE, STYLE.FILLED)
    pkg.setAttrib(NODE.COLOR, RgbColor.CornflowerBlue)
    pkg.setAttrib(NODE.FONTSIZE, 22)
    digraph.addNode(pkg)
    
    ns = ActionServerModel("/joint_path_command", "trajectory_msgs::JointTrajectory")
    digraph.addNode(ns)
    
    subs = SubscribersModel()
    subs.addSubscriber("/joint_path_command","geometry_msgs::Twist1")
    subs.addSubscriber("/joint_path_command","geometry_msgs::Twist2")
    subs.addSubscriber("/joint_path_command","geometry_msgs::Twist3")
    subs.addSubscriber("/joint_path_command","geometry_msgs::Twist4")
    digraph.addNode(subs)
    
    pubs = PublishersModel()
    pubs.addSubscriber("/joint_path_command","geometry_msgs::Twist1")
    pubs.addSubscriber("/joint_path_command","geometry_msgs::Twist2")
    pubs.addSubscriber("/joint_path_command","geometry_msgs::Twist3")
    pubs.addSubscriber("/joint_path_command","geometry_msgs::Twist4")
    digraph.addNode(pubs)
    
    digraph.connect(ns, pkg, Edge(Edge.DIR, "both"))
    digraph.connect(subs, pkg)
    digraph.connect(pkg, pubs)
    
    print str(digraph)
    
    digraph.saveDot("/home/ihm-pma/Documents/dot_test/ns_test.dot")
    digraph.dotToPng("/home/ihm-pma/Documents/dot_test/ns_test.png")
    

if __name__ == '__main__':
    
    digraph_test()
    
