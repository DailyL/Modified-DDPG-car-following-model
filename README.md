# Modified DDPG car-following model with a real-world human driving experience with CARLA simulator

## About the work

<p align = "center">
<img src="/images/introduction.jpg" width="600">
</p>

In the autonomous driving field, fusion of human knowledge into Deep Reinforcement Learning (DRL) is often based on the human demonstration recorded in a simulated environment. This limits the generalization and the feasibility of application in real-world traffic. We propose a two-stage DRL method to train a car-following agent, that modifies the policy by leveraging the real-world human driving experience and achieves performance superior to the pure DRL agent. Training a DRL agent is done within CARLA framework with Robot Operating System (ROS). For evaluation, we designed different driving scenarios to compare the proposed two-stage DRL car-following agent with other agents. After extracting the “good” behavior from the human driver, the agent becomes more efficient and reasonable, which makes this autonomous agent more suitable to Human–Robot Interaction (HRI) traffic.

[Paper](https://www.sciencedirect.com/science/article/abs/pii/S0968090X22004004)

## Prerequisites

* Operating System: Ubuntu 18.04 or 20.04
* [ROS (Melodic or Noetic)](http://wiki.ros.org/noetic/Installation/Ubuntu)
* Programming Language: Python 2 (Python 3 for ROS Noetic)
* [CARLA 0.9.11](https://carla.readthedocs.io/en/0.9.11/) (other version might also work, but this work used 0.9.11)
* Tensorflow
 


## Installation
### This repo is a CARLA-ROS Bridge package with modification by the author (RL algorithm). By cloning this repo, replace the official CARLA-ROS Bridge package, but you need to setup to make it runs on your local machine.

* First, clone this repo to your local machine:

```bash
$ git clone https://github.com/DailyL/Modified-DDPG-car-following-model.git
```
and setup the CARLA-ROS Bridge package follow the [official instruction](https://carla.readthedocs.io/en/0.9.11/ros_installation/) to fit your local machine.  

* Make sure that [CARLA 0.9.11](https://carla.readthedocs.io/en/0.9.11/) is properly installed. 

## Training

* First, follow the [instruction](https://carla.readthedocs.io/en/0.9.11/start_quickstart/#running-carla) to start the CARLA client. 
Then start to train the pure DDPG agent: 

```bash
roslaunch rl_agent ddpg.launch
```
The weights will be saved in [model folder](https://github.com/DailyL/Modified-DDPG-car-following-model/carla-ros-bridge/catkin_ws/src/ros-bridge/rl_agent/src/model).

* For continue training:

```bash
roslaunch rl_agent ddpg_continue.launch
```

The Napoli dataset used for continued training is already converted into pickle file.
To change the speed profile of the **leading vehicle**, change the parameter in [launch file](https://github.com/DailyL/Modified-DDPG-car-following-model/carla-ros-bridge/catkin_ws/src/ros-bridge/rl_agent/launch).

```bash
<param name="mode" default="napoli" doc="which leader profile used for evaluation (napoli;ngsim;or self_defined)" /> 
```
## Evaluation

For evaluation, simple change the training_indicator in [python script](Modified-DDPG-car-following-model/carla-ros-bridge/catkin_ws/src/ros-bridge/rl_agent/src/ddpg.py) into 0, and then run 

```bash
roslaunch rl_agent ddpg.launch
```
or 

```bash
roslaunch rl_agent ddpg_continue.launch
```


## Citation of this work:

```bibtex
@article{li2023modified,
  title={Modified DDPG car-following model with a real-world human driving experience with CARLA simulator},
  author={Li, Dianzhao and Okhrin, Ostap},
  journal={Transportation Research Part C: Emerging Technologies},
  volume={147},
  pages={103987},
  year={2023},
  publisher={Elsevier}
}
```
