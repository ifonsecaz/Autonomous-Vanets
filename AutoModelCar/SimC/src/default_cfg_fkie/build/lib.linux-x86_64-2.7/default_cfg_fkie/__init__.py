#! /usr/bin/env python3
#
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Fraunhofer FKIE/US, Alexander Tiderko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Fraunhofer nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import signal
import sys
import traceback

import roslib
import rospy

from default_cfg import DefaultCfg


PROCESS_NAME = "default_cfg"


def set_terminal_name(name):
    '''
    Change the terminal name.
    @param name: New name of the terminal
    @type name:  C{str}
    '''
    sys.stdout.write("".join(["\x1b]2;", name, "\x07"]))


def set_process_name(name):
    '''
    Change the process name.
    @param name: New process name
    @type name:  C{str}
    '''
    try:
        from ctypes import cdll, byref, create_string_buffer
        libc = cdll.LoadLibrary('libc.so.6')
        buff = create_string_buffer(len(name) + 1)
        buff.value = name
        libc.prctl(15, byref(buff), 0, 0, 0)
    except:
        pass


def main():
    '''
    Creates and runs the ROS node
    '''
    # setup the loglevel
    try:
        log_level = getattr(rospy, rospy.get_param('/%s/log_level' % PROCESS_NAME, "INFO"))
    except Exception as e:
        print ("Error while set the log level: %s\n->INFO level will be used!" % e)
        log_level = rospy.INFO
    rospy.init_node(PROCESS_NAME, log_level=log_level)
    set_terminal_name(PROCESS_NAME)
    set_process_name(PROCESS_NAME)
    try:
        default_cfg = DefaultCfg()
        default_cfg.load()
    except:
        # on load error the process will be killed to notify user in node_manager
        # about error
        rospy.logwarn("%s", traceback.format_exc())
        sys.stdout.write(traceback.format_exc())
        sys.stdout.flush()
        os.kill(os.getpid(), signal.SIGKILL)
    rospy.spin()
