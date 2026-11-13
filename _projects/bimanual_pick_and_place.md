---
layout: page
title: Bimanual Pick-and-Place
description: Industry project with LG (Sep 2025 – Feb 2026). Reinforcement learning in simulation, transferred to a real dual-arm robot.
img: assets/img/bimanual_pallet_to_table.jpg
importance: 2
---

An industry project with LG, from September 2025 to February 2026. I worked on both sides of the pipeline: training the policies with reinforcement learning in simulation, and transferring them to the real robot.

The task is bimanual pick-and-place. Two arms move a part between a slotted pallet and a table, in both directions.

## Real robot

<div class="row">
  <div class="col-sm mt-3 mt-md-0">
    {% include clip.liquid name="bimanual_pallet_to_table" caption="Pallet to table" %}
  </div>
  <div class="col-sm mt-3 mt-md-0">
    {% include clip.liquid name="bimanual_table_to_pallet" caption="Table to pallet" %}
  </div>
</div>

## Training in simulation

<div class="row justify-content-sm-center">
  <div class="col-sm-9 mt-3 mt-md-0">
    {% include clip.liquid name="bimanual_sim" caption="Policy training in massively parallel simulation" %}
  </div>
</div>
