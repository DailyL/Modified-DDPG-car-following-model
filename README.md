# Modified DDPG car-following model with a real-world human driving experience with CARLA simulator

## About the work

Deep Reinforcement Learning (DRL) has shown remarkable success in solving complex tasks across various research fields. However, transferring DRL agents to the real world is still challenging due to the significant discrepancies between simulation and reality. To address this issue, we propose a robust DRL framework that leverages platform-dependent perception modules to extract task-relevant information and train a lane-following and overtaking agent in simulation. This framework facilitates the seamless transfer of the DRL agent to new simulated environments and the real world with minimal effort. We evaluate the performance of the agent in various driving scenarios in both simulation and the real world, and compare it to human players and the PID baseline in simulation. Our proposed framework significantly reduces the gaps between different platforms and the Sim2Real gap, enabling the trained agent to achieve similar performance in both simulation and the real world, driving the vehicle effectively.

<p align = "center">
<img src="/assets/overall_system_hor.jpg" width="600">
</p>


[Project website](https://dailyl.github.io/sim2realVehicle.github.io/)   
[Paper](https://arxiv.org/abs/2304.08235)
