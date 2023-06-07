# Modified DDPG car-following model with a real-world human driving experience with CARLA simulator

## About the work

In the autonomous driving field, fusion of human knowledge into Deep Reinforcement Learning (DRL) is often based on the human demonstration recorded in a simulated environment. This limits the generalization and the feasibility of application in real-world traffic. We propose a two-stage DRL method to train a car-following agent, that modifies the policy by leveraging the real-world human driving experience and achieves performance superior to the pure DRL agent. Training a DRL agent is done within CARLA framework with Robot Operating System (ROS). For evaluation, we designed different driving scenarios to compare the proposed two-stage DRL car-following agent with other agents. After extracting the “good” behavior from the human driver, the agent becomes more efficient and reasonable, which makes this autonomous agent more suitable to Human–Robot Interaction (HRI) traffic.

[Paper](https://www.sciencedirect.com/science/article/abs/pii/S0968090X22004004)
